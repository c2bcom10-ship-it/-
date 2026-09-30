#!/bin/bash
# 릴스 분석 도구 설치 스크립트 (맥 전용)
# 설치하는 것: yt-dlp, ffmpeg, whisper-cpp, whisper 모델(ggml-large-v3-turbo-q5_0.bin)
# 이 스크립트는 맥 비밀번호를 묻지 않아요. Homebrew가 없으면 설치 방법만 알려주고 멈춰요.

set -e

MODEL_NAME="ggml-large-v3-turbo-q5_0.bin"
MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/${MODEL_NAME}"
MODEL_DIR="$HOME/.cache/whisper"

if [ "$(uname)" != "Darwin" ]; then
  echo "❌ 이 스크립트는 맥에서만 실행할 수 있어요."
  exit 1
fi

# 1. Homebrew 확인
# 터미널에 PATH가 아직 안 잡혀 있어도 찾을 수 있게 기본 설치 위치를 먼저 불러와요.
for BREW in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  if [ -x "$BREW" ]; then
    eval "$("$BREW" shellenv)"
    break
  fi
done

if ! command -v brew >/dev/null 2>&1; then
  echo "❌ Homebrew가 없어요. 아래 명령어를 터미널에 붙여넣고 엔터를 누르세요."
  echo "   (맥 비밀번호를 물어보면 입력하세요. 입력할 때 글자가 안 보이는 게 정상이에요.)"
  echo
  echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  echo
  echo "설치가 끝나면 이 스크립트를 다시 실행하세요."
  exit 1
fi
echo "✅ Homebrew 확인: $(brew --version | head -1)"

# 2. yt-dlp, ffmpeg, whisper-cpp 설치 (이미 있으면 건너뛰어요)
for PKG in yt-dlp ffmpeg whisper-cpp; do
  if brew list --versions "$PKG" >/dev/null 2>&1; then
    echo "✅ $PKG 는 이미 설치돼 있어요."
  else
    echo "⏳ $PKG 설치 중..."
    brew install "$PKG"
  fi
done

# 3. whisper 모델 내려받기 (약 550MB, 중간에 끊겨도 다시 실행하면 이어받아요)
mkdir -p "$MODEL_DIR"
echo "⏳ whisper 모델 내려받는 중... (몇 분 걸릴 수 있어요)"
curl -L --fail -C - -o "$MODEL_DIR/$MODEL_NAME" "$MODEL_URL"

# 4. 설치된 버전 확인
echo
echo "===== 설치된 버전 ====="
echo "yt-dlp      : $(yt-dlp --version)"
echo "ffmpeg      : $(ffmpeg -version | head -1)"
echo "whisper-cpp : $(brew list --versions whisper-cpp)"
echo "모델 파일   : $(ls -lh "$MODEL_DIR/$MODEL_NAME" | awk '{print $5, $NF}')"
echo
echo "설치 끝!"
