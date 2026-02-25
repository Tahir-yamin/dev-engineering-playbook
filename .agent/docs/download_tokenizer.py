import os
import urllib.request
import sys

# Usage: python download_tok.py <folder_path>

if len(sys.argv) < 2:
    print("Usage: python download_tok.py <folder_path>")
    sys.exit(1)

folder = sys.argv[1]

if not os.path.exists(folder):
    try:
        os.makedirs(folder)
    except Exception as e:
        print(f"Error creating folder {folder}: {e}")
        sys.exit(1)

# Using mlabonne public mirror (likely compatible & ungated)
urls = {
    "tokenizer.model": "https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated/resolve/main/tokenizer.model?download=true",
    "config.json": "https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated/resolve/main/config.json?download=true",
    "tokenizer_config.json": "https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated/resolve/main/tokenizer_config.json?download=true",
    "special_tokens_map.json": "https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated/resolve/main/special_tokens_map.json?download=true"
}

for filename, url in urls.items():
    path = os.path.join(folder, filename)
    print(f"Downloading {filename} to {path}...")
    try:
        urllib.request.urlretrieve(url, path)
        size = os.path.getsize(path)
        print(f"Downloaded {filename} ({size} bytes)")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
