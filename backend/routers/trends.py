from fastapi import APIRouter
from services.trend_service import trend_service

router = APIRouter(prefix="/api", tags=["trends"])

@router.get("/trends")
async def get_trends(country: str = "united_states"):
    """
    Get trending keywords for a country.
    Supported countries: 'united_states', 'south_korea'
    """
    trends = trend_service.get_trending_searches(country)
    return {"trends": trends, "country": country}

@router.get("/related/{keyword}")
async def get_related_content(keyword: str):
    """
    Get related news and social posts for a keyword.
    """
    news = trend_service.get_related_news(keyword)
    posts = trend_service.get_mock_social_posts(keyword)
    return {
        "keyword": keyword,
        "news": news,
        "social_posts": posts
    }
