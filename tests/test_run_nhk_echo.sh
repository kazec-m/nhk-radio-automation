#!/usr/bin/env bash
# Exercise the launcher without accessing Bluetooth, a browser or Raspberry Pi.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT
mkdir -p "$WORK_DIR/mock-bin"
cp "$ROOT_DIR/run_nhk_echo.sh" "$WORK_DIR/run_nhk_echo.sh"
printf 'ECHO_SINK_NAME=test_sink\nPI_USER=test_user\n' > "$WORK_DIR/.env"

cat > "$WORK_DIR/mock-bin/pactl" <<'MOCK'
#!/usr/bin/env bash
printf 'pactl %s\n' "$*" >> "$MOCK_LOG"
if [[ "${PACTL_EXIT_CODE:-0}" -ne 0 ]]; then
    printf 'mock pactl error\n' >&2
fi
exit "${PACTL_EXIT_CODE:-0}"
MOCK
cat > "$WORK_DIR/mock-bin/sleep" <<'MOCK'
#!/usr/bin/env bash
printf 'sleep %s\n' "$*" >> "$MOCK_LOG"
MOCK
cat > "$WORK_DIR/mock-bin/wpctl" <<'MOCK'
#!/usr/bin/env bash
printf 'wpctl %s\n' "$*" >> "$MOCK_LOG"
MOCK
cat > "$WORK_DIR/mock-bin/xvfb-run" <<'MOCK'
#!/usr/bin/env bash
printf 'xvfb-run %s\n' "$*" >> "$MOCK_LOG"
MOCK
chmod +x "$WORK_DIR/mock-bin/"*

cat > "$WORK_DIR/expected.log" <<'EXPECTED'
pactl set-default-sink test_sink
sleep 5
wpctl set-volume 72 80%
sleep 1
xvfb-run -a python3 /home/test_user/Desktop/nhk_radio_echo.py
EXPECTED

run_case() {
    local label="$1" code="$2"
    export PACTL_EXIT_CODE="$code"
    export MOCK_LOG="$WORK_DIR/$label.log"
    export PATH="$WORK_DIR/mock-bin:$PATH"
    : > "$MOCK_LOG"

    bash "$WORK_DIR/run_nhk_echo.sh" > "$WORK_DIR/$label.stdout" 2> "$WORK_DIR/$label.stderr"
    diff -u "$WORK_DIR/expected.log" "$MOCK_LOG"
    [[ ! -s "$WORK_DIR/$label.stdout" ]]
}

run_case success 0
[[ ! -s "$WORK_DIR/success.stderr" ]]

run_case failure 42
grep -Fxq 'mock pactl error' "$WORK_DIR/failure.stderr"
grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{4} pactl set-default-sink failed: exit code 42$' "$WORK_DIR/failure.stderr"
[[ "$(wc -l < "$WORK_DIR/failure.stderr")" -eq 2 ]]

printf 'PASS: pactl success and failure (exit 42) keep the expected command sequence\n'
