"""Automated Golden Demo Screencast Recorder for ClaimGuard.

Controls headless Chromium via Chrome DevTools Protocol (CDP) to step through
the 4-beat golden demo on http://127.0.0.1:8000/viewer and /call, captures high-resolution
frames across each state transition, and renders a clean H.264 MP4 screencast
to assets/demo/claimguard_golden_demo_backup.mp4.
"""

import asyncio
import base64
import json
import os
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path
import websockets

REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = REPO_ROOT / "assets" / "demo"
FRAMES_DIR = Path("/tmp/claimguard_demo_frames")
OUTPUT_VIDEO = DEMO_DIR / "claimguard_golden_demo_backup.mp4"


async def cdp_call(ws, method, params=None, req_id=1):
    msg = {"id": req_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get("id") == req_id:
            return resp.get("result", {})


async def capture_frame(ws, frame_idx: int):
    shot = await cdp_call(ws, "Page.captureScreenshot", {"format": "png"}, 9000 + frame_idx)
    raw = base64.b64decode(shot["data"])
    filename = FRAMES_DIR / f"frame_{frame_idx:04d}.png"
    with open(filename, "wb") as f:
        f.write(raw)
    return frame_idx + 1


async def record_hold(ws, start_frame: int, duration_sec: float, fps: float = 2.0):
    steps = int(duration_sec * fps)
    current_frame = start_frame
    for _ in range(steps):
        current_frame = await capture_frame(ws, current_frame)
        await asyncio.sleep(1.0 / fps)
    return current_frame


async def main():
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Resetting demo session...")
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/session/reset?session_id=live-demo",
            method="POST"
        )
        urllib.request.urlopen(req)
        print("Session reset to initial state.")
    except Exception as e:
        print(f"Warning: Session reset encountered: {e}")

    print("2. Starting headless Chromium...")
    proc = subprocess.Popen([
        "chromium",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--remote-debugging-port=9222",
        "--window-size=1440,900"
    ])
    await asyncio.sleep(2.0)

    try:
        targets = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json").read())
        viewer_target = targets[0]
        viewer_ws = await websockets.connect(viewer_target["webSocketDebuggerUrl"])
        await cdp_call(viewer_ws, "Page.navigate", {"url": "http://127.0.0.1:8000/viewer"}, 1)
        await asyncio.sleep(1.5)

        # Create caller tab
        req_new = urllib.request.Request("http://127.0.0.1:9222/json/new?http://127.0.0.1:8000/call", method="PUT")
        phone_target = json.loads(urllib.request.urlopen(req_new).read())
        phone_ws = await websockets.connect(phone_target["webSocketDebuggerUrl"])

        frame = 1
        print("Recording initial state...")
        frame = await record_hold(viewer_ws, frame, duration_sec=2.0)

        # Beat 1: Breakdown on NH48
        print("Beat 1: Triggering Breakdown on NH48...")
        await cdp_call(phone_ws, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.pill-btn')[0].click()"
        }, 101)
        frame = await record_hold(viewer_ws, frame, duration_sec=4.0)

        # Beat 2: Revocation + Card Number Leak
        print("Beat 2: Triggering Cancel Tow + Card Leak...")
        await cdp_call(phone_ws, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.pill-btn')[1].click()"
        }, 102)
        frame = await record_hold(viewer_ws, frame, duration_sec=5.0)

        # Beat 3: Lookalike Trap or Concession Pressure
        print("Beat 3: Triggering Pressure & Concession request...")
        await cdp_call(phone_ws, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.pill-btn')[2].click()"
        }, 103)
        frame = await record_hold(viewer_ws, frame, duration_sec=4.5)

        # Beat 4: Aadhaar & Phone Spoken
        print("Beat 4: Triggering Spoken Aadhaar & Phone...")
        await cdp_call(phone_ws, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.pill-btn')[3].click()"
        }, 104)
        frame = await record_hold(viewer_ws, frame, duration_sec=4.5)

        # Hold on final verified audit screen
        print("Recording final audit state...")
        frame = await record_hold(viewer_ws, frame, duration_sec=3.0)

        await viewer_ws.close()
        await phone_ws.close()
    finally:
        proc.terminate()
        proc.wait()

    print(f"Captured {frame - 1} frames. Rendering MP4 video with ffmpeg...")
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", "2",
        "-i", str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v", "libx264",
        "-r", "24",
        "-pix_fmt", "yuv420p",
        str(OUTPUT_VIDEO)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg error:", res.stderr)
    else:
        size_mb = OUTPUT_VIDEO.stat().st_size / (1024 * 1024)
        print(f"Successfully generated {OUTPUT_VIDEO} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    asyncio.run(main())
