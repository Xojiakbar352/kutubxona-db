# Kutubxona ma’lumotlar bazasi — 2-versiya

**Mavzu:** Kutubxona tizimi uchun ma’lumotlar bazasi (3-topshiriq).

Python 3.11+ va SQLite bilan yozilgan konsol dasturi. Namunaviy ma’lumotlarda 15 o‘quvchi va 10 kitob bor. Bu real shaxslar bazasi emas, o‘quv namunasidir.

## Ishga tushirish (Windows)

1. GitHubdan ZIP yuklab olib, `Извлечь все` qiling.
2. `kutubxona_loyiha` papkasini oching va manzil qatoriga `cmd` yozib Enter bosing.
3. `python expand_data.py` — **eski `library.db` mavjud bo‘lsa** yangi namunaviy o‘quvchilarni qo‘shadi. Yangi bazada ham ishlaydi.
4. `python app.py` — menyuni ishga tushiradi.
5. `python -m unittest discover -s tests -v` — 12 ta testni bajaradi.

> Eski `library.db` GitHubga yuklanmagan: u mahalliy kompyuterda saqlanadi. Eski ma’lumotlarni saqlash uchun `library.db` faylini yangi `kutubxona_loyiha` papkasiga ko‘chiring va `python expand_data.py` ni bajaring. **Ko‘chirishdan oldin zaxira oling.** Agar yangi papkada `library.db` bo‘lmasa, `python app.py` o‘zi 15 o‘quvchi va 10 kitobli yangi baza yaratadi.

## Menyu

1. Kitoblar va bo‘sh nusxalar; 2. O‘quvchilar; 3. Kitob berish; 4. Qaytarish; 5. O‘quvchi qo‘shish; 6. Kitob qo‘shish; 7. O‘quvchi qidirish; 8. Faol berishlar; 9. Zaxira yaratish; 10. Zaxiradan tiklash; 0. Chiqish.

Kitob berishda `YYYY-MM-DD` formatidagi bugundan oldin bo‘lmagan sanani kiriting. Kitob berilganda chiqarilgan **Berish ID** ni qaytarishda ishlating.

## Baza modeli

- `readers`: o‘quvchilar, telefonlar (takrorlanmaydi)
- `books`: kitoblar, mualliflar, nusxalar
- `loans`: o‘quvchi-kitob bog‘lanishi, berilgan va qaytarilgan sanalar

`schema.sql` — jadvallar va cheklovlar; `sample_data.sql` — namunaviy ma’lumotlar. `library.db` avtomatik yaratiladi va `.gitignore` orqali GitHubga yuklanmaydi.

## DevOps, CI/CD, Tester, DataOps

- **DevOps:** GitHub orqali kod versiyalarini saqlash; `.github/workflows/tests.yml` bilan avtomatlashtirish.
- **CI:** push yoki pull request bo‘lganda Python testlari va sintaksis tekshiruvi ishlaydi.
- **CD (delivery):** `main` ga push bo‘lgach testlar muvaffaqiyatli o‘tsa, GitHub Actions `kutubxona-release.zip` artefaktini yaratadi. Bu **avtomatik yetkazib berish**, serverga deployment emas.
- **Tester:** `tests/test_app.py` da 12 ta avtomatik test: kitoblar, o‘quvchilar, sana tekshiruvi, qarz, qaytarish, qidirish, zaxira va boshqalar.
- **DataOps:** SQLite bazasi, cheklovlar, zaxiralash (`9`) va tiklash (`10`). Tiklash mavjud ma’lumotni almashtiradi — avval zaxira oling.

## Himoyada ko‘rsatish

1. GitHub repository va fayllar.
2. Actions → `Kutubxona CI` → yashil natija va 12 test; `delivery` artefakti.
3. CMD → `python app.py` → 1, 2, 5, 7, 3, 8, 4, 9 menyulari.
4. Sana xatosi: `4` kiritilsa, dastur xatolik beradi.

**Eslatma:** Bu o‘quv loyihasi; autentifikatsiya, ko‘p foydalanuvchili parallel foydalanish va ishlab chiqarish serveriga joylash hali mavjud emas.
