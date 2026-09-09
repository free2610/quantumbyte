# 🧠 Fika Quiz — Telegram Bot

**Fika Quiz** — Google Gemini AI integratsiyasiga ega bo'lgan, foydalanuvchi tanlagan ixtiyoriy mavzu yoki matn asosida avtomatik testlar tuzuvchi va tayyor fan testlarini (Fizika, Ingliz tili, IT) taqdim etuvchi zamonaviy va professional Telegram bot.

---

## 🌟 Asosiy Imkoniyatlar

- **🧠 Gemini AI Test Generatsiyasi:**
  - Rasmiy `google-genai` asinxron SDK orqali ishlaydi.
  - Ixtiyoriy mavzu yoki matn (maqola/konspekt) asosida 5, 10 yoki 15 talik testlar tuzadi.
  - Qiyinlik darajalari: *Oson*, *O'rtacha*, *Qiyin*.
  - Qat'iy Pydantic validatsiyasi: har bir savolda 4 ta takrorlanmas variant va bitta aniq to'g'ri javob hamda tushuntirish (explanation).
- **📚 Tayyor Fan Testlari:**
  - Fizika, Ingliz tili va IT bo'yicha har birida 10 tadan maxsus saralangan savollar.
  - O'zbek va rus tillarida (jami 60 ta boshlang'ich savol bazaga avtomatik yuklanadi).
  - Gemini kaliti bo'lmaganda ham tayyor testlar 100% to'xtovsiz ishlaydi.
- **🏆 TOP-10 Reytingi:**
  - Faqat umumiy tayyor testlar natijalari bo'yicha adolatli reyting.
  - Har bir foydalanuvchining eng yuqori bali va eng kam sarflagan vaqti hisobga olinadi.
- **📊 Shaxsiy Statistika:**
  - Topshirilgan jami testlar, o'rtacha foiz, eng yaxshi ball va bugungi AI so'rovlari hisobi.
- **🌐 2 Tilli Interfeys:**
  - O'zbekcha (`uz`) va Ruscha (`ru`).
- **👑 Administrator Paneli (`/admin`):**
  - Jami foydalanuvchilar, topshirilgan testlar va AI generatsiyalari statistikasi.
  - Bosqichma-bosqich FSM orqali tayyor testlar bazasiga yangi savol qo'shish va tekshirish.
- **🛡 Xavfsizlik va Barqarorlik:**
  - SQLite (aiosqlite) WAL rejimida va tranzaksiyalar xavfsizligi.
  - Foydalanuvchi bir vaqtda parallel AI so'rov yuborishidan himoya (`asyncio.Lock`).
  - Kunlik AI limiti (standart: 10 ta test).
  - Takroriy bosishdan (double-click) va eski sessiya tugmalaridan himoya.
  - HTML inyeksiya xatolarining oldini olish uchun xavfsiz escape tizimi.

---

## 🚀 O'rnatish va Ishga Tushirish Yo'riqnomasi

### 1. Windows PowerShell'da Virtual Muhit Yaratish

Loyihaning asosiy papkasini oching va virtual muhit (`.venv`) yarating:

```powershell
# Virtual muhit yaratish
python -m venv .venv

# Virtual muhitni faollashtirish
.\.venv\Scripts\Activate.ps1
```

> **Eslatma:** Agar skriptlarni ishga tushirishda ruxsat xatoligi chiqsa, quyidagi buyruqni bajaring:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

### 2. Bog'liqliklarni (Dependencies) O'rnatish

Barcha kerakli kutubxonalarni `requirements.txt` orqali o'rnating:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. BotFather orqali Bot Tokenini Olish

