import pytest
from app import create_app
from app.generator import NewsletterGenerator

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_generator_html_and_md():
    config = {
        'title': 'Test Newsletter',
        'tagline': 'Testing is essential',
        'footer': 'Unsubscribe anytime',
        'blocks': [
            {'type': 'article', 'title': 'Test Article', 'content': 'This is **bold** text.', 'link': 'https://example.com'}
        ]
    }
    gen = NewsletterGenerator(config)
    html_res = gen.render_html()
    md_res = gen.render_markdown()

    assert 'Test Newsletter' in html_res
    assert '<strong>bold</strong>' in html_res
    assert '# Test Newsletter' in md_res
    assert 'https://example.com' in md_res

def test_preview_api(client):
    payload = {
        'title': 'API Test',
        'blocks': [{'type': 'cta', 'title': 'Click Me', 'link': 'https://test.com'}]
    }
    response = client.post('/api/preview', json=payload)
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'html' in json_data
    assert 'markdown' in json_data
    assert 'API Test' in json_data['html']

def test_export_api(client):
    payload = {
        'format': 'markdown',
        'newsletter': {'title': 'Export Test', 'blocks': []}
    }
    response = client.post('/api/export', json=payload)
    assert response.status_code == 200
    assert 'text/markdown' in response.headers['Content-Type']
    assert '# Export Test' in response.data.decode('utf-8')
