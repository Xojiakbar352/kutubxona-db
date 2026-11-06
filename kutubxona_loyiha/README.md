# Kutubxona ma’lumotlar bazasi

**Mavzu:** 3. Kutubxona tizimi uchun ma’lumotlar bazasi. Kichik o‘quv loyihasi.

## Maqsad
Kitoblar, o‘quvchilar va kitob berish/qaytarish jarayonlarini SQLite bazasida saqlash.

## Ishga tushirish
Python 3.10+ o‘rnatilgan bo‘lsin. Terminalda loyiha papkasiga o‘ting:

```bash
python app.py
```

Dastur birinchi ishga tushganda `library.db` bazasini va namuna yozuvlarni yaratadi. Menyuda 1–4 amallarni sinab ko‘ring.

## Test
```bash
python -m unittest discover -s tests -v
```

## Jadvallar
- `readers`: o‘quvchilar (`id` — PK).
- `books`: kitoblar (`id` — PK, `copies_total` — nusxalar soni).
- `loans`: berilgan kitoblar (`reader_id`, `book_id` — FK; `return_date` bo‘sh bo‘lsa kitob qaytarilmagan).

Aloqa: `readers (1) — (N) loans (N) — (1) books`.

## Jamoa rollari (namunaviy taqsimot)
- **Dasturchi / DB developer:** SQL sxema va `app.py`.
- **DevOps:** GitHub repository va ishga tushirish tartibi.
- **CI/CD mas’uli:** `.github/workflows/tests.yml` avtomatik testlari.
- **Tester:** `tests/test_app.py`, xatoliklarni tekshirish.
- **DataOps:** test ma’lumotlari, sifat nazorati va baza nusxalarini boshqarish.

Bir talaba barcha qismlarni tayyorlab namoyish qilishi mumkin; haqiqiy jamoa bo‘lsa ismlar rollarga biriktiriladi.

## GitHubga joylash
1. GitHubda yangi `kutubxona-db` repository yarating.
2. Ushbu papkadagi fayllarni yuklang yoki `git init`, `git add .`, `git commit -m "Initial project"` bilan commit qiling.
3. `git remote add origin <repository-URL>` va `git push -u origin main` orqali yuboring (zarur bo‘lsa avval `git branch -M main`).
4. GitHub Actions bo‘limida test natijasini tekshiring.

**Eslatma:** GitHub repository bu arxivda avtomatik ochilmagan. Uni shaxsiy akkauntingizda yaratish kerak.
