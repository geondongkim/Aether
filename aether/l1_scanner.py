import asyncio
from typing import Dict, Any, Optional

from scrapling import Fetcher

class L1Scanner:
    """
    L1 Scanner (Static Engine)
    Scrapling을 사용하여 빠르고 가벼운 HTTP/HTTPS 요청을 보냅니다.
    응답 HTML을 분석하여 JS 렌더링이 필수적인지 판단합니다.
    """
    
    def __init__(self):
        # Scrapling의 Fetcher 인스턴스
        self.fetcher = Fetcher()

    async def fetch(self, url: str) -> Dict[str, Any]:
        """
        비동기적으로 대상 URL의 정적 HTML을 가져옵니다.
        """
        try:
            # Scrapling Fetcher를 통해 요청 수행
            response = self.fetcher.get(url)
            
            # Scrapling Response 객체에서 text, cookies 등 추출
            # Scrapling 0.4.x 버전에서는 body가 bytes 형태로 원본 HTML 제공
            html_content = response.body.decode('utf-8', errors='ignore') if hasattr(response, 'body') else ""
            cookies = getattr(response, "cookies", {}) # 가져올 수 없으면 빈 딕셔너리로 대체

            
            # 응답 유효성 및 JS 필요 여부 검사
            needs_js = self._is_js_required(html_content)
            
            return {
                "success": True,
                "url": url,
                "html": html_content,
                "cookies": cookies,
                "needs_js": needs_js,
                "engine": "L1",
                "status_code": response.status
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "needs_js": True, # 에러 발생 시 방어적으로 L2로 넘기도록 유도할 수 있음
                "engine": "L1"
            }

    def _is_js_required(self, html: str) -> bool:
        """
        HTML 텍스트를 분석하여 자바스크립트가 반드시 필요한지 판단합니다.
        - 안티봇 챌린지 메시지 (Cloudflare 등)
        - 콘텐츠가 비어있고 <noscript> 태그가 포함되어 있는지
        - 특정 SPA 프레임워크 징후
        """
        js_indicators = [
            "Enable JavaScript and cookies to continue",
            "Please enable JS and disable any ad blocker",
            "You need to enable JavaScript to run this app.",
            "Checking your browser before accessing",
            "<div id=\"app\"></div>" # 대표적인 SPA 태그 형태
        ]
        
        # 단순 휴리스틱: HTML 길이가 너무 짧고 본문이 거의 없는 경우 (동적 로딩 필요)
        if len(html) < 2000:
            if "<script" in html and "<body" in html:
                return True
                
        for indicator in js_indicators:
            if indicator.lower() in html.lower():
                return True
                
        return False
