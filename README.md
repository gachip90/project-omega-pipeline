# OptiBot Knowledge Pipeline

Daily scraper/uploader for the OptiBot mini-clone take-home test. The job pulls OptiSigns Help Center articles from the Zendesk API, converts article HTML into clean Markdown, chunks content by headings, and uploads only new or updated chunks to an OpenAI Vector Store.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Set `OPENAI_API_KEY` in `.env`. Optional settings:

- `VECTOR_STORE_NAME`: OpenAI Vector Store name. Defaults to `OptiBot_Knowledge_Base`.
- `ZENDESK_ARTICLES_URL`: Zendesk Help Center article API URL.

## Run Locally

Initial Markdown export:

```bash
python scraper.py
```

Upload existing Markdown files to a Vector Store:

```bash
python upload_vector.py
```

Daily delta job:

```bash
python main.py
```

Docker:

```bash
docker build -t optibot-pipeline .
docker run --rm -e OPENAI_API_KEY=sk-your-openai-api-key optibot-pipeline
```

## Chunking Strategy

Each article is saved as one Markdown file with the article title as `# Heading` and the source `Article URL` appended at the bottom. Before conversion, the scraper removes common nav/ad/noisy HTML elements such as `nav`, `aside`, `footer`, `header`, scripts, forms, ad containers, breadcrumbs, sidebars, related articles, and voting widgets.

Chunks are split on `##` and `###` headings. Every chunk repeats the article title and keeps the `Article URL` footer so File Search responses can cite the original support article.

## Daily Job

I originally planned to deploy the scraper as a daily job on DigitalOcean Platform Jobs, but I hit an external blocker while setting up payment on the account, so the scheduled run was moved to GitHub Actions for this submission window.

The repository uses [`.github/workflows/daily-scraper.yml`](.github/workflows/daily-scraper.yml) to run `python main.py` on a daily cron schedule and also supports manual runs through `workflow_dispatch`.

## Daily Job Logs

![GitHub Actions daily run log](assets/github-actions-log.png)

The screenshot above shows a successful GitHub Actions run of the daily sync job, including article fetch, delta detection, chunk generation, vector upload, and `sync_state.json` update.

## Playground Screenshot

![OptiBot Playground answer](assets/optibot-playground-answer.png)

The screenshot above shows OptiBot answering "How do I add a YouTube video?" with numbered steps and a cited `Article URL`, which is the exact sanity check requested in the take-home.
