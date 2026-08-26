#!/usr/bin/env python3
"""
Trakt Personal Sync Script
A simple personal tool to fetch and display recent watched history.
For personal / non-commercial use only.
"""

import os
import requests
from datetime import datetime

CLIENT_ID = os.getenv("TRAKT_CLIENT_ID")
ACCESS_TOKEN = os.getenv("TRAKT_ACCESS_TOKEN")

BASE_URL = "https://api.trakt.tv"
HEADERS = {
    "Content-Type": "application/json",
    "trakt-api-version": "2",
    "trakt-api-key": CLIENT_ID,
}

if ACCESS_TOKEN:
    HEADERS["Authorization"] = f"Bearer {ACCESS_TOKEN}"


def get_recent_history(limit=10):
    url = f"{BASE_URL}/sync/history"
    params = {"limit": limit, "extended": "full"}
    response = requests.get(url, headers=HEADERS, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def get_trending_movies(limit=5):
    url = f"{BASE_URL}/movies/trending"
    params = {"limit": limit}
    response = requests.get(url, headers=HEADERS, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def main():
    if not CLIENT_ID:
        print("请先设置环境变量 TRAKT_CLIENT_ID")
        return

    print("=== Trakt Personal Sync ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    print("当前热门电影:")
    try:
        trending = get_trending_movies()
        for i, item in enumerate(trending, 1):
            movie = item["movie"]
            print(f"{i}. {movie['title']} ({movie.get('year', 'N/A')})")
    except Exception as e:
        print(f"获取热门电影失败: {e}")

    print()

    if ACCESS_TOKEN:
        print("最近观看记录:")
        try:
            history = get_recent_history()
            for item in history:
                media = item.get("movie") or item.get("episode")
                if media:
                    title = media.get("title") or media.get("show", {}).get("title", "Unknown")
                    watched_at = item.get("watched_at", "")[:10]
                    print(f"- {title}  ({watched_at})")
        except Exception as e:
            print(f"获取历史失败: {e}")
    else:
        print("未设置 TRAKT_ACCESS_TOKEN，跳过个人历史查询")


if __name__ == "__main__":
    main()
