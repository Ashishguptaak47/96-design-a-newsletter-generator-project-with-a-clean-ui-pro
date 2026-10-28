import jinja2
import markdown

DEFAULT_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f5f7; color: #333333; margin: 0; padding: 20px; line-height: 1.6; }
    .container { max-width: 680px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .header { text-align: center; border-bottom: 2px solid #eaeaea; padding-bottom: 20px; margin-bottom: 30px; }
    .header h1 { margin: 0 0 10px 0; color: #1a1a1a; font-size: 28px; }
    .header p { margin: 0; color: #666666; font-size: 16px; font-style: italic; }
    .block { margin-bottom: 30px; }
    .block-article h2 { color: #0066cc; margin-top: 0; font-size: 22px; }
    .block-article a { color: #0066cc; text-decoration: none; font-weight: bold; }
    .block-sponsor { background-color: #fffbe6; border: 1px solid #ffe58f; padding: 20px; border-radius: 8px; }
    .block-sponsor span.badge { background: #faad14; color: #fff; padding: 2px 8px; font-size: 11px; text-transform: uppercase; border-radius: 4px; font-weight: bold; }
    .block-cta { text-align: center; margin: 30px 0; }
    .btn { display: inline-block; background: #0066cc; color: #ffffff !important; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-weight: bold; }
    .footer { text-align: center; border-top: 1px solid #eaeaea; padding-top: 20px; font-size: 13px; color: #888888; margin-top: 40px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>{{ title or 'Weekly Newsletter' }}</h1>
      {% if tagline %}<p>{{ tagline }}</p>{% endif %}
    </div>
    <div class="content">
      {% for block in blocks %}
        {% if block.type == 'article' %}
          <div class="block block-article">
            <h2>{{ block.title }}</h2>
            <div>{{ block.content_html | safe }}</div>
            {% if block.link %}<p><a href="{{ block.link }}">Read more &rarr;</a></p>{% endif %}
          </div>
        {% elif block.type == 'sponsor' %}
          <div class="block block-sponsor">
            <span class="badge">Sponsored</span>
            <h3>{{ block.title }}</h3>
            <div>{{ block.content_html | safe }}</div>
            {% if block.link %}<p><a href="{{ block.link }}">Learn More</a></p>{% endif %}
          </div>
        {% elif block.type == 'cta' %}
          <div class="block block-cta">
            <a href="{{ block.link }}" class="btn">{{ block.title or 'Click Here' }}</a>
          </div>
        {% elif block.type == 'text' %}
          <div class="block block-text">
            <div>{{ block.content_html | safe }}</div>
          </div>
        {% endif %}
      {% endfor %}
    </div>
    <div class="footer">
      <p>{{ footer or 'Thank you for reading! Managed with Newsletter Generator.' }}</p>
    </div>
  </div>
</body>
</html>
"""

class NewsletterGenerator:
    def __init__(self, config):
        self.title = config.get('title', 'Weekly Newsletter')
        self.tagline = config.get('tagline', 'Insights and updates directly to your inbox')
        self.footer = config.get('footer', 'You are receiving this email because you subscribed.')
        raw_blocks = config.get('blocks', [])
        self.blocks = []
        for b in raw_blocks:
            processed = dict(b)
            content_text = b.get('content', '')
            processed['content_html'] = markdown.markdown(content_text) if content_text else ''
            self.blocks.append(processed)

    def render_html(self):
        template = jinja2.Template(DEFAULT_HTML_TEMPLATE)
        return template.render(
            title=self.title,
            tagline=self.tagline,
            footer=self.footer,
            blocks=self.blocks
        )

    def render_markdown(self):
        lines = [f"# {self.title}", f"*{self.tagline}*\n", "---"]
        for b in self.blocks:
            b_type = b.get('type')
            title = b.get('title', '')
            content = b.get('content', '')
            link = b.get('link', '')

            if b_type in ['article', 'sponsor']:
                prefix = "[SPONSORED] " if b_type == 'sponsor' else ""
                lines.append(f"\n## {prefix}{title}")
                if content:
                    lines.append(content)
                if link:
                    lines.append(f"\n[Read details...]({link})")
            elif b_type == 'cta':
                lines.append(f"\n\n**[{title or 'Click Here'}]({link})**\n\n")
            elif b_type == 'text':
                lines.append(f"\n{content}")
            lines.append("\n---")
        lines.append(f"\n\n*{self.footer}*")
        return "\n".join(lines)
