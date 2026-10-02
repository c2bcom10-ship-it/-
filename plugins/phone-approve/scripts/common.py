"""공통 코드: 설정 읽기/저장, ntfy로 알림 보내기 (파이썬 기본 기능만 사용)."""
import json
import platform
import urllib.request
from pathlib import Path

CONFIG_FILE = Path.home() / ".phone-approve" / "config.json"


def load():
    try:
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        cfg = {}
    cfg.setdefault("server", "https://ntfy.sh")
    cfg.setdefault("topic", "")
    cfg.setdefault("away", False)          # True = 외출 모드 (폰으로 승인/알림)
    cfg.setdefault("timeout_seconds", 540)
    cfg.setdefault("on_timeout", "ask")    # ask = PC 승인창으로 넘김, deny = 거부
    cfg.setdefault("pc_name", platform.node() or "PC")
    return cfg


def save(cfg):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def active(cfg):
    return bool(cfg["topic"]) and cfg["away"]


def reply_topic(cfg):
    return cfg["topic"] + "-reply"


def publish(cfg, title, message, actions=None, priority=3, tags=None):
    body = {"topic": cfg["topic"], "title": title, "message": message[:3500], "priority": priority}
    if actions:
        body["actions"] = actions
    if tags:
        body["tags"] = tags
    req = urllib.request.Request(cfg["server"].rstrip("/") + "/", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def poll_replies(cfg, since):
    """since(유닉스 시간) 이후에 폰에서 누른 버튼 답장들을 가져와요."""
    url = f"{cfg['server'].rstrip('/')}/{reply_topic(cfg)}/json?poll=1&since={int(since)}"
    with urllib.request.urlopen(url, timeout=15) as r:
        lines = r.read().decode().splitlines()
    out = []
    for line in lines:
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if m.get("event") == "message":
            out.append(m.get("message", ""))
    return out
