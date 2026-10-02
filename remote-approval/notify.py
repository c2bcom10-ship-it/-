"""작업이 끝났거나 내 입력을 기다릴 때 텔레그램으로 알려주는 훅.

- Claude Code: Stop / Notification 훅에서 실행 (정보가 stdin으로 들어와요)
- Codex: config.toml의 notify에서 실행 (정보가 첫 번째 인자로 들어와요)
"""
import json
import sys

from tg_common import load_config, send


def main():
    cfg = load_config()
    if not cfg["bot_token"] or not cfg["chat_id"]:
        return
    if len(sys.argv) > 1:  # Codex
        event = json.loads(sys.argv[1])
        last = (event.get("last-assistant-message") or "")[:800]
        text = f"🤖 [{cfg['pc_name']}] Codex 작업 끝\n\n{last}"
    else:  # Claude Code
        event = json.load(sys.stdin)
        name = event.get("hook_event_name")
        if name == "Stop":
            text = f"✅ [{cfg['pc_name']}] Claude 작업 끝\n📁 {event.get('cwd', '')}"
        else:
            text = f"🔔 [{cfg['pc_name']}] Claude: {event.get('message', '확인이 필요해요')}"
    send(cfg, text)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # 알림이 실패해도 작업은 멈추지 않게 해요
