import os
from flask import Flask, render_template, request, jsonify, Response
from app.generator import NewsletterGenerator
from app.rss_fetcher import fetch_rss_feed

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/preview', methods=['POST'])
    def preview():
        data = request.json or {}
        generator = NewsletterGenerator(data)
        return jsonify({
            'html': generator.render_html(),
            'markdown': generator.render_markdown()
        })

    @app.route('/api/fetch-rss', methods=['POST'])
    def rss():
        data = request.json or {}
        url = data.get('url', '')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        articles = fetch_rss_feed(url)
        return jsonify({'articles': articles})

    @app.route('/api/export', methods=['POST'])
    def export():
        data = request.json or {}
        export_format = data.get('format', 'html')
        generator = NewsletterGenerator(data.get('newsletter', {}))
        
        if export_format == 'markdown':
            content = generator.render_markdown()
            mimetype = 'text/markdown'
            filename = 'newsletter.md'
        else:
            content = generator.render_html()
            mimetype = 'text/html'
            filename = 'newsletter.html'
            
        return Response(
            content,
            mimetype=mimetype,
            headers={'Content-Disposition': f'attachment;filename={filename}'}
        )

    return app
