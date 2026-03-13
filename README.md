# Aether (에테르) 🌬️

Aether는 공기처럼 가볍지만(Scrapling 기반) 어디에나 존재하는(Playwright를 통한 완벽한 JS 지원) 하이브리드 웹 스크래핑 엔진입니다.

## 특징
- **Static First 전략 (L1 스캐너):** Scrapling을 활용하여 빠르고 메모리를 덜 차지하는 정적 HTTP 요청을 우선적으로 시도합니다.
- **동적 렌더링 전환 (L2 렌더러):** 데이터가 숨겨져 있거나 클라이언트 측 JavaScript 렌더링(SPA)이 필요한 경우에 한하여 Playwright 엔진을 구동합니다.
- **최적화된 브라우징:** 이미지, 미디어, 폰트, 트래커 등 불필요한 리소스 로드를 차단하여 성능을 극대화합니다.
- **Stealth 모드:** Bot 탐지를 우회하기 위한 핑거프린트 변조 기능이 포함되어 있습니다.

## 설치 방법
```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows의 경우: .\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
playwright install
```

## 디렉토리 구조
- `aether/`: Aether 핵심 엔진 코드가 위치합니다.
- `docs/`: 엔진 내부 아키텍처 및 상세 로직 설명 문서가 포함되어 있습니다.
- `examples/`: 엔진 테스트 및 활용 예제 코드입니다.
