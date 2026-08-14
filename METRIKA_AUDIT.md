# Metrika auditi — o'lchov to'g'riligi

**Yaratildi: 2026-08-12** · Manba: prod `admin_stats()` funksiyasi + jadvallar (jonli tekshirilgan)
Maqsad: target audience kirishidan **oldin** har metrikaning to'g'riligini tasdiqlash.

---

## ⚠️ Bosh topilma: FRONTEND backend'dan 2 versiya orqada

Backend (`admin_stats` RPC) allaqachon **v2** — `claude_58` spetsifikatsiyasi to'liq joriy etilgan:
North Star (W3+ Learners), power curve, true retention, jonli streak, kogorta `_on/_after`,
til kesimi, SR asosidagi aktivatsiya. **Lekin adminka frontendi (HTML) hali eski fieldlarni o'qiydi.**

Natija: adminkada ochilганда **ko'p karta "—" ko'rsatadi yoki umuman noto'g'ri**, va eng muhimi —
**North Star (W3+ Learners) umuman ko'rinmaydi.** Aynan shu — "statistika noto'g'ri ko'rsatyapti" hissi.

---

## Status belgilari
- ✅ **To'g'ri** — backend hisoblaydi, frontend to'g'ri ko'rsatadi, ma'lumot ishonchli
- 🟡 **Ma'lumot yosh** — hisob to'g'ri, lekin tarix kam (target audience bilan to'ladi)
- 🔴 **Frontend buzuq** — backend to'g'ri beradi, lekin frontend eski field o'qib "—"/xato ko'rsatadi
- ⚫ **O'chirilgan** — backend endi bermaydi, frontend hali chaqiradi (o'lik karta)
- 🆕 **Yangi, ko'rsatilmaydi** — backend beradi, frontend umuman render qilmaydi

---

## 1. NORTH STAR — eng muhimi

| Metrika | Backend field | Holat | Izoh |
|---|---|---|---|
| **W3+ Learners (SR)** | `north[].w3_sr` | 🆕🟡 | Haftada ≥3 kun SR review. **Frontendda umuman yo'q.** SR ma'lumoti yosh. |
| W3+ Learners (yadro) | `north[].w3_core` | 🆕 | Amaliy proksi: haftada ≥3 kun yadro harakat. Frontendda yo'q. |

> Shimoliy Yulduzimiz adminkada **ko'rinmaydi** — bu birinchi tuzatiladigan narsa.

## 2. AKTIVATSIYA

| Metrika | Backend | Holat | Izoh |
|---|---|---|---|
| 1-hafta SR≥20 | `stock.a1w_sr20_pct` | 🔴 | Frontend eski `activation_first_lesson_pct` o'qiydi → **"—"** |
| 1-hafta yangi≥20 | `stock.a1w_new20_pct` | 🔴 | Frontendda yo'q |

## 3. STOCK (joriy holat)

| Metrika | Backend | Holat |
|---|---|---|
| Jami user | `stock.users_total` | ✅ |
| Onboarding % | `stock.onboarded_pct` | ✅ |
| Bloklagan | `stock.blocked` | ✅ |
| WAL (haftalik faol) | `stock.wal` | ✅ |
| DAU | `stock.dau` | ✅ (frontend `dau_learn`→`dau` fallback) |
| App open 24h | `stock.app_open_24h` | 🆕 ko'rsatilmaydi |
| **Streak taqsimoti** | `stock.streak_dist` | ✅ **endi JONLI** (B2 tuzatildi — ilgari muzlab qolardi) |
| Streak "muzlagan" | `stock.streak_stale` | 🆕 diagnostika, ko'rsatilmaydi |
| Median kunlik so'z | `stock.median_daily_phrases` | ✅ |
| ~~O'rtacha kunlik so'z~~ | `avg_daily_phrases` | ⚫ **backend o'chirgan**, frontend hali o'qiydi → "—" |
| Pro (jami) | `stock.pro_total` | 🔴 frontend eski `pro_active` → "—" |
| Pro (to'lov/kod/sovg'a) | `pro_paid`/`pro_code`/`pro_gift` | 🆕 (B3) ko'rsatilmaydi |
| ~~Free→Pro %~~ | `free_to_pro_pct` | ⚫ backend o'chirgan, frontend o'qiydi → "—" |
| ~~AI kesh %~~ | `define_cache_ratio_pct` | ⚫ backend o'chirgan, frontend o'qiydi → "—" |

## 4. KOGORTALAR (retention)

| Metrika | Backend | Holat |
|---|---|---|
| D1/D7/D30 (aynan N-kun) | `cohorts[].d1_on / d7_on / d30_on` | 🔴 frontend eski `d1/d7/d30` o'qiydi → **butun jadval "—"** |
| D1/D7/D30 (N-kun yoki keyin) | `cohorts[].d1_after / ...` | 🆕 ikki ta'rif ajratilgan (B5), ko'rsatilmaydi |

## 5. TRUE RETENTION 🔴 sizning misolingiz

| Metrika | Backend | Holat |
|---|---|---|
| Mature/Young retention | `true_retention` | 🆕🟡 **Ma'lumot deyarli yo'q** |

