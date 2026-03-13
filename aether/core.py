import asyncio
import logging
from typing import Dict, Any, Optional

from .l1_scanner import L1Scanner
from .l2_renderer import L2Renderer

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - Aether [%(levelname)s] - %(message)s')
logger = logging.getLogger("AetherEngine")

class AetherEngine:
    """
    Aether 메인 엔진
    L1 스캐너와 L2 렌더러를 조율하여 최적의 스크래핑 파이프라인을 실행합니다.
    """
    
    def __init__(self, use_renderer: bool = True, headless: bool = True):
        self.use_renderer = use_renderer
        self.l1_scanner = L1Scanner()
        if self.use_renderer:
            self.l2_renderer = L2Renderer(headless=headless)
        else:
            self.l2_renderer = None

    async def fetch(self, url: str) -> Dict[str, Any]:
        """
        URL 데이터를 수집합니다.
        1. L1(Static)으로 먼저 찌름.
        2. JS 렌더링이 필요하다고 판단되면 L2(Dynamic)로 전환하여 다시 수집.
        """
        logger.info(f"요청 시작: {url}")
        
        # 1. L1 스캐닝 (Static First)
        logger.info("L1 Scanner (Scrapling) 동작 중...")
        l1_result = await self.l1_scanner.fetch(url)
        
        if not l1_result.get("success"):
            logger.warning(f"L1 Scanner 실패: {l1_result.get('error')}")
        
        # JS 렌더링이 필수적인지 확인
        needs_js = l1_result.get("needs_js", False)
        
        if not needs_js or not self.use_renderer:
            logger.info("정적 데이터 수집 성공 혹은 브라우저 렌더링 비활성화됨. (L1 데이터 반환)")
            return l1_result
            
        logger.info("L1 분석 결과 JavaScript 렌더링 필요 감지됨. L2 Renderer (Playwright)로 전환합니다.")
        
        # 2. L2 렌더러 (Dynamic) 전환
        # L1에서 얻은 쿠키 세션 주입
        cookies = l1_result.get("cookies", [])
        
        # Scrapling 쿠키 포맷을 Playwright 형식으로 변환 (간략화)
        formatted_cookies = []
        if isinstance(cookies, dict):
             for name, value in cookies.items():
                 # Playwright는 도메인, 경로 등이 필요할 수 있으나 생략하거나 url 파싱하여 추가 가능
                 # 여기서는 임시 구현
                 pass
        
        logger.info("L2 Renderer 동작 중...")
        l2_result = await self.l2_renderer.fetch(url, extra_cookies=None) # 포맷 이슈로 임시 None
        
        if l2_result.get("success"):
            logger.info("L2 Renderer를 통한 동적 수집 성공.")
        else:
            logger.error(f"L2 Renderer 실패: {l2_result.get('error')}")
            
        return l2_result