1. Telegramda [@BotFather](https://t.me/BotFather) botiga kiring.
2. `/newbot` buyrug'ini yuboring.
3. Botingizga nom va unikal username tanlang (masalan, `FikaQuizBot`).
4. BotFather sizga taqdim etgan **API Token**ni nusxalab oling (masalan: `123456789:ABCdefGHI...`).

---

### 4. Google AI Studio orqali Gemini API Kalitini Olish

1. [Google AI Studio](https://aistudio.google.com/) saytiga kiring.
2. Google hisobingiz bilan tizimga kiring.
3. **"Get API key"** tugmasini bosing va yangi API kalit yarating (`Create API key`).
4. Berilgan API kalitni nusxalab oling.

---

### 5. `.env` Faylini Sozlash

Loyiha ildizidagi `.env` faylini oching (agar mavjud bo'lmasa, `.env.example` dan nusxa oling) va sozlamalarni kiriting:

```ini
# Telegram Bot Token (BotFather'dan olingan token)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Gemini API kaliti
GEMINI_API_KEY=AIzaSy...

# Gemini modeli (tavsiya etiladi: gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TIMEOUT_SECONDS=60

# Admin Telegram ID lari (o'zingizning Telegram ID'ingizni JSON ro'yxat ko'rinishida yozing)
# Telegram ID'ingizni bilish uchun @userinfobot ga /start bosing.
ADMIN_IDS=[123456789]

# Ma'lumotlar bazasi fayl manzili
DATABASE_PATH=./data/fika_quiz.db

# Standart til
DEFAULT_LANGUAGE=uz

# Foydalanuvchilar uchun kunlik AI test yaratish limiti
AI_DAILY_LIMIT=10

# Log darajasi (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

---

### 6. Botni Ishga Tushirish

Botni quyidagi standart buyruq orqali ishga tushiring:

```powershell
python -m app
```

Yoki to'g'ridan-to'g'ri virtual muhit orqali:

```powershell
.\.venv\Scripts\python.exe -m app
```

Terminalda quyidagiga o'xshash xabarlar ko'rinsa, bot muvaffaqiyatli ishga tushgan hisoblanadi:
```
INFO | app.bot - Fika Quiz boti ishga tushirilmoqda...
INFO | app.bot - Ma'lumotlar bazasi tayyor: ./data/fika_quiz.db
INFO | app.bot - Gemini AI xizmati faollashtirilgan (Model: gemini-2.5-flash)
INFO | app.bot - Bot muvaffaqiyatli ishga tushdi: @FikaQuizBot
INFO | app.bot - Long polling so'rovlari boshlanmoqda...
```

---

### 7. Avtomatik Testlarni Bajarish

Loyiha to'liq birlik (unit) va integratsion testlar bilan qoplangan. Testlarni ishga tushirish:

```powershell
.\.venv\Scripts\pytest -v
```

Natija:
```
======================== 18 passed, 1 warning in 4.37s ========================
```

---

### 8. Ko'p Uchraydigan Xatolar va Yechimlar

| Muammo | Sababi | Yechim |
| :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN sozlanmagan!` | `.env` faylida token bo'sh qolgan yoki `.env` topilmadi | `.env` fayliga BotFather bergan tokeningizni to'g'ri joylashtiring. |
| `Cannot connect to host api.telegram.org` | Internet uzilishi yoki proksi/VPN talab qilinishi | Internet aloqasini tekshiring yoki kerak bo'lsa VPN'ni yoqing. |
| `Gemini 429 quota oshib ketdi` | Bepul Gemini API chegarasiga yetildi | Biroz kuting yoki boshqa Google hisobingizdan yangi API kalit oling. |
| `Ruxsat yo'q (Admin buyrug'i)` | Telegram ID `ADMIN_IDS` ga kiritilmagan | [@userinfobot](https://t.me/userinfobot) orqali o'z ID'ingizni bilib, `.env` faylidagi `ADMIN_IDS=[SIZNING_ID]` qatoriga kiriting va botni qayta ishga tushiring. |
| `Execution of scripts is disabled on this system` | Windows PowerShell xavfsizlik cheklovi | PowerShell'da `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` buyrug'ini bajaring. |

---

## 📁 Loyiha Arxitekturasi

```
telegram bot/
├── .env                 # Maxfiy konfiguratsiyalar
├── .env.example         # Konfiguratsiya namunasi
├── .gitignore           # Git uchun istisnolar
├── requirements.txt     # Python paketlari ro'yxati
├── README.md            # To'liq o'zbekcha qo'llanma
├── app/
│   ├── __init__.py
│   ├── __main__.py      # python -m app chaqiruvi
│   ├── bot.py           # Bot, dispatcher va lifecycle hodisalari
│   ├── config.py        # Pydantic Settings konfiguratsiyasi
│   ├── core/
│   │   ├── database.py  # aiosqlite asinxron DB menejeri
│   │   ├── models.py    # Pydantic ma'lumotlar modellari
│   │   ├── i18n.py      # O'zbek va rus tillari lug'ati
│   │   └── security.py  # HTML escape, sanitization, admin filter
│   ├── services/
│   │   ├── gemini.py    # google-genai SDK orqali AI test generatsiyasi
│   │   ├── quiz_manager.py # Test sessiyalarini boshqarish tizimi
│   │   └── preloaded_data.py # Fizika, Ingliz tili va IT bo'yicha 60 ta savol
│   ├── states/
│   │   └── quiz_states.py # aiogram FSM holatlari (AI test, Admin)
│   ├── keyboards/
│   │   ├── reply.py     # Asosiy menyu klaviaturasi
│   │   └── inline.py    # Variantlar, til va admin inline tugmalari
│   └── handlers/
│       ├── common.py    # /start, /cancel, /help, tilni almashtirish
│       ├── ai_quiz.py   # AI orqali test yaratish va topshirish jarayoni
│       ├── premade_quiz.py # Tayyor fan testlari jarayoni
│       ├── results.py   # Mening natijalarim va TOP-10 reyting
│       └── admin.py     # Admin boshqaruv paneli va savol qo'shish
├── data/
│   └── fika_quiz.db     # SQLite ma'lumotlar bazasi
└── tests/               # 18 ta to'liq avtomatlashtirilgan testlar
```
