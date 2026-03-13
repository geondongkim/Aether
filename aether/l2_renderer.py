import asyncio
from typing import Dict, Any, List
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

class L2Renderer:
    """
    L2 Renderer (Dynamic Engine)
    Playwright를 사용하여 JavaScript를 렌더링합니다.
    스텔스 모드를 지원하여 봇 탐지를 회피하고, 불필요한 리소스 로딩을 차단합니다.
    """
    
    def __init__(self, headless: bool = True):
        self.headless = headless

    async def fetch(self, url: str, extra_cookies: List[Dict] = None) -> Dict[str, Any]:
        """
        비동기적으로 대상 URL을 Playwright로 접근하여 완전한 HTML을 반환합니다.
        """
        async with async_playwright() as p:
            # 브라우저 런칭
            browser = await p.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-features=IsolateOrigins,site-per-process"
                ]
            )
            
            # 콘텍스트 생성
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            
            # L1 스캐너로부터 전달받은 쿠키가 있다면 주입
            if extra_cookies:
                await context.add_cookies(extra_cookies)
                
            page = await context.new_page()
            
            # Stealth 모드 적용 (playwright-stealth)
            await stealth_async(page)
            
            # 리소스 필터링: 불필요한 리소스 차단 로직 (최적화)
            await page.route("**/*", self._block_unnecessary_resources)
            
            try:
                # 페이지 이동 (네트워크 유휴 상태까지 대기)
                response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # 추가적인 동적 렌더링이 필요한 스파이더링 사이트를 위한 대기 시간 부여
                # SPA 사이트 로딩 보장을 위한 예시
                await page.wait_for_timeout(2000)
                
                html_content = await page.content()
                cookies = await context.cookies()
                
                return {
                    "success": True,
                    "url": url,
                    "html": html_content,
                    "cookies": cookies,
                    "engine": "L2",
                    "status_code": response.status if response else 200
                }
            except Exception as e:
                return {
                    "success": False,
                    "url": url,
                    "error": str(e),
                    "engine": "L2"
                }
            finally:
                await browser.close()
                
    async def _block_unnecessary_resources(self, route):
        """이미지, 미디어, 폰트 등을 차단하여 브라우저 로딩 속도를 최적화합니다."""
        blocked_resource_types = ['image', 'media', 'font', 'stylesheet', 'other']
        if route.request.resource_type in blocked_resource_types:
            await route.abort()
        else:
            await route.continue_()
