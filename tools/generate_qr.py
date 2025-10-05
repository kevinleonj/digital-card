# tools/generate_qr.py
import os, sys
from typing import Dict

try:
    import qrcode  # type: ignore
except Exception as e:
    sys.stderr.write("Missing dependency 'qrcode'. Install with: pip install qrcode[pil]\n")
    raise

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
OUT_DIR = os.path.join("static", "qr")
os.makedirs(OUT_DIR, exist_ok=True)

def build_urls(base: str) -> Dict[str, str]:
    return {
        "friend": f"{base}/",
        "recruiter": f"{base}/r",
    }

def make_qr_png(name: str, url: str) -> None:
    try:
        img = qrcode.make(url)
        img.save(os.path.join(OUT_DIR, f"{name}.png"))
        print(f"Saved {name}.png -> {url}")
    except Exception as ex:
        print(f"ERROR generating QR for {name}: {ex}")

def main() -> int:
    for name, url in build_urls(BASE_URL).items():
        make_qr_png(name, url)
    print("Done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
