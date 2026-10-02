"""처음 한 번만 실행하는 설치 도우미.

1) 텔레그램 봇 토큰 입력  2) 내 채팅 ID 자동으로 찾기  3) 테스트 메시지 보내기
4) Claude Code 설정(~/.claude/settings.json)에 훅 자동 등록 (기존 파일은 백업)
"""
import json
import shutil
import sys
import time
from pathlib import Path

from tg_common import CONFIG_FILE, HERE, api, send

CLAUDE_SETTINGS = Path.home() / ".claude" / "settings.json"


def cmd(script):
    return f'"{sys.executable}" "{HERE / script}"'


def find_chat_id(cfg):
    print("\n👉 휴대폰 텔레그램에서 방금 만든 봇을 찾아 아무 메시지(예: 안녕)나 보내 주세요.")
    print("   기다리는 중... (2분)")
    deadline = time.time() + 120
    while time.time() < deadline:
        for u in api(cfg, "getUpdates", {"timeout": 20}, timeout=30):
            chat = (u.get("message") or {}).get("chat")
            if chat:
                api(cfg, "getUpdates", {"offset": u["update_id"] + 1, "timeout": 0})
                return str(chat["id"])
    sys.exit("❗ 메시지를 못 받았어요. 봇에게 메시지를 보낸 뒤 다시 실행해 주세요.")


def install_claude_hooks():
    CLAUDE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    settings = {}
    if CLAUDE_SETTINGS.exists():
        backup = CLAUDE_SETTINGS.with_suffix(".json.backup")
        shutil.copy(CLAUDE_SETTINGS, backup)
        print(f"📦 기존 설정을 백업했어요: {backup}")
        settings = json.loads(CLAUDE_SETTINGS.read_text(encoding="utf-8") or "{}")

    hooks = settings.setdefault("hooks", {})
    ours = {
        "PermissionRequest": {"matcher": "*", "hooks": [
            {"type": "command", "command": cmd("claude_approve.py"), "timeout": 600}]},
        "Notification": {"matcher": "idle_prompt", "hooks": [
            {"type": "command", "command": cmd("notify.py")}]},
        "Stop": {"hooks": [{"type": "command", "command": cmd("notify.py")}]},
    }
    for event, entry in ours.items():
        # 다시 실행해도 같은 훅이 두 번 들어가지 않게 예전 것을 지워요
        kept = [e for e in hooks.get(event, [])
                if not any(str(HERE) in h.get("command", "") for h in e.get("hooks", []))]
        hooks[event] = kept + [entry]
    CLAUDE_SETTINGS.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Claude Code 훅을 등록했어요: {CLAUDE_SETTINGS}")


def main():
    cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8")) if CONFIG_FILE.exists() else {}
    if not cfg.get("bot_token"):
        cfg["bot_token"] = input("🤖 BotFather가 알려준 봇 토큰을 붙여넣고 Enter: ").strip()
    print("봇 확인:", api(cfg, "getMe")["username"])
    if not cfg.get("chat_id"):
        cfg["chat_id"] = find_chat_id(cfg)
    cfg.setdefault("timeout_seconds", 540)
    cfg.setdefault("on_timeout", "ask")
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"💾 설정 저장: {CONFIG_FILE}")
    send(cfg, "🎉 연결 성공! 이제 PC의 승인 요청이 여기로 와요.")
    print("📱 휴대폰에 테스트 메시지를 보냈어요.")

    if input("\nClaude Code에 자동 등록할까요? (y/n): ").strip().lower() == "y":
        install_claude_hooks()
    print("\n🔔 Codex 알림을 쓰려면 codex/config.toml 안내를 보세요. 아래 줄을 쓰면 돼요:")
    print(f'   notify = [{json.dumps(sys.executable)}, {json.dumps(str(HERE / "notify.py"))}]')
    print("\n끝! Claude Code를 껐다가 다시 켜 주세요.")


if __name__ == "__main__":
    main()
