import os
import argparse
import asyncio
import re
from pathlib import Path
from dotenv import load_dotenv
from client import NLMClient

# Load environment variables from .env file
load_dotenv()

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to be safe for filesystem."""
    # Remove invalid characters
    return re.sub(r'[<>:"/\\|?*]', '', filename).strip()

async def sync_transcripts(output_dir: Path):
    notebook_id = os.getenv("NOTEBOOK_ID")
    if not notebook_id:
        print("Error: NOTEBOOK_ID environment variable is not set.")
        return

    client = NLMClient(notebook_id)
    
    # Check if output dir exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. List all sources first
    try:
        sources = await client.list_sources()
    except Exception as e:
        print(f"Error listing sources: {e}")
        return

    print(f"Found {len(sources)} sources.")

    for source in sources:
        safe_title = sanitize_filename(source.title)
        filename = f"{safe_title}.md"
        file_path = output_dir / filename
        
        # 2. Check if file exists BEFORE fetching content
        if file_path.exists():
            print(f"[SKIP] {filename} already exists.")
            continue
            
        print(f"[FETCH] Downloading content for: {source.title}...")
        try:
            full_text = await client.get_source_content(source.id)
            if full_text and full_text.content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"# {source.title}\n\n")
                    f.write(f"Source ID: {source.id}\n")
                    f.write(f"Type: {source.source_type}\n\n")
                    f.write(full_text.content)
            else:
                 print(f"Warning: No content found for {source.title}")
                 
        except Exception as e:
            print(f"Failed to fetch content for {source.title}: {e}")

async def clear_sources():
    notebook_id = os.getenv("NOTEBOOK_ID")
    if not notebook_id:
        print("Error: NOTEBOOK_ID environment variable is not set.")
        return

    client = NLMClient(notebook_id)
    try:
        sources = await client.list_sources()
    except Exception as e:
        print(f"Error listing sources: {e}")
        return

    print(f"Found {len(sources)} sources to delete.")
    for source in sources:
        print(f"[DELETE] Deleting source: {source.title}...")
        try:
            await client.delete_source(source.id)
        except Exception as e:
            print(f"Failed to delete {source.title}: {e}")
    print("Done clearing sources.")

def main():
    parser = argparse.ArgumentParser(description="NotebookLM Connect - Transcript Sync")
    parser.add_argument("--sync", action="store_true", help="Sync transcripts from NotebookLM")
    parser.add_argument("--clear", action="store_true", help="Clear all sources from NotebookLM")
    parser.add_argument("--output", type=str, default="./transcripts", help="Output directory")
    
    args = parser.parse_args()
    
    if args.sync:
        asyncio.run(sync_transcripts(Path(args.output)))
    elif args.clear:
        asyncio.run(clear_sources())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
