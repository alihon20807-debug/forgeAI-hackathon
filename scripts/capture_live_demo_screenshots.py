"""Interactive Live Demo Screenshot Capture using Chrome DevTools Protocol (CDP)."""

import asyncio
import base64
import json
import subprocess
import time
import urllib.request
import websockets

async def cdp_call(ws, method, params=None, req_id=1):
    msg = {"id": req_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get("id") == req_id:
            return resp.get("result", {})

async def run():
    # 1. Reset demo session first
    req = urllib.request.Request("http://localhost:8000/api/session/reset?session_id=live-demo", method="POST")
    urllib.request.urlopen(req)
    print("Session reset.")

    # 2. Launch Chromium with debugging port
    proc = subprocess.Popen([
        "chromium", "--headless", "--disable-gpu", "--no-sandbox",
        "--remote-debugging-port=9222", "--window-size=1440,900"
    ])
    time.sleep(1.5)

    try:
        # Get browser targets
        targets = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
        initial_target = targets[0]

        # Connect to Target 1 (Viewer)
        viewer_ws = await websockets.connect(initial_target["webSocketDebuggerUrl"])
        await cdp_call(viewer_ws, "Page.navigate", {"url": "http://localhost:8000/viewer"}, 1)
        await asyncio.sleep(1.5)
        print("Viewer loaded and connected to /ws/live.")

        # Create new target for Phone (Mobile Viewport)
        req_new = urllib.request.Request("http://localhost:9222/json/new?http://localhost:8000/call", method="PUT")
        create_res = json.loads(urllib.request.urlopen(req_new).read())
        phone_ws = await websockets.connect(create_res["webSocketDebuggerUrl"])
        
        # Emulate Android mobile viewport (412x915)
        await cdp_call(phone_ws, "Emulation.setDeviceMetricsOverride", {
            "width": 412,
            "height": 915,
            "deviceScaleFactor": 2.0,
            "mobile": True
        }, 10)
        await asyncio.sleep(1.5)
        print("Phone UI loaded in mobile emulation mode.")

        # Click Turn 1 Pill: "🚗 1. Breakdown on NH48"
        print("Clicking Turn 1: Breakdown on NH48...")
        await cdp_call(phone_ws, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.pill-btn')[0].click()"
        }, 20)
        await asyncio.sleep(2.0)

        # Click Turn 2 Pill: "✋ 2. Cancel Tow + Card Leak"
        print("Clicking Turn 2: Cancel Tow + Card Leak...")
        await cdp_call(phone_ws, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.pill-btn')[1].click()"
        }, 30)
        await asyncio.sleep(2.5)

        # Capture Phone Screenshot
        phone_shot = await cdp_call(phone_ws, "Page.captureScreenshot", {"format": "png"}, 40)
        with open("/tmp/phone_active.png", "wb") as f:
            f.write(base64.b64decode(phone_shot["data"]))
        print("Saved /tmp/phone_active.png")

        # Capture Viewer Screenshot
        viewer_shot = await cdp_call(viewer_ws, "Page.captureScreenshot", {"format": "png"}, 50)
        with open("/tmp/viewer_active.png", "wb") as f:
            f.write(base64.b64decode(viewer_shot["data"]))
        print("Saved /tmp/viewer_active.png")

        await viewer_ws.close()
        await phone_ws.close()
    finally:
        proc.terminate()
        print("Headless browser closed.")

if __name__ == "__main__":
    asyncio.run(run())
