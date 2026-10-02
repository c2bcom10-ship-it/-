"""Claude Code가 승인창을 띄우려는 순간 실행돼요.
외출 모드면 폰으로 [허용] [거부] 버튼 알림을 보내고, 누른 답을 Claude Code에 돌려줘요."""
import json
import sys
import time
import uuid

import common


def describe(event):
    tool = event.get("tool_name", "?")
    inp = event.get("tool_input") or {}
    detail = (inp.get("command") or inp.get("file_path") or inp.get("url")
              or inp.get("query") or json.dumps(inp, ensure_ascii=False))
    return tool, str(detail)[:1500]


def decide(behavior, reason=None):
    d = {"behavior": behavior}
    if reason:
        d["reason"] = reason
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": d}}))


def main():
    event = json.load(sys.stdin)
    cfg = common.load()
    if not common.active(cfg):
        return  # 집 모드: 평소처럼 PC 화면에 승인창이 떠요

    tool, detail = describe(event)
    rid = uuid.uuid4().hex[:10]
    reply_url = f"{cfg['server'].rstrip('/')}/{common.reply_topic(cfg)}"
    started = time.time() - 5
    common.publish(
        cfg, f"🔐 {cfg['pc_name']} 승인 요청: {tool}",
        f"{detail}\n\n📁 {event.get('cwd', '')}",
        actions=[
            {"action": "http", "label": "✅ 허용", "url": reply_url, "method": "POST",
             "body": f"{rid}:allow", "clear": True},
            {"action": "http", "label": "❌ 거부", "url": reply_url, "method": "POST",
             "body": f"{rid}:deny", "clear": True},
        ],
        priority=5, tags=["lock"])

    deadline = time.time() + int(cfg["timeout_seconds"])
    while time.time() < deadline:
        try:
            for msg in common.poll_replies(cfg, started):
                if msg == f"{rid}:allow":
                    return decide("allow")
                if msg == f"{rid}:deny":
                    return decide("deny", "휴대폰에서 거부했어요")
        except Exception:
            pass  # 인터넷이 잠깐 끊겨도 계속 기다려요
        time.sleep(2)

    if cfg["on_timeout"] == "deny":
        decide("deny", "휴대폰 응답 시간이 지나서 거부했어요")
    # ask: 아무것도 출력하지 않으면 PC 화면에 원래 승인창이 떠요


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # 무슨 일이 있어도 Claude Code 작업을 망가뜨리지 않아요
