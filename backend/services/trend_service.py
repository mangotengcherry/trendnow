from pytrends.request import TrendReq
import feedparser
import random
from typing import List, Dict, Any

class TrendService:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def get_trending_searches(self, country: str = 'united_states') -> List[str]:
        """
        Get trending searches for a specific country.
        """
        try:
            # pn values: 'united_states', 'south_korea'
            trends = self.pytrends.trending_searches(pn=country)
            return trends[0].tolist() 
        except Exception as e:
            print(f"Error fetching trends: {e}")
            # Fallback to mock data
            return self._get_mock_trends(country)

    def get_realtime_trending_searches(self, country: str = 'US') -> List[Dict[str, Any]]:
        """
        Get real-time trending searches.
        """
        try:
            # realtime_trending_searches returns a DataFrame
            # standard pn is 2-letter code for realtime
            if country.lower() == 'south_korea':
                country_code = 'KR'
            elif country.lower() == 'united_states':
                country_code = 'US'
            else:
                country_code = country

            trends_df = self.pytrends.realtime_trending_searches(pn=country_code)
            result = []
            for index, row in trends_df.iterrows():
                 result.append({
                     "title": row.get('title', ''),
                     "entity_names": row.get('entity_names', []),
                 })
            return result
        except Exception as e:
            print(f"Error fetching realtime trends: {e}")
            # Fallback to mock data with simple structure
            mock_trends = self._get_mock_trends('south_korea' if country in ['KR', 'south_korea'] else 'united_states')
            return [{"title": t, "entity_names": []} for t in mock_trends]

    def _get_mock_trends(self, country: str) -> List[str]:
        if country == 'south_korea' or country == 'KR':
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
        """
        Get related news for a keyword using Google News RSS.
        """
        encoded_keyword = keyword.replace(' ', '+')
        rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-US&gl=US&ceid=US:en"
        # For Korean content if needed, we could adjust hl/gl/ceid.
        
        feed = feedparser.parse(rss_url)
        news_items = []
        for entry in feed.entries[:5]: # Top 5 news
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "source": entry.source.title if hasattr(entry, 'source') else "Google News"
            })
        return news_items

    def get_mock_social_posts(self, keyword: str) -> List[Dict[str, str]]:
        """
        Generate mock social media posts since we don't have API access.
        """
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
