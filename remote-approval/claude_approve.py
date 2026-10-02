"""Claude Code 'PermissionRequest' 훅.

Claude Code가 "이거 해도 돼요?" 승인창을 띄우려는 순간 이 파일이 실행돼요.
텔레그램으로 [허용] [거부] 버튼을 보내고, 휴대폰에서 누른 답을 Claude Code에 돌려줘요.
"""
import json
import sys
import time
import uuid

from tg_common import STATE_DIR, api, load_config, send

RESULTS = STATE_DIR / "results"
OFFSET_FILE = STATE_DIR / "offset.txt"


def describe(event):
    tool = event.get("tool_name", "?")
    inp = event.get("tool_input", {}) or {}
    if tool == "Bash":
        detail = inp.get("command", "")
    elif tool in ("Edit", "Write", "MultiEdit", "NotebookEdit", "Read"):
        detail = inp.get("file_path") or inp.get("notebook_path", "")
    elif tool in ("WebFetch", "WebSearch"):
        detail = inp.get("url") or inp.get("query", "")
    else:
        detail = json.dumps(inp, ensure_ascii=False)
    return tool, detail[:1500]


def poll_once(cfg):
    """텔레그램에서 새 버튼 클릭을 가져와 results 폴더에 저장해요.

    승인 요청이 여러 개 동시에 와도 서로 답을 빼앗지 않도록,
    받은 답은 모두 파일로 저장한 뒤에 다음 위치(offset)로 넘어가요.
    """
    try:
        offset = int(OFFSET_FILE.read_text())
    except (OSError, ValueError):
        offset = 0
    updates = api(cfg, "getUpdates",
                  {"offset": offset, "timeout": 20, "allowed_updates": ["callback_query"]}, timeout=30)
    for u in updates:
        cq = u.get("callback_query")
        if not cq:
            continue
        # 보안: 내 채팅방에서 누른 버튼만 인정해요
        if str(cq.get("message", {}).get("chat", {}).get("id")) != cfg["chat_id"]:
            continue
        req_id, _, answer = (cq.get("data") or "").partition(":")
        if req_id and answer in ("allow", "deny"):
            (RESULTS / f"{req_id}.txt").write_text(answer)
        try:
            api(cfg, "answerCallbackQuery", {"callback_query_id": cq["id"]})
        except Exception:
            pass
    if updates:
        OFFSET_FILE.write_text(str(updates[-1]["update_id"] + 1))


def output(behavior, reason=None):
    decision = {"behavior": behavior}
    if reason:
        decision["reason"] = reason
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": decision}}))


def main():
    event = json.load(sys.stdin)
    cfg = load_config()
    if not cfg["bot_token"] or not cfg["chat_id"]:
        return  # 설정 전이면 아무것도 안 하고 원래 승인창을 띄워요
    RESULTS.mkdir(parents=True, exist_ok=True)

    tool, detail = describe(event)
    req_id = uuid.uuid4().hex[:12]
    text = (f"🔐 [{cfg['pc_name']}] Claude 승인 요청\n"
            f"📁 {event.get('cwd', '')}\n"
            f"🛠 {tool}\n\n{detail}")
    msg = send(cfg, text, [[{"text": "✅ 허용", "callback_data": f"{req_id}:allow"},
                            {"text": "❌ 거부", "callback_data": f"{req_id}:deny"}]])

    result_file = RESULTS / f"{req_id}.txt"
    deadline = time.time() + int(cfg["timeout_seconds"])
    answer = None
    while time.time() < deadline:
        if result_file.exists():
            answer = result_file.read_text().strip()
            result_file.unlink(missing_ok=True)
            break
        try:
            poll_once(cfg)
        except Exception:
            time.sleep(3)  # 인터넷이 잠깐 끊겨도 다시 시도해요

    label = {"allow": "✅ 허용함", "deny": "❌ 거부함"}.get(answer, "⏰ 시간 초과")
    try:
        api(cfg, "editMessageText", {"chat_id": cfg["chat_id"], "message_id": msg["message_id"],
                                     "text": f"{text}\n\n→ {label}"[:4000]})
    except Exception:
        pass

    if answer == "allow":
        output("allow")
    elif answer == "deny":
        output("deny", "휴대폰에서 거부했어요")
    elif cfg["on_timeout"] == "deny":
        output("deny", "휴대폰 응답 시간이 지나서 거부했어요")
    # on_timeout == "ask": 아무것도 출력하지 않으면 PC의 원래 승인창이 떠요


if __name__ == "__main__":
    main()
