# Aether (에테르) 🌬️

Aether는 공기처럼 가볍지만(Scrapling 기반) 어디에나 존재하는(Playwright를 통한 완벽한 JS 지원) 하이브리드 웹 스크래핑 엔진입니다.

## 특징
- **Static First 전략 (L1 스캐너):** Scrapling을 활용하여 빠르고 메모리를 덜 차지하는 정적 HTTP 요청을 우선적으로 시도합니다.
- **동적 렌더링 전환 (L2 렌더러):** 데이터가 숨겨져 있거나 클라이언트 측 JavaScript 렌더링(SPA)이 필요한 경우에 한하여 Playwright 엔진을 구동합니다.
- **최적화된 브라우징:** 이미지, 미디어, 폰트, 트래커 등 불필요한 리소스 로드를 차단하여 성능을 극대화합니다.
- **Stealth 모드:** Bot 탐지를 우회하기 위한 핑거프린트 변조 기능이 포함되어 있습니다.
- **웹 UI:** FastAPI 기반 웹 서버로 브라우저에서 바로 스크래핑 결과를 확인할 수 있습니다.

## 설치 방법
```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows의 경우: .\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
playwright install
```

## 웹 UI 실행 방법

```bash
uvicorn web.app:app --reload --port 8000
```

브라우저에서 `http://localhost:8000` 에 접속하면 아래와 같이 사용할 수 있습니다.

1. **URL 입력** — 스크래핑할 주소를 입력합니다. (`http://`, `https://` 필수)
2. **스크래핑 시작** 버튼 클릭 (또는 Enter)
3. **결과 확인:**
   - 상단의 엔진 배지(`L1` / `L2`)로 어떤 엔진이 사용되었는지 확인 가능
   - **HTML 원문** 탭: 수집된 HTML 소스를 코드 형태로 확인 및 클립보드 복사
   - **렌더링 미리보기** 탭: 수집된 HTML을 정적으로 렌더링하여 화면으로 확인

> **참고:** L2(Playwright) 렌더링이 필요한 페이지는 처리에 수 초~수십 초가 걸릴 수 있으며, 최대 60초 타임아웃이 적용됩니다.

## Python 코드에서 직접 사용

```python
import asyncio
from aether.core import AetherEngine

async def main():
    engine = AetherEngine(headless=True)
    result = await engine.fetch("https://example.com")
    print(f"엔진: {result['engine']}, 상태: {result['status_code']}")
    print(result['html'][:500])

asyncio.run(main())
```

## 디렉토리 구조
- `aether/`: Aether 핵심 엔진 코드가 위치합니다.
- `web/`: FastAPI 웹 서버(`app.py`) 및 프론트엔드(`static/index.html`)가 위치합니다.
- `docs/`: 엔진 내부 아키텍처 및 상세 로직 설명 문서가 포함되어 있습니다.
- `examples/`: 엔진 테스트 및 활용 예제 코드입니다.
