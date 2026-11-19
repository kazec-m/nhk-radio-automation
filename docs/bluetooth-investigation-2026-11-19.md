# Bluetooth audio investigation — 2026-11-19

## Summary
- Intermittent Bluetooth connection sounds were heard at night in the past.
- The issue was not observed on 2026-11-19; audio is currently operating normally.
- Root cause has not been established.

## Observations
- Bluetooth service: active (running), since 2026-08-04.
- WirePlumber service: active (running), since 2026-08-04.
- 2026-11-08, approximately 19:51–19:54: repeated BlueZ AVDTP connection errors, `Host is down (112)`.
- Historical WirePlumber logs showed `Failed to release transport` and `bluez_output` / `xrun` messages, including around 06:15 on several dates.
- No WirePlumber journal entries were returned for 2026-11-08 19:50–19:56.
- User crontab starts `run_nhk_echo.sh` at 06:00 on weekdays. November 8 was Sunday.
- `run_nhk_echo.sh` sets the default audio sink, adjusts volume, and starts the Python radio player. It contains no explicit Bluetooth connect command.
- A keyword search of `nhk_radio_echo.py` for Bluetooth/connect/pactl/wpctl returned no matches.
- The Raspberry Pi launcher appears to differ from the updated GitHub version; deployment status needs verification.

## Possible explanations (not confirmed)
- The Bluetooth audio device may have been unavailable, asleep, or temporarily unreachable.
- BlueZ or audio-session management may have retried a connection.
- Morning audio xruns may be separate from nighttime connection errors.

## Follow-up
1. If the sound recurs, record its exact timestamp and compare BlueZ and WirePlumber logs.
2. Check whether the speaker enters standby or is connected to another device.
3. Compare the deployed Raspberry Pi scripts with the GitHub main branch before updating anything.
4. Avoid changing Bluetooth settings while the system is operating normally.

## Privacy
Device addresses, local IP addresses, credentials and secrets are intentionally omitted.
