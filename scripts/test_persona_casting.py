#!/usr/bin/env python3
"""
Persona Casting Query 테스트 스크립트

castingQuery를 직접 넣어서 DB에서 어떤 persona가 매칭되는지 확인합니다.

사용법:
  # .env 파일 설정 후
  python scripts/test_persona_casting.py "환불 지연에 분노한 고객 고객이 3일 이상 환불 지연에 화를 내며 에스컬레이션을 요구하는 상황"

  # 여러 쿼리 비교
  python scripts/test_persona_casting.py --compare \
    "환불 지연에 분노한 고객" \
    "기술에 서툰 60대 사용자가 앱 결제에서 반복 실패"

  # admin preset만 조회
  python scripts/test_persona_casting.py --scope admin "환불 지연에 분노한 고객"

  # project persona도 함께 조회
  python scripts/test_persona_casting.py --scope both --project-id <uuid> "환불 지연에 분노한 고객"

필요한 환경변수 (.env):
  SUPABASE_URL=https://xxx.supabase.co
  SUPABASE_SERVICE_ROLE_KEY=eyJ...
  OPENAI_API_KEY=sk-...
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import httpx
except ImportError:
    sys.exit("httpx 필요: pip install httpx")

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# ─── Config ───────────────────────────────────────────────────────────

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
DEFAULT_LIMIT = 10


def load_env():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        env_path = Path(__file__).parent.parent / ".env"
    if load_dotenv and env_path.exists():
        load_dotenv(env_path)

    required = ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "OPENAI_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        print(f"누락된 환경변수: {', '.join(missing)}")
        print(f".env 파일 위치: {env_path}")
        sys.exit(1)

    return {
        "supabase_url": os.getenv("SUPABASE_URL").rstrip("/"),
        "supabase_key": os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        "openai_key": os.getenv("OPENAI_API_KEY"),
    }


# ─── Embedding ────────────────────────────────────────────────────────

def embed_text(text: str, *, openai_key: str) -> list[float]:
    resp = httpx.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": EMBEDDING_MODEL,
            "input": text.strip(),
            "dimensions": EMBEDDING_DIMENSIONS,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()["data"][0]["embedding"]


def vector_literal(vector: list[float]) -> str:
    return "[" + ",".join(f"{v:.8f}" for v in vector) + "]"


# ─── Supabase RPC ────────────────────────────────────────────────────

def call_rpc(*, supabase_url: str, supabase_key: str, function: str, params: dict) -> list[dict]:
    resp = httpx.post(
        f"{supabase_url}/rest/v1/rpc/{function}",
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
        },
        json=params,
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"RPC 에러 ({resp.status_code}): {resp.text[:500]}")
        sys.exit(1)
    return resp.json()


def fetch_admin_candidates(*, supabase_url, supabase_key, query_vector, limit, language=None):
    params = {
        "p_query_embedding": vector_literal(query_vector),
        "p_exclude_ids": [],
        "p_project_candidate_ids": [],
        "p_limit": limit,
    }
    if language:
        params["p_language"] = language
    return call_rpc(
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        function="retrieve_admin_template_persona_candidates",
        params=params,
    )


def fetch_project_candidates(*, supabase_url, supabase_key, query_vector, project_id, limit, language=None):
    params = {
        "p_project_id": project_id,
        "p_query_embedding": vector_literal(query_vector),
        "p_exclude_ids": [],
        "p_limit": limit,
    }
    if language:
        params["p_language"] = language
    return call_rpc(
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        function="retrieve_project_persona_candidates",
        params=params,
    )


# ─── Display ──────────────────────────────────────────────────────────

def display_results(query: str, rows: list[dict], *, source: str = ""):
    print(f"\n{'='*70}")
    print(f"castingQuery: \"{query}\"")
    if source:
        print(f"source: {source}")
    print(f"결과: {len(rows)}건")
    print(f"{'='*70}")

    if not rows:
        print("  (매칭된 persona 없음)")
        return

    for i, row in enumerate(rows, 1):
        score = row.get("vector_score", 0)
        name = row.get("name", "?")
        p_type = row.get("type", "?")
        desc = (row.get("searchable_description") or "")[:120]

        # attributes에서 주요 정보 추출
        attrs = row.get("attributes") or {}
        difficulty = attrs.get("difficulty", "?")
        tech = attrs.get("tech_familiarity", attrs.get("techFamiliarity", "?"))
        occupation = attrs.get("occupation", "?")
        verticals = attrs.get("vertical", [])
        capabilities = attrs.get("capability", [])

        bar = "█" * int(score * 30) + "░" * (30 - int(score * 30))
        print(f"\n  #{i}  {name} ({p_type})")
        print(f"      vector_score: {score:.4f}  {bar}")
        print(f"      difficulty: {difficulty} | tech: {tech} | occupation: {occupation}")
        if verticals:
            print(f"      vertical: {', '.join(verticals[:3])}")
        if capabilities:
            print(f"      capability: {', '.join(capabilities[:3])}")
        if desc:
            print(f"      desc: {desc}...")

    # 점수 분포 요약
    scores = [r.get("vector_score", 0) for r in rows]
    print(f"\n  --- 점수 분포 ---")
    print(f"  max: {max(scores):.4f} | min: {min(scores):.4f} | avg: {sum(scores)/len(scores):.4f}")


def display_comparison(queries: list[str], all_results: list[list[dict]]):
    """여러 쿼리 결과를 나란히 비교"""
    print(f"\n{'='*70}")
    print(f"비교 모드: {len(queries)}개 쿼리")
    print(f"{'='*70}")

    # 모든 persona ID 수집
    all_personas = {}
    for rows in all_results:
        for row in rows:
            pid = row.get("id")
            if pid and pid not in all_personas:
                all_personas[pid] = row.get("name", "?")

    # 비교 테이블
    header = f"{'Persona':<25}"
    for i, q in enumerate(queries):
        header += f" | Q{i+1} score"
    print(f"\n{header}")
    print("-" * len(header))

    for pid, name in all_personas.items():
        line = f"{name[:24]:<25}"
        for results in all_results:
            score = next((r["vector_score"] for r in results if r.get("id") == pid), None)
            if score is not None:
                line += f" | {score:.4f}  "
            else:
                line += f" |    -    "
        print(line)

    print(f"\n쿼리 목록:")
    for i, q in enumerate(queries):
        print(f"  Q{i+1}: \"{q}\"")


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Persona casting query 테스트")
    parser.add_argument("queries", nargs="+", help="castingQuery 텍스트 (여러 개 가능)")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"결과 수 (default: {DEFAULT_LIMIT})")
    parser.add_argument("--scope", choices=["admin", "project", "both"], default="admin",
                        help="검색 범위 (default: admin)")
    parser.add_argument("--project-id", help="project scope 검색 시 project ID")
    parser.add_argument("--language", default=None, help="언어 필터 (ko, en 등)")
    parser.add_argument("--compare", action="store_true", help="여러 쿼리 결과를 비교 테이블로 표시")
    parser.add_argument("--json", action="store_true", help="결과를 JSON으로 출력")
    args = parser.parse_args()

    if args.scope in ("project", "both") and not args.project_id:
        sys.exit("--scope project/both 사용 시 --project-id 필요")

    env = load_env()

    all_results = []
    for query in args.queries:
        print(f"\n⏳ embedding 중: \"{query[:50]}...\"" if len(query) > 50 else f"\n⏳ embedding 중: \"{query}\"")
        query_vector = embed_text(query, openai_key=env["openai_key"])

        rows = []

        if args.scope in ("admin", "both"):
            admin_rows = fetch_admin_candidates(
                supabase_url=env["supabase_url"],
                supabase_key=env["supabase_key"],
                query_vector=query_vector,
                limit=args.limit,
                language=args.language,
            )
            for r in admin_rows:
                r["_source"] = "admin"
            rows.extend(admin_rows)

        if args.scope in ("project", "both"):
            project_rows = fetch_project_candidates(
                supabase_url=env["supabase_url"],
                supabase_key=env["supabase_key"],
                query_vector=query_vector,
                project_id=args.project_id,
                limit=args.limit,
                language=args.language,
            )
            for r in project_rows:
                r["_source"] = "project"
            rows.extend(project_rows)

        # vector_score 내림차순 정렬
        rows.sort(key=lambda r: r.get("vector_score", 0), reverse=True)
        all_results.append(rows)

        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        elif not args.compare:
            display_results(query, rows, source=args.scope)

    if args.compare and not args.json:
        display_comparison(args.queries, all_results)


if __name__ == "__main__":
    main()
