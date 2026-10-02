"""작업이 끝났거나 내 입력을 기다릴 때 폰으로 알려줘요.
Claude Code는 정보를 stdin으로, Codex(notify 설정)는 첫 번째 인자로 넘겨줘요."""
import json
import sys

import common


def main():
    cfg = common.load()
    if not common.active(cfg):
        return
    if len(sys.argv) > 1:  # Codex
        event = json.loads(sys.argv[1])
        common.publish(cfg, f"🤖 {cfg['pc_name']} Codex 작업 끝",
                       (event.get("last-assistant-message") or "완료")[:800], tags=["robot"])
        return
    event = json.load(sys.stdin)
    if event.get("hook_event_name") == "Stop":
        common.publish(cfg, f"✅ {cfg['pc_name']} Claude 작업 끝",
                       event.get("cwd", "") or "완료", tags=["white_check_mark"])
    else:
        common.publish(cfg, f"🔔 {cfg['pc_name']} Claude가 기다리는 중",
                       event.get("message", "확인이 필요해요"), priority=4, tags=["bell"])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
