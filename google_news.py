import feedparser
from urllib.parse import quote_plus
from typing import List, Optional

def search_google_news(
    query: str,
    hl: str = "en-US",
    gl: str = "US",
    ceid: str = "US:en",
    topic: Optional[str] = None,
    location: Optional[str] = None,
    max_articles: int = 10
) -> List[dict]:
    """
    Search Google News RSS and return a list of articles.
    Args:
        query (str): Search keywords.
        hl (str): Language code.
        gl (str): Country code.
        ceid (str): Country:Language code.
        topic (str, optional): News topic.
        location (str, optional): Location for geo news.
        max_articles (int): Max number of articles to return.
    Returns:
        List[dict]: List of articles with title, link, published, source, summary.
    """
    # Build RSS URL
    if topic:
        base_url = f"https://news.google.com/rss/headlines/section/topic/{quote_plus(topic.upper())}"
        params = f"?hl={hl}&gl={gl}&ceid={ceid}"
        rss_url = base_url + params
    elif location:
        base_url = f"https://news.google.com/rss/headlines/section/geo/{quote_plus(location)}"
        params = f"?hl={hl}&gl={gl}&ceid={ceid}"
        rss_url = base_url + params
    else:
        base_url = "https://news.google.com/rss/search?q="
        query_encoded = quote_plus(query)
        params = f"&hl={hl}&gl={gl}&ceid={ceid}"
        rss_url = f"{base_url}{query_encoded}{params}"

    # Parse RSS feed
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:max_articles]:
        # Google News often puts source after title with ' - '
        title_parts = entry.title.split(" - ")
        clean_title = " - ".join(title_parts[:-1]) if len(title_parts) > 1 else entry.title
        source = title_parts[-1] if len(title_parts) > 1 else "Unknown"
        published = entry.get("published", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        articles.append({
            "title": clean_title,
            "source": source,
            "published": published,
            "link": link,
            "summary": summary
        })
    return articles