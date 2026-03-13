# Aether 하이브리드 스크래핑 아키텍처

이 문서는 Aether 엔진의 설계 철학과 L1/L2 전환 로직 구조를 설명합니다.

## 핵심 개념: Static First
대규모 데이터 수집 시, 모든 요청을 브라우저 렌더링으로 처리하면 리소스(메모리, CPU)가 급격히 고갈됩니다. Aether는 이를 해결하기 위해 **Scrapling (L1 스캐너)**을 우선적으로 사용하여 가벼운 비동기 HTTP 요청을 날립니다. 이후 데이터를 확인하고, 필요한 경우에만 **Playwright (L2 렌더러)**를 띄우는 하이브리드 방식을 채택합니다.

## 시스템 흐름 (Flow)
1. **사용자 요청:** `AetherEngine.fetch(url)` 호출
2. **L1 Scanner (Scrapling) 동작:** 
   - HTTP GET 요청 수행
   - 반환된 HTML 파싱
   - 특정 지표 (예: "Enable JavaScript" 메시지, 캡차 등) 확인
3. **분기점 (Switch Switcher):**
   - 데이터 추출이 가능하면 **L1 결과 반환 후 종료**.
   - JS 렌더링이 필수적이라고 판단되면 **L2로 전환**.
4. **L2 Renderer (Playwright) 동작:**
   - L1에서 얻은 세션/쿠키를 Playwright 컨텍스트에 주입
   - Stealth 모드를 적용하여 탐지 우회
   - 불필요 리소스(이미지, CSS 등)를 차단하여 빠른 렌더링
   - 결과(DOM, 데이터) 반환

## 주요 컴포넌트
- **core.py**: L1과 L2를 제어하고 요청을 라우팅하는 메인 엔진부
- **l1_scanner.py**: Scrapling 기반 정적 요청 및 판별 로직
- **l2_renderer.py**: Playwright 기반 동적 렌더링 및 Stealth 환경 구성
