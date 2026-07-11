#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_english.py — sentences.json ga inglizcha tarjima (en) qo'shadi.
Internet ochiq joyda ishga tushiring (Mac terminal yoki GitHub Actions).

O'rnatish:
  pip install deep-translator          # venv ichida

Ishga tushirish:
  python add_english.py sentences.json
"""
import json, sys, time
from deep_translator import GoogleTranslator

def main(path):
    data = json.load(open(path, encoding="utf-8"))
    tr = GoogleTranslator(source="ru", target="en")
    for i, item in enumerate(data, 1):
        if item.get("en"):
            continue
        try:
            item["en"] = tr.translate(item["ru"])
        except Exception as e:
            item["en"] = ""
            print(f"  [{i}] xato: {e}")
        if i % 25 == 0:
            print(f"[{i}/{len(data)}] ...", flush=True)
            json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(0.15)
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    done = sum(1 for x in data if x.get("en"))
    print(f"\nTayyor: {done}/{len(data)} ga inglizcha qo'shildi -> {path}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sentences.json")
