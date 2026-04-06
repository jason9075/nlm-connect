import os
import re
import json

def process_file(filepath, date_str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    
    title = ""
    source_id = ""
    type_val = ""
    text_lines = []
    
    in_text = False
    
    for line in lines:
        if line.startswith('#'):
            title = line.lstrip('#').strip()
        elif line.startswith('Source ID:'):
            source_id = line[len('Source ID:'):].strip()
        elif line.startswith('Type:'):
            type_val = line[len('Type:'):].strip()
            in_text = True
        elif in_text:
            text_lines.append(line)
            
    text = "\n".join(text_lines).strip()
    text = text.replace(" ", "")
    
    return {
        "date": date_str,
        "title": title,
        "source_id": source_id,
        "type": type_val,
        "text": text
    }

def main():
    transcript_dir = "transcripts"
    group_dir = "group"
    
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)
        
    files = []
    for filename in os.listdir(transcript_dir):
        if not filename.endswith('.md'):
            continue
        
        match = re.search(r'【(\d{8})】', filename)
        if match:
            date_str = match.group(1)
            files.append((date_str, filename))
            
    # Sort files by date
    files.sort(key=lambda x: x[0])
    
    # Process in chunks of 5
    for i in range(0, len(files), 5):
        chunk = files[i:i+5]
        start_date = chunk[0][0]
        end_date = chunk[-1][0]
        
        group_data = []
        for date_str, filename in chunk:
            filepath = os.path.join(transcript_dir, filename)
            try:
                data = process_file(filepath, date_str)
                group_data.append(data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
        output_filename = f"{start_date}-{end_date}.txt"
        if start_date == end_date and len(chunk) == 1:
             output_filename = f"{start_date}.txt"
             
        output_filepath = os.path.join(group_dir, output_filename)
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(group_data, f, ensure_ascii=False, indent=2)
            
        print(f"Written {output_filepath} with {len(group_data)} records.")

if __name__ == "__main__":
    main()
