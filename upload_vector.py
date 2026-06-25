import glob
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

INPUT_DIR = "output_docs"
CHUNKED_DIR = "chunked_docs"
VECTOR_STORE_NAME = os.getenv("VECTOR_STORE_NAME", "OptiBot_Knowledge_Base")

client = OpenAI()


def chunk_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    url = ""
    for line in reversed(lines):
        if line.startswith("Article URL:"):
            url = line.strip()
            break

    main_title = "Untitled"
    chunks = []
    current_chunk = []

    for line in lines:
        if line.startswith("# "):
            main_title = line.strip()
            current_chunk.append(line)
        elif line.startswith("## ") or line.startswith("### "):
            if current_chunk:
                chunks.append("".join(current_chunk))
            current_chunk = [main_title + "\n\n", line]
        elif not line.startswith("Article URL:") and line.strip() != "---":
            current_chunk.append(line)

    if current_chunk:
        chunks.append("".join(current_chunk))

    base_name = os.path.basename(filepath).replace(".md", "")
    chunk_paths = []

    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) > len(main_title) + 15:
            chunk_filename = f"{base_name}_chunk_{i + 1}.md"
            chunk_path = os.path.join(CHUNKED_DIR, chunk_filename)
            with open(chunk_path, "w", encoding="utf-8") as out_f:
                out_f.write(chunk.rstrip())
                out_f.write(f"\n\n---\n{url}\n")
            chunk_paths.append(chunk_path)

    return chunk_paths


def chunk_markdown_files():
    os.makedirs(CHUNKED_DIR, exist_ok=True)

    files = glob.glob(os.path.join(INPUT_DIR, "*.md"))
    all_chunks = []

    print(f"[*] Input Markdown files: {len(files)}")

    for filepath in files:
        try:
            chunk_paths = chunk_markdown_file(filepath)
            all_chunks.extend(chunk_paths)
            print(f"[*] Chunked {filepath}: {len(chunk_paths)} chunks generated.")
        except Exception as exc:
            print(f"[!] Failed to chunk {filepath}: {exc}")

    print(f"[v] Chunking complete. Generated {len(all_chunks)} chunks.")
    return all_chunks


def find_or_create_vector_store():
    vector_stores = client.vector_stores.list()
    for vector_store in vector_stores.data:
        if vector_store.name == VECTOR_STORE_NAME:
            print(f"[*] Using existing Vector Store: {vector_store.id}")
            return vector_store.id

    print(f"[*] Creating OpenAI Vector Store: '{VECTOR_STORE_NAME}'...")
    vector_store = client.vector_stores.create(name=VECTOR_STORE_NAME)
    print(f"[*] Vector Store ID: {vector_store.id}")
    return vector_store.id


def upload_chunks(vector_store_id, chunk_paths):
    if not chunk_paths:
        print("[!] No chunks generated. Exiting.")
        return False

    print(f"[*] Uploading {len(chunk_paths)} chunks via OpenAI API...")
    completed = 0
    failed = []

    for path in chunk_paths:
        try:
            with open(path, "rb") as stream:
                file_batch = client.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store_id,
                    files=[stream],
                )

            file_counts = file_batch.file_counts
            if file_batch.status == "completed" and file_counts.failed == 0:
                completed += file_counts.completed
                print(f"[v] Uploaded chunk: {path}")
            else:
                failed.append(path)
                print(
                    f"[!] Upload incomplete for {path}: "
                    f"status={file_batch.status}, completed={file_counts.completed}, "
                    f"failed={file_counts.failed}, cancelled={file_counts.cancelled}"
                )
        except Exception as exc:
            failed.append(path)
            print(f"[!] Upload failed for {path}: {exc}")

    print(
        f"[v] Upload summary: {completed} chunks embedded, "
        f"{len(failed)} chunks failed."
    )
    return not failed


def upload_existing_markdown_to_vector_store():
    chunk_paths = chunk_markdown_files()
    vector_store_id = find_or_create_vector_store()

    if not upload_chunks(vector_store_id, chunk_paths):
        raise RuntimeError("One or more chunks failed to upload.")

    print("=======================================================")
    print("Vector Store upload complete. Attach this store to your Assistant in Playground.")


if __name__ == "__main__":
    upload_existing_markdown_to_vector_store()
