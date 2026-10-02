"""phone-approve 조종 스크립트.

  python3 ctl.py setup    처음 설정 (내 전용 알림 채널 만들기 + 테스트 알림)
  python3 ctl.py on       외출 모드 켜기 (승인 요청과 알림이 폰으로 와요)
  python3 ctl.py off      집 모드 (평소처럼 PC 화면에서 승인)
  python3 ctl.py status   지금 상태 보기
  python3 ctl.py codex    Codex에도 연결 (작업 끝 알림 + 승인창 줄이기)
"""
import re
import secrets
import shutil
import sys
from pathlib import Path

import common

HERE = Path(__file__).resolve().parent


def show_subscribe(cfg):
    print("📱 폰에서 할 일 (처음 한 번만):")
    print("  1. 앱스토어/플레이스토어에서 'ntfy' 앱을 설치해요.")
    print("  2. 앱에서 [+] 버튼 → 아래 채널 이름을 그대로 입력 → Subscribe(구독)")
    print(f"\n     채널 이름:  {cfg['topic']}\n")
    if cfg["server"] != "https://ntfy.sh":
        print(f"     (서버 주소를 {cfg['server']} 로 바꿔서 구독하세요)")
    print("  ⚠️ 채널 이름은 비밀번호처럼 다른 사람에게 알려주지 마세요.")


def setup(cfg):
    if not cfg["topic"]:
        cfg["topic"] = "pa-" + secrets.token_hex(10)
    cfg["away"] = True
    common.save(cfg)
    try:
        common.publish(cfg, "🎉 연결 성공!", "이제 PC의 승인 요청이 여기로 와요.", tags=["tada"])
        print("✅ 테스트 알림을 보냈어요.")
    except Exception as e:
        print(f"❗ 알림을 보내지 못했어요 (인터넷 연결 확인): {e}")
    show_subscribe(cfg)
    print("\n🟢 외출 모드가 켜졌어요. 집에 오면 /phone-approve:off 로 끄세요.")


def set_away(cfg, on):
    if not cfg["topic"]:
        sys.exit("❗ 아직 설정 전이에요. 먼저 /phone-approve:setup 을 실행하세요.")
    cfg["away"] = on
    common.save(cfg)
    if on:
        print("🟢 외출 모드 ON — 승인 요청과 작업 끝 알림이 폰으로 가요.")
    else:
        print("🏠 집 모드 — 평소처럼 PC 화면에서 승인해요. 폰 알림은 안 가요.")


def status(cfg):
    if not cfg["topic"]:
        print("아직 설정 전이에요. /phone-approve:setup 을 실행하세요.")
        return
    print("🟢 외출 모드 ON" if cfg["away"] else "🏠 집 모드 (OFF)")
    print(f"채널 이름: {cfg['topic']}   서버: {cfg['server']}")
    print(f"응답 대기: {cfg['timeout_seconds']}초, 시간 초과 시: "
          + ("거부" if cfg["on_timeout"] == "deny" else "PC 승인창 띄우기"))


def codex(cfg):
    if not cfg["topic"]:
        sys.exit("❗ 먼저 /phone-approve:setup 을 실행하세요.")
    # 플러그인이 업데이트돼도 경로가 안 바뀌게 고정된 곳에 복사해 둬요
    home = common.CONFIG_FILE.parent
    for f in ("notify.py", "common.py"):
        shutil.copy(HERE / f, home / f)
    notify_line = "notify = [{}, {}]".format(
        *(f'"{p}"' for p in (Path(sys.executable).as_posix(), (home / "notify.py").as_posix())))

    toml = Path.home() / ".codex" / "config.toml"
    toml.parent.mkdir(parents=True, exist_ok=True)
    text = toml.read_text(encoding="utf-8") if toml.exists() else ""
    if text:
        shutil.copy(toml, toml.with_suffix(".toml.backup"))
    added = []
    if re.search(r"(?m)^\s*notify\s*=", text):
        text = re.sub(r"(?m)^\s*notify\s*=.*$", notify_line.replace("\\", "\\\\"), text)
    else:
        added.append(notify_line)
    if not re.search(r"(?m)^\s*approval_policy\s*=", text):
        added.append('approval_policy = "on-request"')
    if not re.search(r"(?m)^\s*sandbox_mode\s*=", text):
        added.append('sandbox_mode = "workspace-write"')
    # 맨 위 설정은 [표] 보다 앞에 있어야 해서 파일 맨 앞에 넣어요
    if added:
        text = "# phone-approve가 추가함\n" + "\n".join(added) + "\n\n" + text
    toml.write_text(text, encoding="utf-8")
    print(f"✅ Codex 설정 완료: {toml}")
    print("   - 작업이 끝나면 폰으로 알림이 가요 (외출 모드일 때만)")
    print("   - 작업 폴더 안에서는 묻지 않고 진행해서 승인창이 줄어들어요")
    print("   Codex를 껐다가 다시 켜 주세요.")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    cfg = common.load()
    actions = {"setup": lambda: setup(cfg), "on": lambda: set_away(cfg, True),
               "off": lambda: set_away(cfg, False), "status": lambda: status(cfg),
               "codex": lambda: codex(cfg)}
    if cmd not in actions:
        sys.exit(__doc__)
    actions[cmd]()


if __name__ == "__main__":
    main()
