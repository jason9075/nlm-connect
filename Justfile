default: help

# Show this help message
@help:
    just --list

# Install Python dependencies
install:
    pip install -r requirements.txt

# Run the main syncing script
run:
    python src/main.py --sync --output ./transcripts

# Process the transcripts into JSON/TXT chunks
process-transcripts:
    python process_transcripts.py

# Clean Python cache directories
clean:
    rm -rf __pycache__
    find . -type d -name "__pycache__" -exec rm -rf {} +

# Clear all sources from NotebookLM
clear-source:
    python src/main.py --clear
