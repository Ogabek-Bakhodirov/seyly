# Ruscha Ustoz — Telegram Mini App

## Fayllar
- index.html — ilova (Web App)
- sentences.json — 1000 so'z (ru + o'qilishi + uz)
- build_lessons.py — har so'zga YouTube video topadi -> lessons.json
- add_english.py — inglizcha tarjima qo'shadi (ixtiyoriy)

## GitHub Pages'da jonlashtirish (bepul)
1. Yangi repo oching: `ruscha` (Public).
2. Shu papkadagi fayllarni yuklang (Add file -> Upload files).
3. Settings -> Pages -> Source: `main` branch, `/root` -> Save.
4. 1 daqiqada manzil tayyor:
   https://ogabek-bakhodirov.github.io/ruscha/
Bu — Telegram Mini App URL'i.

## Videolarni qo'shish (Mac'da, bir marta)
python3 -m venv venv && source venv/bin/activate
pip install yt-dlp youtube-transcript-api
python build_lessons.py sentences.json lessons.json
So'ng lessons.json ni repoga yuklang — videolar avtomatik chiqadi.
