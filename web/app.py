import asyncio
import re
import sys
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 프로젝트 루트를 파이썬 경로에 추가하여 aether 패키지 임포트 가능하게 함
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aether.core import AetherEngine

# --- 앱 초기화 ---
app = FastAPI(
    title="Aether 웹 스크래퍼",
    description="Aether 하이브리드 스크래핑 엔진을 웹에서 조작하는 인터페이스",
    version="0.1.0"
)

# 정적 파일 디렉토리 마운트 (/static → web/static/)
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 엔진 인스턴스 (앱 수명 동안 재사용)
_engine: AetherEngine | None = None

def get_engine() -> AetherEngine:
    global _engine
    if _engine is None:
        _engine = AetherEngine(headless=True)
    return _engine


# --- 요청/응답 스키마 ---

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    success: bool
    url: str
    engine: str | None = None
    status_code: int | None = None
    html: str | None = None
    error: str | None = None


# --- URL 유효성 검사 (SSRF 방지) ---
# http/https 프로토콜만 허용, 로컬호스트 및 내부 IP 대역 차단

_INTERNAL_PATTERNS = re.compile(
    r"^https?://"
    r"(localhost|127\.\d+\.\d+\.\d+|0\.0\.0\.0"
    r"|10\.\d+\.\d+\.\d+"
    r"|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+"
    r"|192\.168\.\d+\.\d+"
    r"|::1|fd[0-9a-f]{2}:)",
    re.IGNORECASE
)

def _validate_url(url: str) -> None:
    """URL 형식 및 허용 범위를 검증합니다. 잘못된 경우 HTTPException을 발생시킵니다."""
    if not url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="URL은 http:// 또는 https:// 로 시작해야 합니다."
        )
    if _INTERNAL_PATTERNS.match(url):
        raise HTTPException(
            status_code=400,
            detail="내부 네트워크 주소는 스크래핑 대상으로 허용되지 않습니다."
        )


# --- 라우트 ---

@app.get("/", response_class=FileResponse, include_in_schema=False)
async def root():
    """프론트엔드 HTML 반환"""
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(req: ScrapeRequest):
    """
    URL을 받아 Aether 엔진으로 스크래핑한 결과를 반환합니다.
    - L1(Scrapling) 우선 → 필요 시 L2(Playwright) 자동 전환
    - 최대 대기 시간: 60초
    """
    _validate_url(req.url)

    engine = get_engine()

    try:
        result = await asyncio.wait_for(engine.fetch(req.url), timeout=60.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="요청 시간이 초과되었습니다 (60초). 다시 시도해 주세요.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"스크래핑 중 오류가 발생했습니다: {str(e)}")

    return ScrapeResponse(
        success=result.get("success", False),
        url=result.get("url", req.url),
        engine=result.get("engine"),
        status_code=result.get("status_code"),
        html=result.get("html", ""),
        error=result.get("error"),
    )
