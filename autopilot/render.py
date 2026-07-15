#!/usr/bin/env python3
"""
Render a mockup folder's index.html to PNGs via Chrome DevTools Protocol.
 - hero.png : above-the-fold 1440x900 @2x (the outreach thumbnail)
 - full.png : the whole page @2x (the "see the full concept" image)

Cross-platform Chrome discovery (macOS local + ubuntu GitHub Actions).
Usage: python3 render.py <folder-with-index.html> [<folder2> ...]
"""
import asyncio, json, base64, subprocess, time, urllib.request, os, sys, shutil
import websockets

PORT = 9223
WIDTH, HEIGHT, DSF = 1440, 900, 2

def find_chrome():
    for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              shutil.which("google-chrome"), shutil.which("google-chrome-stable"),
              shutil.which("chromium"), shutil.which("chromium-browser"),
              shutil.which("chrome")):
        if c and os.path.exists(c):
            return c
    raise SystemExit("No Chrome/Chromium found")

async def msg(ws, i, m, p=None):
    await ws.send(json.dumps({"id": i, "method": m, "params": p or {}}))
    while True:
        r = json.loads(await ws.recv())
        if r.get("id") == i:
            return r

async def wev(ws, m, t=15):
    try:
        async with asyncio.timeout(t):
            while True:
                r = json.loads(await ws.recv())
                if r.get("method") == m:
                    return r
    except Exception:
        return None

REVEAL = r"""
(async () => {
  const sleep = ms => new Promise(r=>setTimeout(r,ms));
  const H = document.documentElement.scrollHeight;
  for (let y=0; y<=H; y+=320){ window.scrollTo(0,y); await sleep(16); }
  window.scrollTo(0,H); await sleep(120);
  document.querySelectorAll('*').forEach(el=>{
    const s = getComputedStyle(el);
    if (parseFloat(s.opacity) < 0.05 && el.getBoundingClientRect().height>0 &&
        !/overlay|backdrop|glow|grain|noise|scrim/i.test(el.className||'')){
      el.style.opacity='1'; el.style.transform='none'; el.style.transition='none';
    }
  });
  window.scrollTo(0,0); await sleep(60);
  return document.documentElement.scrollHeight;
})()
"""

async def shoot(ws, nid, folder):
    f = os.path.join(folder, "index.html")
    if not os.path.exists(f):
        print(f"  SKIP {folder}: no index.html"); return None
    await msg(ws, nid(), "Emulation.setDeviceMetricsOverride",
              {"width": WIDTH, "height": HEIGHT, "deviceScaleFactor": DSF, "mobile": False})
    await msg(ws, nid(), "Page.navigate", {"url": "file://" + os.path.abspath(f)})
    await wev(ws, "Page.loadEventFired", 20)
    await asyncio.sleep(1.6)  # fonts + images settle
    await msg(ws, nid(), "Runtime.evaluate", {"expression": REVEAL, "awaitPromise": True})
    await asyncio.sleep(0.5)
    # hero: above the fold
    hero = await msg(ws, nid(), "Page.captureScreenshot",
                     {"format": "png", "captureBeyondViewport": False})
    hp = os.path.join(folder, "hero.png")
    open(hp, "wb").write(base64.b64decode(hero["result"]["data"]))
    # full page
    lm = await msg(ws, nid(), "Page.getLayoutMetrics")
    cs = lm["result"].get("cssContentSize") or lm["result"]["contentSize"]
    w = max(WIDTH, round(cs["width"])); h = min(round(cs["height"]), 16000)
    full = await msg(ws, nid(), "Page.captureScreenshot",
                     {"format": "png", "captureBeyondViewport": True,
                      "clip": {"x": 0, "y": 0, "width": w, "height": h, "scale": 1}})
    fp = os.path.join(folder, "full.png")
    open(fp, "wb").write(base64.b64decode(full["result"]["data"]))
    print(f"  OK {os.path.basename(folder)}  hero {os.path.getsize(hp)//1024}KB  full {w}x{h} {os.path.getsize(fp)//1024}KB")
    return {"hero": hp, "full": fp}

async def main(folders):
    t = json.loads(urllib.request.urlopen(f"http://localhost:{PORT}/json").read())
    u = next(x for x in t if x["type"] == "page")["webSocketDebuggerUrl"]
    i = [0]; nid = lambda: (i.__setitem__(0, i[0] + 1) or i[0])
    res = {}
    async with websockets.connect(u, max_size=200_000_000) as ws:
        await msg(ws, nid(), "Page.enable"); await msg(ws, nid(), "Runtime.enable")
        for folder in folders:
            res[folder] = await shoot(ws, nid, folder)
    return res

def render(folders):
    chrome = find_chrome()
    tmp = "/tmp/chrome-mockup-render"
    proc = subprocess.Popen(
        [chrome, "--headless=new", f"--remote-debugging-port={PORT}", "--remote-allow-origins=*",
         f"--user-data-dir={tmp}", "--hide-scrollbars", "--no-first-run", "--no-sandbox",
         "--disable-gpu", "--force-color-profile=srgb", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://localhost:{PORT}/json/version", timeout=1).read(); break
            except Exception:
                time.sleep(0.25)
        return asyncio.run(main(folders))
    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except Exception: proc.kill()

if __name__ == "__main__":
    folders = sys.argv[1:] or []
    if not folders:
        print("usage: render.py <folder> [...]"); sys.exit(1)
    render([os.path.abspath(x) for x in folders])
    print("DONE")
