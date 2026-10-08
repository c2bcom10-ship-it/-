"""네이버 밴드에 오늘의 글을 올리는 프로그램.

글을 고르는 순서 (한국 시간 기준):
  1. 글/2026-10-10.txt 처럼 오늘 날짜 파일이 있으면 그 글
  2. 없으면 글/월요일.txt 처럼 오늘 요일 파일
  파일이 없거나 비어 있으면 그날은 올리지 않아요.

글의 첫 줄이 [알림] 이면 회원들 휴대폰에 푸시 알림도 보내요.

사용법:
  python post.py              오늘 글 올리기
  python post.py --dry-run    올리지 않고 어떤 글이 올라갈지만 보기
  python post.py --list-bands 내 밴드 목록과 band_key 보기
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://openapi.band.us"
KST = timezone(timedelta(hours=9))
WEEKDAYS = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
POSTS_DIR = Path(__file__).parent / "글"
PUSH_MARK = "[알림]"


def call(method, path, token, params=None):
    url = f"{API}{path}?" + urllib.parse.urlencode({"access_token": token})
    data = None
    if method == "POST":
        data = urllib.parse.urlencode(params or {}).encode()
    elif params:
        url += "&" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, method=method)
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if body.get("result_code") != 1:
        sys.exit(f"❌ 밴드가 오류를 알려왔어요: {json.dumps(body, ensure_ascii=False)}")
    return body["result_data"]


def todays_post(now):
    for name in (now.strftime("%Y-%m-%d"), WEEKDAYS[now.weekday()]):
        path = POSTS_DIR / f"{name}.txt"
        if path.exists():
            text = path.read_text(encoding="utf-8").strip()
            if text:
                return path.name, text
    return None, ""


def main():
    args = sys.argv[1:]
    token = os.environ.get("BAND_ACCESS_TOKEN", "").strip()
    band_key = os.environ.get("BAND_KEY", "").strip()

    if "--list-bands" in args:
        if not token:
            sys.exit("❌ BAND_ACCESS_TOKEN 이 비어 있어요.")
        for band in call("GET", "/v2.1/bands", token)["bands"]:
            print(f"{band['name']}  (회원 {band.get('member_count', '?')}명)  band_key: {band['band_key']}")
        return

    now = datetime.now(KST)
    file_name, text = todays_post(now)
    print(f"📅 오늘: {now:%Y-%m-%d} {WEEKDAYS[now.weekday()]}")
    if not text:
        print("😴 오늘 올릴 글이 없어요. (파일이 없거나 비어 있음)")
        return

    do_push = text.startswith(PUSH_MARK)
    if do_push:
        text = text[len(PUSH_MARK):].strip()
    print(f"📄 고른 파일: {file_name}   🔔 알림: {'보냄' if do_push else '안 보냄'}")
    print("-" * 30 + f"\n{text}\n" + "-" * 30)

    if "--dry-run" in args:
        print("🧪 연습 모드라서 실제로 올리지는 않았어요.")
        return
    if not token or not band_key:
        sys.exit("❌ BAND_ACCESS_TOKEN 또는 BAND_KEY 가 비어 있어요. 설명서의 3단계를 확인해 주세요.")

    result = call("POST", "/v2.2/band/post/create", token, {
        "band_key": band_key,
        "content": text,
        "do_push": "true" if do_push else "false",
    })
    print(f"✅ 글을 올렸어요! (post_key: {result.get('post_key')})")


if __name__ == "__main__":
    main()
