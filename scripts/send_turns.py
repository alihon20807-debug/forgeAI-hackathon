import json
import time
import urllib.request
import subprocess

def send_turn(turn_id, text):
    data = json.dumps({
        "session_id": "live-demo",
        "turn_id": turn_id,
        "caller_id": "caller_mobile",
        "raw_transcript": text,
        "masked_transcript": text,
        "agent_version": "v2"
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8000/api/call/turn",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req)
    res_data = json.loads(resp.read())
    print(f"Turn {turn_id} processed:", res_data.get("agent_response")[:80])
    return res_data

# Turn 1
print("Sending Turn 1...")
send_turn(1, "Hello, my car broke down near Manesar on NH48. Can you send a flatbed tow truck?")

# Turn 2
print("Sending Turn 2...")
send_turn(2, "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4532 0150 1234 5678 hai for claim.")

# Take screenshot of viewer
time.sleep(1)
subprocess.run([
    "chromium", "--headless", "--disable-gpu", "--no-sandbox",
    "--window-size=1440,1080", "--screenshot=/tmp/viewer_final.png",
    "http://localhost:8000/viewer"
], check=True)
print("Saved /tmp/viewer_final.png successfully!")
