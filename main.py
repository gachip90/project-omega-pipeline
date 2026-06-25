import json
import os
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify as md
from openai import OpenAI


load_dotenv()

API_URL = os.getenv(
    "ZENDESK_ARTICLES_URL",
    "https://support.optisigns.com/api/v2/help_center/en-us/articles.json?page=8&per_page=50",
)
OUTPUT_DIR = "output_docs"
CHUNKED_DIR = "chunked_docs"
STATE_FILE = "sync_state.json"
VECTOR_STORE_NAME = os.getenv("VECTOR_STORE_NAME", "OptiBot_Knowledge_Base")
REQUEST_TIMEOUT_SECONDS = 30

client = OpenAI()

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHUNKED_DIR, exist_ok=True)


@dataclass
class ChangedArticle:
    doc_id: str
    updated_at: str
    file_path: str


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, sort_keys=True)


def clean_filename(title):
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", title).strip().lower()
    return re.sub(r"[-\s]+", "-", slug) or "untitled"


def clean_article_html(html_body):
    soup = BeautifulSoup(html_body or "", "html.parser")

    for tag in soup(["script", "style", "noscript", "iframe", "form"]):
        tag.decompose()

    noisy_selectors = [
        "nav",
        "aside",
        "footer",
        "header",
        ".ad",
        ".ads",
        ".advertisement",
        ".breadcrumb",
        ".breadcrumbs",
        ".sidebar",
        ".related-articles",
        ".article-votes",
        ".article-relatives",
    ]
    for selector in noisy_selectors:
        for tag in soup.select(selector):
            tag.decompose()

    return str(soup)


def article_to_markdown(article):
    title = article.get("title", "Untitled")
    html_body = clean_article_html(article.get("body", ""))
    article_url = article.get("html_url", "")
    raw_markdown = md(html_body, heading_style="ATX", strip=["script", "style"])
    raw_markdown = re.sub(r"\n{3,}", "\n\n", raw_markdown).strip()
    return f"# {title}\n\n{raw_markdown}\n\n---\nArticle URL: {article_url}\n"


def fetch_articles():
    print(f"[*] Fetching articles from Zendesk API: {API_URL}")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(API_URL, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    print(f"[*] Zendesk returned {len(articles)} articles.")
    return articles


def scrape_and_detect_delta():
    articles = fetch_articles()
    state = load_state()

    stats = {"added": 0, "updated": 0, "skipped": 0, "empty": 0, "failed": 0}
    changed_articles = []

    for article in articles:
        try:
            doc_id = str(article["id"])
            updated_at = article.get("updated_at")
            html_body = article.get("body", "")

            if not html_body:
                stats["empty"] += 1
                continue

            if doc_id not in state:
                stats["added"] += 1
            elif state[doc_id] != updated_at:
                stats["updated"] += 1
            else:
                stats["skipped"] += 1
                continue

            slug = clean_filename(article.get("title", "Untitled"))
            file_path = os.path.join(OUTPUT_DIR, f"{slug}.md")
            markdown = article_to_markdown(article)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            changed_articles.append(
                ChangedArticle(doc_id=doc_id, updated_at=updated_at, file_path=file_path)
            )
        except Exception as exc:
            stats["failed"] += 1
            print(f"[!] Failed to process article {article.get('id', 'unknown')}: {exc}")

    print(
        "[v] Delta check complete: "
        f"{stats['added']} added, {stats['updated']} updated, "
        f"{stats['skipped']} skipped, {stats['empty']} empty, {stats['failed']} failed."
    )
    print(f"[*] Files ready for chunking: {len(changed_articles)}")
    return changed_articles


def chunk_file(filepath):
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

    print(f"[*] Chunked {filepath}: {len(chunk_paths)} chunks generated.")
    return chunk_paths


def find_or_create_vector_store():
    vector_stores = client.vector_stores.list()
    for vector_store in vector_stores.data:
        if vector_store.name == VECTOR_STORE_NAME:
            print(f"[*] Using existing Vector Store: {vector_store.id}")
            return vector_store.id

    print(f"[*] Vector Store '{VECTOR_STORE_NAME}' not found. Creating new store...")
    vector_store = client.vector_stores.create(name=VECTOR_STORE_NAME)
    print(f"[*] Created Vector Store: {vector_store.id}")
    return vector_store.id


def upload_chunks(vector_store_id, chunk_paths):
    if not chunk_paths:
        print("[*] No chunks generated. Nothing to upload.")
        return True

    print(f"[*] Uploading {len(chunk_paths)} chunks to Vector Store {vector_store_id}...")
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
        f"[*] Upload summary: {completed} chunks embedded, "
        f"{len(failed)} chunks failed."
    )
    return not failed


def commit_state_updates(changed_articles):
    state = load_state()
    for article in changed_articles:
        state[article.doc_id] = article.updated_at
    save_state(state)
    print(f"[v] sync_state.json updated for {len(changed_articles)} articles.")


def main_job():
    print("=== STARTING DAILY SYNC JOB ===")

    try:
        changed_articles = scrape_and_detect_delta()
    except Exception as exc:
        print(f"[!] Scrape step failed. State was not changed: {exc}")
        raise

    if not changed_articles:
        print("[*] No changes detected. Exiting job cleanly.")
        print("=== SYNC JOB COMPLETED SUCCESSFULLY ===")
        return

    all_new_chunks = []
    for article in changed_articles:
        try:
            all_new_chunks.extend(chunk_file(article.file_path))
        except Exception as exc:
            print(f"[!] Failed to chunk {article.file_path}. State was not changed: {exc}")
            raise

    print(
        f"[*] Chunking summary: {len(changed_articles)} input files, "
        f"{len(all_new_chunks)} chunks generated."
    )

    vector_store_id = find_or_create_vector_store()
    upload_ok = upload_chunks(vector_store_id, all_new_chunks)

    if not upload_ok:
        raise RuntimeError("One or more chunks failed to upload. State was not changed.")

    commit_state_updates(changed_articles)
    print("=== SYNC JOB COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    main_job()
