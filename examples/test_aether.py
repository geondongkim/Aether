import asyncio
import sys
import os

# 현재 디렉토리를 파이썬 경로에 추가하여 aether 모듈 임포트 가능하게 함
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__line__), '..'))) if '__line__' in globals() else sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aether.core import AetherEngine

async def main():
    # Aether 엔진 인스턴스화 (헤드리스 모드)
    engine = AetherEngine(headless=True)
    
    print("==================================================")
    print("1. 정적 페이지 (L1 Scanner Only 예상)")
    print("==================================================")
    url_static = "http://example.com"
    result_static = await engine.fetch(url_static)
    print(f"URL: {result_static['url']}")
    print(f"사용 엔진: {result_static.get('engine')}")
    print(f"상태 코드: {result_static.get('status_code')}")
    print(f"HTML 길이: {len(result_static.get('html', ''))}")
    
    print("\n==================================================")
    print("2. 동적 페이지 (L1 -> L2 Renderer 전환 예상)")
    print("==================================================")
    # SPA 또는 JS 렌더링이 필수적인 사이트 예시
    url_dynamic = "https://ko.reactjs.org/"
    result_dynamic = await engine.fetch(url_dynamic)
    print(f"URL: {result_dynamic['url']}")
    print(f"사용 엔진: {result_dynamic.get('engine')}")
    print(f"상태 코드: {result_dynamic.get('status_code')}")
    print(f"HTML 길이: {len(result_dynamic.get('html', ''))}")
    
if __name__ == "__main__":
    asyncio.run(main())
