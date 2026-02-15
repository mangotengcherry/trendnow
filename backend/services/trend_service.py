from trendspy import Trends
import feedparser
import random
from typing import List, Dict, Any

class TrendService:
    def __init__(self):
        self.trends_client = Trends()

    def get_trending_searches(self, country: str = 'united_states') -> List[str]:
        country_map = {'united_states': 'US', 'south_korea': 'KR'}
        geo = country_map.get(country, 'US')
        try:
            trending = self.trends_client.trending_now(geo=geo)
            keywords = []
            for item in trending[:20]:
                keyword = str(item) if not hasattr(item, 'keyword') else item.keyword
                keywords.append(keyword)
            return keywords if keywords else self._get_mock_trends(country)
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return self._get_mock_trends(country)

    def _get_mock_trends(self, country: str) -> List[str]:
        if country in ('south_korea', 'KR'):
            return [
                "손흥민", "비트코인", "삼성전자", "오늘 날씨", "주식 시장",
                "부동산 정책", "아이폰 16", "넷플릭스 신작", "유튜브 인기", "환율 정보"
            ]
        else:
            return [
                "Taylor Swift", "Super Bowl", "OpenAI", "Bitcoin", "Election Results",
                "NBA Finals", "Cyber Truck", "Elon Musk", "Starship Launch", "iPhone 16"
            ]

    def get_related_news(self, keyword: str) -> List[Dict[str, str]]:
        encoded_keyword = keyword.replace(' ', '+')
        rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(rss_url)
        news_items = []
        for entry in feed.entries[:5]:
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "source": entry.source.title if hasattr(entry, 'source') else "Google News"
            })
        return news_items

    def get_mock_social_posts(self, keyword: str) -> List[Dict[str, str]]:
        platforms = ["Twitter", "Threads", "Reddit"]
        templates = [
            f"Everyone is talking about #{keyword} right now! 🤯",
            f"Just saw the news about {keyword}. What do you think?",
            f"Can't believe {keyword} is trending again.",
            f"Anyone else following the {keyword} situation? #trend",
            f"My thoughts on {keyword}: It's complicated."
        ]

        posts = []
        for _ in range(5):
            posts.append({
                "platform": random.choice(platforms),
                "author": f"user_{random.randint(1000, 9999)}",
                "content": random.choice(templates),
                "likes": random.randint(10, 5000),
                "shares": random.randint(5, 1000)
            })
        return posts

trend_service = TrendService()
