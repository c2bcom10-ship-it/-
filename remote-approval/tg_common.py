"""텔레그램 봇과 대화하는 공통 코드 (파이썬 기본 기능만 사용, 설치할 것 없음)."""
import json
import os
import platform
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_FILE = HERE / "config.json"
STATE_DIR = Path.home() / ".remote-approval"


def load_config():
    """config.json 또는 환경변수에서 봇 토큰과 채팅 ID를 읽어요."""
    cfg = {}
    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    cfg["bot_token"] = os.environ.get("TG_BOT_TOKEN", cfg.get("bot_token", ""))
    cfg["chat_id"] = str(os.environ.get("TG_CHAT_ID", cfg.get("chat_id", "")))
    cfg.setdefault("timeout_seconds", 540)
    # 시간 안에 답이 없으면: "ask" = PC 화면의 원래 승인창으로 넘김, "deny" = 거부
    cfg.setdefault("on_timeout", "ask")
    cfg.setdefault("pc_name", platform.node() or "PC")
    return cfg


def api(cfg, method, params=None, timeout=40):
    url = f"https://api.telegram.org/bot{cfg['bot_token']}/{method}"
    data = urllib.parse.urlencode(
        {k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in (params or {}).items()}
    ).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=timeout) as r:
        body = json.loads(r.read().decode())
    if not body.get("ok"):
        raise RuntimeError(body)
    return body["result"]


def send(cfg, text, buttons=None):
    params = {"chat_id": cfg["chat_id"], "text": text[:4000]}
    if buttons:
        params["reply_markup"] = {"inline_keyboard": buttons}
    return api(cfg, "sendMessage", params)
