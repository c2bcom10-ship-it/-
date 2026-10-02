---
name: setup
description: 폰으로 승인하기 처음 설정. 사용자가 "폰 승인 설정", "phone-approve 설정", "폰으로 승인받고 싶어"라고 하면 사용해요.
---

# 폰으로 승인하기 — 처음 설정

사용자는 초보자예요. 한국어로, 한 단계씩 짧고 쉽게 안내하세요.

1. 파이썬이 있는지 확인해요: `python3 --version` 을 실행하고, 안 되면 `python --version` 을 실행해요.
   - 둘 다 없으면 설치를 도와주세요. Windows는 `winget install -e --id Python.Python.3.12` (설치 후 Claude Code를 다시 켜야 해요), Mac은 `xcode-select --install`. 설치가 끝나면 이 단계를 다시 해요.
   - 이후 명령에서는 되는 쪽(`python3` 또는 `python`)을 쓰세요.
2. 설정을 실행해요:
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ctl.py" setup
   ```
3. 출력에 나온 **채널 이름**을 사용자에게 크게 보여주고, 폰에서 할 일을 안내해요:
   - 'ntfy' 앱 설치 (아이폰: App Store, 안드로이드: Play 스토어)
   - 앱에서 [+] → 채널 이름 입력 → Subscribe
   - "🎉 연결 성공!" 알림이 오면 완료 (구독 전에 보낸 알림은 안 보일 수 있으니, 구독 후 다시 확인하려면 `ctl.py setup` 을 한 번 더 실행해요)
4. Codex도 쓰는지 물어보고, 쓴다고 하면 실행해요:
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ctl.py" codex
   ```
5. 마지막으로 이렇게 알려주세요:
   - 나갈 때: `/phone-approve:on` (외출 모드 — 승인 요청이 폰으로 가요)
   - 돌아오면: `/phone-approve:off` (집 모드 — 평소처럼 PC에서 승인)
   - 지금은 외출 모드가 켜져 있어요.
