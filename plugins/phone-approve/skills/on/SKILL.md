---
name: on
description: 외출 모드 켜기. 승인 요청과 작업 끝 알림을 폰으로 보내요. 사용자가 "외출 모드", "폰 승인 켜줘", "나갈게"라고 하면 사용해요.
---

다음을 실행하고 결과를 한국어로 짧게 알려주세요. (`python3`가 없으면 `python`으로)

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ctl.py" on
```

"설정 전"이라고 나오면 `/phone-approve:setup` 을 먼저 하자고 안내하세요.
