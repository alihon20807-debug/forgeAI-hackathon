"""Generates the official backup screencast video for ClaimGuard Golden Demo.

Executes the 4-beat golden demo against the running FastAPI server:
1. Initial clean state
2. Turn 1: Breakdown on NH48 -> Action HELD
3. Turn 2: Revocation + Card Leak -> Action FROZEN -> ABORTED, Card REDACTED
4. Turn 3: Fee Waiver Pressure -> Outbound Veto triggered, Policy Latch intact
5. Turn 4: Spoken Aadhaar & Phone -> Verhoeff D5 & Luhn mathematical masking

Captures high-resolution frames of http://127.0.0.1:8000/viewer across each step
and renders assets/demo/claimguard_golden_demo_backup.mp4 using ffmpeg.
"""

import json
import os
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = REPO_ROOT / "assets" / "demo"
FRAMES_DIR = Path("/tmp/claimguard_video_frames")
OUTPUT_VIDEO = DEMO_DIR / "claimguard_golden_demo_backup.mp4"

DEMO_TURNS = [
    {
        "turn_id": 1,
        "label": "Turn 1: Clean Breakdown Intimation",
        "text": "Hello, my car broke down near Manesar on NH48. Can you send a flatbed tow truck?",
        "hold_seconds": 6,
    },
    {
        "turn_id": 2,
        "label": "Turn 2: Mid-Call Revocation + Spoken Card Number",
        "text": "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4111 1111 1111 1111 hai for claim.",
        "hold_seconds": 7,
    },
    {
        "turn_id": 3,
        "label": "Turn 3: Deductible Pressure & Concession Request",
        "text": "Mera 1500 rupees deductible waive kar do please, I have been your loyal customer for 5 years!",
        "hold_seconds": 6,
    },
    {
        "turn_id": 4,
        "label": "Turn 4: Spoken Aadhaar & Phone Verification",
        "text": "Aadhaar number note kar lijiye 3675 9834 6012 aur phone 98765 43210 for verification.",
        "hold_seconds": 7,
    },
]


def reset_session():
    print("Resetting live demo session...")
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/session/reset?session_id=live-demo",
            method="POST",
        )
        urllib.request.urlopen(req)
    except Exception as e:
        print("Reset warning:", e)


def capture_screenshot(dest_path: Path):
    subprocess.run([
        "chromium",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1440,900",
        f"--screenshot={dest_path}",
        "http://127.0.0.1:8000/viewer",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def send_turn(turn_id: int, text: str):
    data = json.dumps({
        "session_id": "live-demo",
        "turn_id": turn_id,
        "caller_id": "caller_golden_demo",
        "raw_transcript": text,
        "masked_transcript": text,
        "agent_version": "v2",
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/call/turn",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def main():
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    reset_session()
    frame_idx = 1

    print("Capturing Frame 0: Initial Clean Command Center...")
    initial_shot = FRAMES_DIR / "shot_0.png"
    capture_screenshot(initial_shot)

    # Replicate initial frame for 4 seconds
    for _ in range(4):
        shutil.copyfile(initial_shot, FRAMES_DIR / f"frame_{frame_idx:04d}.png")
        frame_idx += 1

    for turn_spec in DEMO_TURNS:
        tid = turn_spec["turn_id"]
        label = turn_spec["label"]
        text = turn_spec["text"]
        hold = turn_spec["hold_seconds"]

        print(f"\nExecuting {label}...")
        res = send_turn(tid, text)
        print(f"Agent reply: {res.get('agent_response', '')[:90]}...")

        # Small pause for state commit and DB triggers
        time.sleep(0.5)

        shot_path = FRAMES_DIR / f"shot_{tid}.png"
        capture_screenshot(shot_path)

        for _ in range(hold):
            shutil.copyfile(shot_path, FRAMES_DIR / f"frame_{frame_idx:04d}.png")
            frame_idx += 1

    total_frames = frame_idx - 1
    duration_sec = total_frames  # 1 frame per second
    print(f"\nCaptured {total_frames} frames ({duration_sec} seconds). Rendering MP4...")

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", "1",
        "-i", str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v", "libx264",
        "-r", "24",
        "-pix_fmt", "yuv420p",
        str(OUTPUT_VIDEO),
    ]
    subprocess.run(cmd, check=True)

    size_mb = OUTPUT_VIDEO.stat().st_size / (1024 * 1024)
    print(f"Golden demo backup video successfully generated at: {OUTPUT_VIDEO} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
