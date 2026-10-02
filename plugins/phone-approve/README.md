# 📱 폰으로 승인하기 (phone-approve)

밖에 있을 때 PC의 Claude Code가 **"이거 해도 돼요?"** 하고 멈추면,
폰에 알림이 와서 **[✅ 허용] [❌ 거부]** 버튼만 누르면 돼요.

## 설치 (딱 3줄)

PC의 Claude Code 안에서 한 줄씩 입력하세요.

```
/plugin marketplace add c2bcom10-ship-it/-
/plugin install phone-approve@c2b-tools
/phone-approve:setup
```

그다음은 Claude가 알아서 안내해요. 폰에서 할 일은 이것뿐이에요.
1. **ntfy** 앱 설치 (무료, 가입 필요 없음)
2. 앱의 **[+]** 버튼 → Claude가 알려준 **채널 이름** 입력 → Subscribe

## 사용법

| 상황 | 입력 |
|---|---|
| 🚶 나갈 때 | `/phone-approve:on` |
| 🏠 돌아왔을 때 | `/phone-approve:off` |

`/phone-approve:on` 을 입력하는 대신 그냥 "나갈게, 외출 모드 켜줘"라고 말해도 돼요.

외출 모드에서는 이런 알림이 폰으로 와요.
- 🔐 승인 요청 → 버튼을 눌러 허용/거부
- ✅ 작업이 끝났을 때
- 🔔 Claude가 내 대답을 기다릴 때

## Codex도 쓴다면
설정할 때 Claude가 "Codex도 쓰세요?" 하고 물어봐요. **네**라고 하면
Codex 작업이 끝날 때도 폰으로 알림이 오고, 승인창이 덜 뜨도록 설정해 줘요.
(Codex는 승인 버튼을 폰으로 보낼 방법이 없어서, 승인창 자체를 줄이는 방식이에요.)

## 알아두면 좋은 것
- 9분 안에 버튼을 안 누르면 PC 화면에 원래 승인창이 떠요.
- PC가 **절전 모드**면 작업이 멈춰요. 전원 설정에서 절전을 "안 함"으로 해 두세요.
- 채널 이름은 비밀번호예요. 다른 사람에게 알려주지 마세요.
- 파이썬이 필요해요. 없으면 설정할 때 Claude가 설치를 도와줘요.
- 지우기: `/plugin uninstall phone-approve@c2b-tools`
