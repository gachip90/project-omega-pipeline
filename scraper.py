import os
import re

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


API_URL = os.getenv(
    "ZENDESK_ARTICLES_URL",
    "https://support.optisigns.com/api/v2/help_center/en-us/articles.json?page=8&per_page=50",
)
OUTPUT_DIR = "output_docs"
REQUEST_TIMEOUT_SECONDS = 30

os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_filename(title):
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", title).strip().lower()
    return re.sub(r"[-\s]+", "-", slug) or "untitled"


def clean_article_html(html_body):
    soup = BeautifulSoup(html_body or "", "html.parser")

    for tag in soup(["script", "style", "noscript", "iframe", "form"]):
        tag.decompose()

    for selector in [
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
    ]:
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


def fetch_and_convert_articles():
    print(f"[*] Fetching data from: {API_URL}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(API_URL, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    articles = response.json().get("articles", [])
    print(f"[*] Retrieved {len(articles)} articles. Converting to Markdown...")

    processed = 0
    failed = 0
    youtube_found = False

    for article in articles:
        try:
            if not article.get("body"):
                continue

            title = article.get("title", "Untitled")
            if "How to use YouTube with OptiSigns" in title:
                youtube_found = True

            file_path = os.path.join(OUTPUT_DIR, f"{clean_filename(title)}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(article_to_markdown(article))

            processed += 1
        except Exception as exc:
            failed += 1
            print(f"[!] Failed to convert article {article.get('id', 'unknown')}: {exc}")

    print(
        f"[v] Completed. Saved {processed} Markdown files to '{OUTPUT_DIR}'. "
        f"{failed} articles failed."
    )

    if youtube_found:
        print("[v] Target article 'How to use YouTube with OptiSigns' confirmed in dataset.")
    else:
        print("[!] WARNING: Target YouTube article not found.")


if __name__ == "__main__":
    fetch_and_convert_articles()
