# 📱 폰으로 승인하기 (PC 앞에 없어도 Claude Code·Codex 작업이 안 끊기게)

밖에서 휴대폰으로 일을 시켰는데, PC 화면에 **"이 명령 실행해도 될까요?"** 창이 떠서
작업이 멈춰 버리는 문제를 해결해요.

```
PC의 Claude Code ──"rm -rf build 해도 돼요?"──▶ 텔레그램 봇 ──▶ 📱 내 폰
                                                         [✅ 허용] [❌ 거부]
PC의 Claude Code ◀──────────── "허용" ──────────────────────────┘  → 작업 계속!
```

---

## 0단계. 먼저 알아두기: 방법은 3가지예요

| 방법 | 어떤 거예요? | 추천 상황 |
|---|---|---|
| **A. 승인창 자체를 줄이기** | 안전한 명령은 묻지 않게 설정 | **모두 꼭 하세요** (아래 1단계) |
| **B. Claude 공식 기능 "Remote Control"** | Claude 앱에서 PC 세션을 이어서 쓰고 승인도 앱에서 눌러요 | Claude Code만 쓴다면 이게 제일 간단해요 (2단계) |
| **C. 이 폴더의 텔레그램 봇** | 승인 버튼과 "작업 끝" 알림을 텔레그램으로 받아요 | Remote Control을 안 켜고 터미널에서 그냥 돌릴 때, Codex 알림도 받고 싶을 때 (3단계) |

> 💡 B와 C는 함께 써도 돼요. 그럴 땐 승인 요청이 텔레그램으로 먼저 와요.

---

## 1단계. 승인창 줄이기 (5분)

### Claude Code
Claude Code 안에서 이렇게 해 보세요.

1. **`Shift + Tab`** 을 눌러 모드를 바꿔요.
   - `accept edits on` : 파일 고치기는 묻지 않아요 (추천)
   - `auto mode` : 웬만한 건 Claude가 안전한지 판단해서 알아서 해요 (보이면 이걸 추천)
2. 자주 묻는 명령을 한 번에 허용 목록에 넣기:
   ```
   /fewer-permission-prompts
   ```
   지난 작업 기록을 보고 "자주 승인한 안전한 명령"을 자동으로 허용 목록에 넣어줘요.
3. 승인창이 뜰 때 **"Yes, and don't ask again"** (다시 묻지 않기)를 고르면 다음부터 안 물어봐요.

### Codex
[`codex/config.toml`](codex/config.toml) 내용을 내 컴퓨터의 Codex 설정 파일에 붙여넣으세요.
- Windows: `C:\Users\내이름\.codex\config.toml`
- Mac: `~/.codex/config.toml`

작업 폴더 안에서는 묻지 않고 알아서 하고, 폴더 밖은 못 건드리게 막아요.

---

## 2단계. Claude 공식 Remote Control 켜기 (3분, Claude Code 전용)

1. PC에서 Claude Code를 켜고 입력: `/config`
2. **Enable Remote Control for all sessions** 를 켜요. (이제 모든 세션이 폰과 연결돼요)
3. 같은 `/config` 화면에서 **Push when actions required** 를 켜요.
   → 승인이 필요하면 폰에 푸시 알림이 와요.
4. 폰의 **Claude 앱 → Code** 에서 내 PC 세션을 열고, 승인 버튼을 누르면 돼요.

> 이미 켜둔 세션이면 그 안에서 `/remote-control` 만 입력해도 돼요. QR코드를 폰으로 찍으면 바로 열려요.

---

## 3단계. 텔레그램 승인 봇 설치 (10분)

