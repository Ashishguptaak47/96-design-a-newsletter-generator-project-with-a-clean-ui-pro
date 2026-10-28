# Modern Newsletter Generator

A full-featured, interactive Python newsletter generator web application built with Flask, Jinja2, and custom CSS/JS. Easily compose, customize, preview, and export responsive HTML emails and Markdown newsletters.

## Features
- **Interactive Block Builder**: Add Headers, Articles, Quick Links, Sponsor Callouts, and Call to Action blocks.
- **Live Dual Preview**: Render live HTML email previews alongside formatted Markdown output.
- **RSS News Ingestion**: Automatically import top stories from RSS feeds into your newsletter.
- **Multiple Themes**: Modern Clean, Tech Minimal, and Editorial styles.
- **Export Capability**: Direct download options for HTML templates and Markdown files.

## Project Structure
```
newsletter-generator/
├── app/
│   ├── __init__.py
│   ├── generator.py
│   ├── rss_fetcher.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       └── index.html
├── tests/
│   └── test_main.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000`.

## Running Tests
```bash
pytest
```
