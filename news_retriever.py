import requests
from datetime import datetime

NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"


def search_articles(query, api_key, page_size=5):
    """Search NewsAPI 'everything' endpoint and return list of articles.

    Each article dict contains: id, title, description, content, url, publishedAt, source
    """
    params = {
        "q": query,
        "pageSize": page_size,
        "language": "en",
        "sortBy": "relevancy",
    }
    headers = {"Authorization": api_key}
    resp = requests.get(NEWSAPI_ENDPOINT, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    articles = []
    for i, a in enumerate(data.get("articles", [])):
        content = a.get("content") or a.get("description") or ""
        articles.append({
            "id": f"{a.get('source',{}).get('id') or 'src'}_{i}_{int(datetime.utcnow().timestamp())}",
            "title": a.get("title"),
            "description": a.get("description"),
            "content": content,
            "url": a.get("url"),
            "publishedAt": a.get("publishedAt"),
            "source": a.get("source", {}).get("name"),
        })
    return articles