### ① 파이썬 설치 (이미 있으면 건너뛰기)
- [python.org](https://www.python.org/downloads/)에서 내려받아 설치해요.
- ⚠️ Windows는 설치 첫 화면에서 **"Add python.exe to PATH"** 에 꼭 체크하세요.
- 다른 프로그램은 설치하지 않아도 돼요.

### ② 텔레그램 봇 만들기
1. 폰에 **텔레그램** 앱을 설치하고 가입해요.
2. 검색창에 **`@BotFather`** 를 검색해서 들어가요. (파란 체크 표시가 있는 공식 계정)
3. `/newbot` 을 보내요.
4. 봇 이름(아무거나, 예: `내PC승인봇`)을 보내요.
5. 봇 아이디를 보내요. **반드시 `bot`으로 끝나야 해요** (예: `my_pc_approve_bot`).
6. BotFather가 `123456789:ABCdef...` 같은 **토큰**을 줘요. 복사해 두세요.
   > 🔒 토큰은 비밀번호예요. 다른 사람에게 보여주지 마세요.

### ③ 이 폴더를 PC에 받기
`remote-approval` 폴더를 통째로 PC에 내려받아요. (예: `C:\Users\내이름\remote-approval`)
> 폴더 위치를 나중에 옮기면 ④를 다시 해야 해요.

### ④ 설치 도우미 실행
터미널(Windows는 `명령 프롬프트` 또는 `PowerShell`)을 열고:

```bash
cd C:\Users\내이름\remote-approval     # Mac은: cd ~/remote-approval
python setup.py                        # Mac은: python3 setup.py
```

화면에서 시키는 대로 하면 돼요.
1. 토큰을 붙여넣고 Enter
2. 폰 텔레그램에서 내 봇을 찾아 **아무 메시지나 보내기** (예: `안녕`)
3. 폰에 "🎉 연결 성공!" 메시지가 오면 성공
4. "Claude Code에 자동 등록할까요?" → `y`
5. 마지막에 나오는 `notify = [...]` 줄은 Codex용이에요. Codex를 쓰면 `config.toml`에 붙여넣으세요.

### ⑤ 확인하기
Claude Code를 **껐다가 다시 켜고**, 승인이 필요한 일을 시켜 보세요.
폰 텔레그램에 `[✅ 허용] [❌ 거부]` 버튼이 오면 성공이에요!

---

## ⚙️ 설정 바꾸기 (`config.json`)

설치하면 폴더에 `config.json` 이 생겨요. 메모장으로 열어서 바꿀 수 있어요.

| 항목 | 뜻 | 기본값 |
|---|---|---|
| `timeout_seconds` | 폰에서 몇 초 동안 답을 기다릴지 | `540` (9분) |
| `on_timeout` | 시간 안에 답이 없으면? `"ask"` = PC 화면에 원래 승인창 띄우기, `"deny"` = 거부하고 Claude가 다른 방법 찾기 | `"ask"` |
| `pc_name` | 메시지에 보일 PC 이름 (PC가 여러 대일 때 구분용) | 컴퓨터 이름 |

> 💡 밖에 오래 있을 땐 `on_timeout` 을 `"deny"` 로 바꾸면 작업이 멈춰서 기다리지 않아요.

---

## 🔌 작업이 끊기는 다른 이유들

| 증상 | 해결 |
|---|---|
| PC가 절전 모드로 들어가서 멈춤 | Windows: `설정 → 시스템 → 전원 → 화면 및 절전` 에서 절전을 **안 함**으로. Mac: 터미널에서 `caffeinate -dis` 를 켜두기 |
| 로그인이 풀렸다고 나옴 | PC에서 `claude auth login` 을 한 번 다시 해요. (Remote Control을 쓰려면 `setup-token` 방식 말고 이 방식으로 로그인해야 해요) |
| 아예 PC 없이 하고 싶음 | 폰의 Claude 앱 → **Code** 에서 깃허브 저장소를 골라 시작하면 **클라우드**에서 돌아가요. PC를 켜둘 필요도 없고 승인창도 거의 없어요 |

---

## 🛡 안전 장치
- **내 텔레그램 채팅방**에서 누른 버튼만 인정해요. 다른 사람이 봇을 찾아내도 승인할 수 없어요.
- 봇 토큰이 들어있는 `config.json` 은 `.gitignore` 에 있어서 깃허브에 올라가지 않아요.
- 설치 도우미는 기존 Claude 설정을 `settings.json.backup` 으로 백업한 뒤에 고쳐요.

## 🗑 지우는 방법
`~/.claude/settings.json.backup` 을 `settings.json` 으로 되돌리거나,
`settings.json` 에서 `remote-approval` 이 들어간 줄들을 지우면 돼요.

## 📂 파일 설명
| 파일 | 하는 일 |
|---|---|
| `setup.py` | 처음 한 번 실행하는 설치 도우미 |
| `claude_approve.py` | Claude 승인 요청을 폰으로 보내고 답을 받아와요 |
| `notify.py` | "작업 끝", "입력 기다리는 중" 알림 (Claude·Codex 공용) |
| `tg_common.py` | 텔레그램과 대화하는 공통 코드 |
| `codex/config.toml` | Codex 설정 예시 |
