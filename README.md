<div align="center">
# Aura SEO Intelligence Agent

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-3.1_Flash_Preview-4285F4)
![LangChain](https://img.shields.io/badge/LangChain-Agent_Workflow-1C3C3C)
![Playwright](https://img.shields.io/badge/Playwright-Web_Automation-2EAD33?logo=playwright&logoColor=white)
</div>

AI-assisted SEO audit agent that combines website inspection, competitor discovery, performance analysis, and PDF reporting into one project.

## Project Overview

Aura is designed as a multi-tool SEO assistant. It can audit a target website, collect structured findings, check performance data, inspect competitor-style search results, and package output into a PDF-ready format. It also keeps a conversational layer on top using Gemini and LangChain.

## Key Features

- Runs a website SEO audit from a supplied URL.
- Collects title, meta, headings, links, image alt data, and content stats.
- Supports PageSpeed and mobile-style performance checks through API keys.
- Uses Playwright for competitor result discovery.
- Generates PDF reports from HTML content.
- Uses environment variables for Gemini and API keys.

## Tech Stack

- Python
- LangChain
- Gemini `gemini-3.1-flash-preview`
- Playwright
- BeautifulSoup
- Requests
- xhtml2pdf

## Project Structure

```text
SEO/
├── SEOBOT.py
├── audit_class.py
├── googlesearch.py
├── dachecker.py
├── requirements.txt
└── .env.example
```

## Environment Variables

Create a `.env` file from `.env.example` and configure:

- `GEMINI_API_KEY`
- `GOOGLE_PAGESPEED_API_KEY`
- `RAPIDAPI_KEY`
- `RAPIDAPI_HOST`

## Run Locally

```bash
python -m venv .venv
pip install -r requirements.txt
playwright install
python SEOBOT.py
```

## Audit Coverage

- Basic on-page SEO signals
- Link and image checks
- Core performance data
- Competitor-style discovery
- PDF export support

## Best Use Cases

- SEO analysis demos
- AI agent workflow experiments
- Internal website review tooling
- Portfolio projects involving automation and LLMs

## Future Improvements

- Add richer schema detection
- Enable full keyword extraction reports
- Store audit history and comparisons
- Add a web dashboard instead of CLI-only flow