**Sabab (tasdiqlandi):** `sr_reviews` jadvali mavjud va sxemasi to'g'ri (`reviewed_at`, `prev_state`,
`prev_interval`, `passed`, `grade`, `rev`). `sr_apply_review_v2` funksiyasi unga yozadi HAM.
LEKIN yozuv kodi **bugun (2026-08-12 ~09:50)** qo'shilgan — jadvalda atigi **9 qator, hammasi 9 soniyalik oynada**.
Tarixiy 1428 ta SR review (daily_usage.sr_total) log qilinmagan.

**Ikki nuqson:**
1. **Tarix yo'q** — retention faqat bugundan boshlab yig'iladi. Target audience kelguncha tarix to'planadi (yaxshi tomon).
2. **`grade` yozilmaydi** — INSERT `grade` ni qo'ymaydi (null qoladi). `passed` esa haqiqiy javob emas,
   `lapses` oshdi-oshmadi proksisi (`p_lapses <= v_prev_lapses`). Ya'ni "Again/Hard/Good/Easy" farqi saqlanmaydi.

## 6. YANGI METRIKALAR — backend beradi, frontend YO'Q

| Metrika | Backend | Holat |
|---|---|---|
| Power user egri chizig'i (L/28) | `power_curve` | 🆕 ko'rsatilmaydi |
| Streak uzilgandan keyin qaytish | `streak_break` | 🆕 ko'rsatilmaydi |
| Til kesimi (Simpson-xavfsiz) | `by_lang` | 🆕 ko'rsatilmaydi |

## 7. AUDITORIYA (grafiklar)

| Metrika | Backend | Holat |
|---|---|---|
| Tillar (doughnut) | ~~`audience.lang_dist`~~ → `by_lang` | 🔴 frontend eski `lang_dist` o'qiydi → **doughnut buzuq** |
| Darajalar | `audience.level_dist` | ✅ |
| Qiziqishlar | `audience.interest_dist` | ✅ |

## 8. KUNLIK TREND (grafik)

| Chiziq | Backend `daily[]` | Holat |
|---|---|---|
| Faol / Yangi / O'rganilgan / Qidiruv | `active/signups/learned/searches` | ✅ |
| Saqlangan | ~~`saved`~~ | 🔴 backend endi bermaydi, frontend chizig'i bo'sh |
| SR review / Push yuborilgan | `sr_reviews / push_sent` | 🆕 ko'rsatilmaydi |

## 9. ENGAGEMENT

| Metrika | Backend | Holat |
|---|---|---|
| Push CTR (real) | `engagement.push` | ✅ (2026-07-25 dan) |
| Notify (proksi) | `engagement.notif` | ✅ |
| Karta CTR / top | `engagement.card / card_top` | ✅ |
| Pro popup/so'rov | `engagement.pro` | ✅ (2026-07-27 dan) |
| App update CTR | `engagement.app_updates` | ✅ |
| ~~A/B test~~ | `engagement.ab` | ⚫ backend o'chirgan, frontend hali render qiladi (bo'sh) |

## 10. VIDEO BAZASI

| Metrika | Backend | Holat |
|---|---|---|
| Video/ingest holati | ~~`transcript`~~ | 🔴 backend endi bermaydi, frontend "aloqa yo'q" ko'rsatadi |

---

## Xulosa — 3 savolga javob

**1. Nimalarni o'lchashimiz kerak?**
Backend allaqachon to'g'ri ro'yxatni belgilagan (claude_58): North Star W3+ Learners, kogorta retention,
aktivatsiya (SR≥20), power curve, streak break, til kesimi, true retention. Ro'yxat — to'g'ri.

**2. Qanday o'lchaymiz?**
`admin_stats` RPC `daily_usage`/`users`/`events`/`sr_reviews` dan hisoblaydi. Mantiq — asosan sog'lom
(TZ UTC+5 birlashtirilgan, owner chiqarilgan, streak jonli, kogorta ikki ta'rifda).

**3. Nima to'g'ri kelmaydi?**
- 🔴 **FRONTEND 2 versiya orqada** — eng katta muammo. Adminka eski fieldlarni o'qiydi → "—"/xato,
  North Star umuman ko'rinmaydi. **Bu yagona eng katta tuzatish.**
- 🟡 **SR review logi bugun boshlangan** — retention tarixi yo'q (target audience bilan to'ladi).
- 🟡 **`grade` saqlanmaydi** — javob sifati (Again/Good/Easy) yo'qoladi; `passed` faqat proksi.
- ℹ️ Ma'lumot boshlanish sanalari: qidiruv 07-22, push CTR 07-25, Pro 07-27 — undan oldingisi ishonchsiz.

---

## Tavsiya etilgan tartib
1. **Frontendni v2 backendga moslash** (task #52) — bu bir zarbada 🔴 va ⚫ larning HAMMASINI yopadi
   va North Star'ni ko'rsatadi. Eng katta ta'sir.
2. **`grade` ni sr_reviews ga yozish** — `sr_apply_review_v2` INSERT'iga `grade` qo'shish (kichik tuzatish).
3. Target audience kirgach — retention/true_retention tarixi tabiiy to'planadi.
