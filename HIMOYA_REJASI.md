# Himoya rejasi (3–5 daqiqa)

Assalomu alaykum. Men 3-mavzu — kutubxona tizimi uchun ma’lumotlar bazasini tanladim. Maqsad — kitoblar, o‘quvchilar va berish-qaytarish amallarini tartibli yuritish. Dastur Python va SQLite asosida yaratilgan.

Bazadagi uchta asosiy jadval: `readers`, `books`, `loans`. Ular o‘quvchi, kitob va kitob berish operatsiyalarini bog‘laydi. Namunaviy bazada 15 nafar o‘quvchi va 10 ta kitob mavjud. Dastur orqali yangi o‘quvchi va kitob qo‘shish, qidirish, berish va qaytarish mumkin.

GitHubdan loyiha fayllarini ko‘rsataman. GitHub Actions har bir kod yangilanishida testlarni avtomatik tekshiradi (CI). Testlar o‘tsa, GitHub yuklab olish uchun ZIP paket yaratadi (CD — delivery). Tester qismi 12 ta avtomatik testdan iborat. DataOps qismida ma’lumotlar bazasining tuzilishi, cheklovlar, zaxiralash va tiklash ko‘rsatilgan.

**Namoyish:** `python app.py` → `2` (o‘quvchilar), `7` (qidirish), `5` (qo‘shish), `1` (kitoblar), `3` (kitob berish), `8` (faol berishlar), `4` (qaytarish), `9` (zaxira).

**Savol-javob:**
- Nega SQLite? Alohida server o‘rnatmasdan kichik loyihada ishlaydi.
- GitHub Actions nima qiladi? Test va paket yaratishni avtomatlashtiradi.
- CI va CD farqi? CI — tekshirish; CD — tekshiruvdan keyin tayyor paketni yetkazish.
- DataOps nima? Ma’lumotlar sifati, saqlanishi va tiklanishiga e’tibor berish.
- Jamoa qayerda? Loyiha yakka tartibda tayyorlangan va yakka himoya qilinadi; rollar haqiqiy jamoa sifatida ko‘rsatilmaydi.

**Muhim:** Himoyada faqat haqiqatan GitHubda bajarilgan testlar natijasini ayting. Yangilangan fayllar yuklangandan keyin Actions natijasini tekshiring.
