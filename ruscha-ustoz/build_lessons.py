#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_lessons.py — YouGlish'ning ishini to'g'ridan-to'g'ri YouTube'da takrorlaydi.

Mantiq (YouGlish ham xuddi shunday ishlaydi):
  1) Har bir ruscha gap uchun YouTube'dan bir nechta nomzod video topamiz (yt-dlp qidiruvi).
  2) Har video subtitrini (avtomatik yoki qo'lda) olamiz — bu {matn, boshlanish_vaqti} ro'yxati.
  3) Gap (yoki uning kalit qismi) qaysi subtitr bo'lagida uchrasa — o'sha soniyani yozamiz.
  4) Natija: lessons.json -> [{ru, tr, en, uz, yt:{id, start, caption}}].
Ilova YouTube'ni shu soniyadan (start=) embed qiladi. Kalit ham, kvota ham kerak emas.

MUHIM: bu skriptni INTERNET OCHIQ joyda ishga tushiring (kompyuteringiz yoki GitHub Actions).

O'rnatish (venv bilan — tavsiya etiladi):
  python3 -m venv rus-venv
  source rus-venv/bin/activate         # Windows: rus-venv\\Scripts\\activate
  pip install yt-dlp youtube-transcript-api

Ishga tushirish:
  python build_lessons.py sample_sentences.json lessons.json
"""

import json
import re
import sys
import time

from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi

SEARCH_PER_PHRASE = 12      # har gap uchun nechta video sinaladi
LANGS = ["ru"]              # subtitr tili
PAD_BEFORE = 1              # gapdan 1 soniya oldin boshlaydi (kontekst uchun)


def normalize(s: str) -> str:
    """Kichik harf, tinish belgilarsiz, bitta bo'shliq — solishtirish uchun."""
    s = s.lower().replace("ё", "е")
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def make_transcript_fetcher():
    """
    youtube-transcript-api'ning ESKI (<1.0, get_transcript) va YANGI (>=1.0, .fetch)
    versiyalarini ham qo'llaydi. Har ikkisi uchun bir xil ro'yxat qaytaradi:
    [{"text": ..., "start": ...}, ...]
    """
    inst = YouTubeTranscriptApi()
    if hasattr(inst, "fetch"):                      # yangi API
        def fetch(vid):
            data = inst.fetch(vid, languages=LANGS)
            return [{"text": sn.text, "start": float(sn.start)} for sn in data]
        return fetch
    else:                                           # eski API
        def fetch(vid):
            data = YouTubeTranscriptApi.get_transcript(vid, languages=LANGS)
            return [{"text": d["text"], "start": float(d["start"])} for d in data]
        return fetch


TRANSCRIPT = make_transcript_fetcher()


def search_video_ids(query: str, n: int):
    opts = {
        "quiet": True, "no_warnings": True, "skip_download": True,
        "extract_flat": True, "default_search": f"ytsearch{n}",
    }
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(query, download=False)
        return [e["id"] for e in info.get("entries", []) if e.get("id")]
    except Exception:
        return []


def find_clip(phrase: str):
    """Gap aytilgan videoni va soniyani topadi. Topolmasa None."""
    target = normalize(phrase)
    words = target.split()
    key = target if len(words) <= 5 else " ".join(words[:5])  # uzun gap -> kalit qism

    for vid in search_video_ids(phrase, SEARCH_PER_PHRASE):
        try:
            tr = TRANSCRIPT(vid)
        except Exception:
            continue
        for j in range(len(tr)):
            window = normalize(" ".join(seg["text"] for seg in tr[j:j + 3]))
            if key and key in window:
                start = max(0, int(tr[j]["start"]) - PAD_BEFORE)
                return {"id": vid, "start": start, "caption": tr[j]["text"].strip()}
    return None


def main(inp, outp):
    data = json.load(open(inp, encoding="utf-8"))
    out, hits = [], 0
    for i, item in enumerate(data, 1):
        clip = find_clip(item["ru"])
        item["yt"] = clip
        out.append(item)
        if clip:
            hits += 1
        status = f"OK  {clip['id']} @ {clip['start']}s" if clip else "topilmadi"
        print(f"[{i}/{len(data)}] {item['ru'][:40]:<40} -> {status}", flush=True)
        json.dump(out, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        time.sleep(0.5)
    print(f"\nTayyor: {hits}/{len(out)} gapga video topildi -> {outp}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Foydalanish: python build_lessons.py <sentences.json> <lessons.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
