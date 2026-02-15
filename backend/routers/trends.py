from fastapi import APIRouter, HTTPException
from typing import List, Optional
from services.trend_service import trend_service

router = APIRouter(prefix="/api", tags=["trends"])

@router.get("/trends")
async def get_trends(country: str = "united_states"):
    """
    Get trending keywords for a country.
    Supported countries: 'united_states', 'south_korea'
    """
    # Map to country code for realtime
    country_map = {
        'united_states': 'US',
        'south_korea': 'KR'
    }
    
    country_code = country_map.get(country, 'US')
    
    # Try realtime first
    realtime_data = trend_service.get_realtime_trending_searches(country_code)
    
    if realtime_data:
        trends = [item['title'] for item in realtime_data]
    else:
        # Fallback to daily
        # Note: trending_searches(pn='united_states')
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
