#!/usr/bin/env python3
"""
企業名リストから公式HPを検索し、直近開催されるインターン情報を取得するスクリプト
"""

import asyncio
import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from internship_scraper import main

if __name__ == "__main__":
    asyncio.run(main())
