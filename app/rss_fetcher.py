import urllib.request
import xml.etree.ElementTree as ET

def fetch_rss_feed(feed_url, limit=5):
    """Parses RSS/Atom XML from a URL without external heavy dependencies."""
    articles = []
    try:
        req = urllib.request.Request(
            feed_url, 
            headers={'User-Agent': 'Mozilla/5.0 (NewsletterGenerator/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        
        # Standard RSS 2.0
        channel = root.find('channel')
        if channel is not None:
            for item in channel.findall('item')[:limit]:
                title = item.findtext('title', 'Untitled')
                link = item.findtext('link', '')
                description = item.findtext('description', '')
                articles.append({
                    'title': title.strip(),
                    'link': link.strip(),
                    'summary': description.strip()[:200] + ('...' if len(description) > 200 else '')
                })
            return articles
            
        # Atom feed fallback
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', namespaces) or root.findall('entry')
        for entry in entries[:limit]:
            title = entry.findtext('atom:title', namespaces) or entry.findtext('title', 'Untitled')
            link_elem = entry.find('atom:link', namespaces) or entry.find('link')
            link = link_elem.attrib.get('href', '') if link_elem is not None else ''
            summary = entry.findtext('atom:summary', namespaces) or entry.findtext('summary', '')
            articles.append({
                'title': title.strip(),
                'link': link.strip(),
                'summary': summary.strip()[:200] + ('...' if len(summary) > 200 else '')
            })
    except Exception as e:
        articles.append({
            'title': 'Error fetching RSS feed',
            'link': '',
            'summary': str(e)
        })
    return articles
