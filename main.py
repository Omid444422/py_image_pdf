#!/usr/bin/env python3
import sys
from PIL import Image

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 test.py [output.pdf] img1 img2 ...")
        sys.exit(1)

    # اگر اولین ورودی .pdf بود، اسم فایل خروجی است
    if args[0].lower().endswith(".pdf"):
        output, files = args[0], args[1:]
    else:
        output, files = "output.pdf", args

    if not files:
        print("No image files given.")
        sys.exit(1)

    pages = []
    for path in files:
        img = Image.open(path)

        # مدیریت عکس‌های شفاف (PNG با آلفا)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")

        pages.append(img)

    pages[0].save(
        output,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=pages[1:],
    )
    print(f"✔ Saved {len(pages)} page(s) to {output}")

if __name__ == "__main__":
    main()
