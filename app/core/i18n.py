"""Internationalization module for Uzbek (uz) and Russian (ru) languages."""

MESSAGES: dict[str, dict[str, str]] = {
    "welcome_new": {
        "uz": "Assalomu alaykum! <b>Fika Quiz</b> botiga xush kelibsiz.\n\nIltimos, muloqot tilini tanlang:",
        "ru": "Здравствуйте! Добро пожаловать в бот <b>Fika Quiz</b>.\n\nПожалуйста, выберите язык интерфейса:",
    },
    "welcome_back": {
        "uz": (
            "Assalomu alaykum, <b>{name}</b>! <b>Fika Quiz</b> botiga xush kelibsiz.\n\n"
            "Bu yerda siz Gemini AI yordamida istalgan mavzuda yoki matn asosida testlar yaratishingiz, "
            "tayyor fan testlarini yechishingiz va TOP-10 reytingida bellashishingiz mumkin.\n\n"
            "Quyidagi menyudan kerakli bo'limni tanlang:"
        ),
        "ru": (
            "Здравствуйте, <b>{name}</b>! Добро пожаловать в <b>Fika Quiz</b>.\n\n"
            "Здесь вы можете генерировать тесты на любую тему или по тексту с помощью Gemini AI, "
            "проходить готовые предметные тесты и соревноваться в ТОП-10 рейтинге.\n\n"
            "Выберите нужный раздел в меню ниже:"
        ),
    },
    "main_menu_title": {
        "uz": "Asosiy menyu:",
        "ru": "Главное меню:",
    },
    "btn_ai_quiz": {
        "uz": "🧠 AI test yaratish",
        "ru": "🧠 Создать тест с ИИ",
    },
    "btn_premade_quiz": {
        "uz": "📚 Tayyor testlar",
        "ru": "📚 Готовые тесты",
    },
    "btn_my_results": {
        "uz": "📊 Mening natijalarim",
        "ru": "📊 Мои результаты",
    },
    "btn_leaderboard": {
        "uz": "🏆 TOP-10",
        "ru": "🏆 ТОП-10",
    },
    "btn_change_lang": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Сменить язык",
    },
    "btn_help": {
        "uz": "ℹ️ Yordam",
        "ru": "ℹ️ Помощь",
    },
    "cancel_done": {
        "uz": "❌ Joriy amal bekor qilindi. Asosiy menyudasiz.",
        "ru": "❌ Текущее действие отменено. Вы в главном меню.",
    },
    "lang_changed": {
        "uz": "✅ Til muvaffaqiyatli o'zbek tiliga o'zgartirildi.",
        "ru": "✅ Язык успешно изменен на русский.",
    },
    "select_lang_prompt": {
        "uz": "Iltimos, tilni tanlang:",
        "ru": "Пожалуйста, выберите язык:",
    },
    "help_text": {
        "uz": (
            "ℹ️ <b>Fika Quiz Bot qo'llanmasi</b>\n\n"
            "🔹 <b>🧠 AI test yaratish:</b>\n"
            "O'zingiz xohlagan mavzuni yozing yoki istalgan maqola/matn yuboring. "
            "Gemini AI bir necha soniyada sizga variantli test yaratib beradi.\n\n"
            "🔹 <b>📚 Tayyor testlar:</b>\n"
            "Fizika, Ingliz tili va IT sohalariga oid 10 talik maxsus testlar.\n\n"
            "🔹 <b>🏆 TOP-10:</b>\n"
            "Faqat tayyor testlar bo'yicha eng yuqori ball va eng kam vaqt sarflagan bilimdonlar reytingi.\n\n"
            "🔹 <b>Buyruqlar:</b>\n"
            "/start - Botni qayta ishga tushirish\n"
            "/cancel - Har qanday jarayonni to'xtatish\n\n"
            "⚠️ <i>Eslatma: Sun'iy intellekt (Gemini AI) yaratgan savollarda ba'zida noaniqliklar yoki "
            "kamchiliklar uchrashi mumkin. Agar xatolik sezsangiz, tushunishingizni so'raymiz.</i>"
        ),
        "ru": (
            "ℹ️ <b>Руководство по боту Fika Quiz</b>\n\n"
            "🔹 <b>🧠 Создать тест с ИИ:</b>\n"
            "Напишите любую тему или отправьте текст статьи/конспекта. "
            "Gemini AI за секунды сгенерирует для вас интерактивный тест с вариантами.\n\n"
            "🔹 <b>📚 Готовые тесты:</b>\n"
            "Специальные тесты по 10 вопросов по Физике, Английскому языку и IT.\n\n"
            "🔹 <b>🏆 ТОП-10:</b>\n"
            "Рейтинг лучших участников по готовым тестам (учитываются наивысший балл и наименьшее время).\n\n"
            "🔹 <b>Команды:</b>\n"
            "/start - Перезапустить бота\n"
            "/cancel - Отменить любое текущее действие\n\n"
            "⚠️ <i>Примечание: Вопросы, сгенерированные искусственным интеллектом (Gemini AI), "
            "могут иногда содержать неточности. Пожалуйста, учитывайте это при прохождении.</i>"
        ),
    },
    "active_quiz_exists": {
        "uz": "⚠️ Sizda allaqachon tugallanmagan faol test mavjud!\n\nIltimos, avval uni yakunlang yoki /cancel buyrug'i orqali bekor qiling.",
        "ru": "⚠️ У вас уже есть активный незавершенный тест!\n\nПожалуйста, завершите его или отмените командой /cancel.",
    },
    "ai_mode_select": {
        "uz": "🧠 <b>AI Test yaratish usulini tanlang:</b>\n\n1️⃣ <b>Mavzu bo'yicha:</b> Qisqa mavzu yozasiz (masalan, 'Kvant fizikasi')\n2️⃣ <b>Matn bo'yicha:</b> O'zingiz kiritgan matn/konspekt asosida",
        "ru": "🧠 <b>Выберите способ создания теста с ИИ:</b>\n\n1️⃣ <b>По теме:</b> Вы задаете тему (например, 'Квантовая физика')\n2️⃣ <b>По тексту:</b> На основе отправленного вами текста или статьи",
    },
    "btn_by_topic": {
        "uz": "📝 Mavzu kiritish",
        "ru": "📝 Ввести тему",
    },
    "btn_by_text": {
        "uz": "📄 Matn yuborish",
        "ru": "📄 Отправить текст",
    },
    "prompt_enter_topic": {
        "uz": "Iltimos, test mavzusini kiriting (masalan: <i>Jahon tarixi, Python OOP, Quyosh sistemasi</i>):\n\n<i>Bekor qilish: /cancel</i>",
        "ru": "Пожалуйста, введите тему теста (например: <i>История мира, Python ООП, Солнечная система</i>):\n\n<i>Отмена: /cancel</i>",
    },
    "prompt_enter_text": {
        "uz": "Iltimos, test yaratilishi kerak bo'lgan matnni yuboring (maksimal 3000 belgi):\n\n<i>Bekor qilish: /cancel</i>",
        "ru": "Пожалуйста, отправьте текст, по которому нужно составить тест (максимум 3000 символов):\n\n<i>Отмена: /cancel</i>",
    },
    "text_too_long": {
        "uz": "⚠️ Matn juda uzun ({length} ta belgi). Maksimal ruxsat etilgan uzunlik: 3000 ta belgi. Iltimos, qisqartirib qayta yuboring:",
        "ru": "⚠️ Текст слишком длинный ({length} символов). Максимально допустимо: 3000 символов. Пожалуйста, сократите и отправьте снова:",
    },
    "topic_too_long": {
        "uz": "⚠️ Mavzu nomi juda uzun. Maksimal 200 ta belgi bo'lishi kerak. Qisqaroq qilib qayta kiriting:",
        "ru": "⚠️ Тема слишком длинная. Максимум 200 символов. Введите более короткое название:",
    },
    "select_difficulty": {
        "uz": "Qiyinlik darajasini tanlang:",
        "ru": "Выберите уровень сложности:",
    },
    "diff_easy": {
        "uz": "🟢 Oson",
        "ru": "🟢 Легкий",
    },
    "diff_medium": {
        "uz": "🟡 O'rtacha",
        "ru": "🟡 Средний",
    },
    "diff_hard": {
        "uz": "🔴 Qiyin",
        "ru": "🔴 Сложный",
    },
    "select_count": {
        "uz": "Savollar sonini tanlang:",
        "ru": "Выберите количество вопросов:",
    },
    "ai_generating": {
        "uz": "⏳ <b>Test tayyorlanmoqda...</b>\n\nGemini AI savollarni tuzmoqda, bir necha soniya kuting...",
        "ru": "⏳ <b>Тест готовится...</b>\n\nGemini AI составляет вопросы, подождите несколько секунд...",
    },
    "ai_unavailable": {
        "uz": "❌ Hozirda Gemini AI xizmati sozlanmagan (API kalit kiritilmagan). Siz <b>📚 Tayyor testlar</b> bo'limidan bemalol foydalanishingiz mumkin!",
        "ru": "❌ В данный момент сервис Gemini AI не настроен (ключ API не указан). Вы можете использовать раздел <b>📚 Готовые тесты</b>!",
    },
    "ai_limit_reached": {
        "uz": "⚠️ Sizning kunlik AI test yaratish limitingiz tugadi ({limit}/{limit}). Yangi limit ertaga beriladi. Hozircha tayyor testlarni yechishingiz mumkin!",
        "ru": "⚠️ Ваш дневной лимит тестов с ИИ исчерпан ({limit}/{limit}). Лимит обновится завтра. Пока вы можете решать готовые тесты!",
    },
    "ai_concurrent_request": {
        "uz": "⚠️ Sizda allaqachon generatsiya qilinayotgan so'rov mavjud. Iltimos, u yakunlanishini kuting.",
        "ru": "⚠️ У вас уже выполняется генерация теста. Пожалуйста, дождитесь завершения.",
    },
    "ai_generation_failed": {
        "uz": "❌ Afsuski, test yaratishda vaqtinchalik xatolik yuz berdi. Iltimos, birozdan so'ng boshqa mavzu bilan qayta urinib ko'ring.",
        "ru": "❌ К сожалению, произошла ошибка при генерации теста. Пожалуйста, попробуйте чуть позже или выберите другую тему.",
    },
    "question_progress": {
        "uz": "<b>Savol {current}/{total}</b> | <i>{topic}</i>",
        "ru": "<b>Вопрос {current}/{total}</b> | <i>{topic}</i>",
    },
    "answer_correct": {
        "uz": "✅ <b>To'g'ri javob!</b>\n\n💡 <b>Izoh:</b> {explanation}",
        "ru": "✅ <b>Правильный ответ!</b>\n\n💡 <b>Пояснение:</b> {explanation}",
    },
    "answer_incorrect": {
        "uz": "❌ <b>Noto'g'ri!</b>\nTo'g'ri javob: <b>{correct_opt}</b>\n\n💡 <b>Izoh:</b> {explanation}",
        "ru": "❌ <b>Неправильно!</b>\nПравильный ответ: <b>{correct_opt}</b>\n\n💡 <b>Пояснение:</b> {explanation}",
    },
    "btn_next_question": {
        "uz": "Keyingi savol ➡️",
        "ru": "Следующий вопрос ➡️",
    },
    "btn_finish_quiz": {
        "uz": "Natijani ko'rish 🏁",
        "ru": "Завершить и узнать результат 🏁",
    },
    "already_answered": {
        "uz": "Bu savolga allaqachon javob berdingiz!",
        "ru": "Вы уже ответили на этот вопрос!",
    },
    "quiz_completed_title": {
        "uz": "🎉 <b>Test yakunlandi!</b>",
        "ru": "🎉 <b>Тест завершен!</b>",
    },
    "quiz_results_summary": {
        "uz": (
            "🎉 <b>Test yakunlandi!</b>\n\n"
            "📋 <b>Mavzu:</b> {topic}\n"
            "✅ <b>To'g'ri javoblar:</b> {correct} ta\n"
            "❌ <b>Noto'g'ri javoblar:</b> {incorrect} ta\n"
            "📊 <b>Natija:</b> {percent}%\n"
            "⏱ <b>Sarflangan vaqt:</b> {time_str}"
        ),
        "ru": (
            "🎉 <b>Тест завершен!</b>\n\n"
            "📋 <b>Тема:</b> {topic}\n"
            "✅ <b>Правильных ответов:</b> {correct}\n"
            "❌ <b>Неправильных ответов:</b> {incorrect}\n"
            "📊 <b>Результат:</b> {percent}%\n"
            "⏱ <b>Затраченное время:</b> {time_str}"
        ),
    },
    "btn_view_errors": {
        "uz": "❌ Xatolarni ko'rish",
        "ru": "❌ Посмотреть ошибки",
    },
    "btn_new_quiz": {
        "uz": "🔄 Yangi test",
        "ru": "🔄 Новый тест",
    },
    "btn_home": {
        "uz": "🏠 Asosiy menyu",
        "ru": "🏠 Главное меню",
    },
    "no_errors_to_show": {
        "uz": "👏 Ajoyib natija! Siz barcha savollarga to'g'ri javob berdingiz, hech qanday xato yo'q!",
        "ru": "👏 Отличный результат! Вы ответили правильно на все вопросы, ошибок нет!",
    },
    "error_review_item": {
        "uz": (
            "<b>{num}-savol:</b> {question}\n"
            "❌ Sizning javobingiz: {user_ans}\n"
            "✅ To'g'ri javob: {correct_ans}\n"
            "💡 Izoh: {explanation}\n"
        ),
        "ru": (
            "<b>Вопрос {num}:</b> {question}\n"
            "❌ Ваш ответ: {user_ans}\n"
            "✅ Правильный ответ: {correct_ans}\n"
            "💡 Пояснение: {explanation}\n"
        ),
    },
    "premade_select_category": {
        "uz": "📚 <b>Tayyor fan testlari:</b>\n\nTest topshirmoqchi bo'lgan faningizni tanlang (har bir testda 10 ta savol):",
        "ru": "📚 <b>Готовые предметные тесты:</b>\n\nВыберите предмет для прохождения теста (в каждом тесте по 10 вопросов):",
    },
    "cat_physics": {
        "uz": "🧲 Fizika",
        "ru": "🧲 Физика",
    },
    "cat_english": {
        "uz": "🇬🇧 Ingliz tili",
        "ru": "🇬🇧 Английский язык",
    },
    "cat_it": {
        "uz": "💻 IT va Dasturlash",
        "ru": "💻 IT и Программирование",
    },
    "premade_no_questions": {
        "uz": "Ushbu fan bo'yicha hozircha savollar topilmadi.",
        "ru": "По данному предмету пока нет вопросов.",
    },
    "leaderboard_title": {
        "uz": "🏆 <b>Tayyor testlar bo'yicha TOP-10 bilimdonlar:</b>\n\n<i>Reyting qoidasi: har bir foydalanuvchining eng yuqori bali va eng kam sarflangan vaqti olinadi.</i>\n\n",
        "ru": "🏆 <b>ТОП-10 знатоков по готовым тестам:</b>\n\n<i>Правило рейтинга: учитывается лучший балл пользователя и наименьшее время.</i>\n\n",
    },
    "leaderboard_empty": {
        "uz": "Hozircha hech kim tayyor testlarni yakunlamagan. Siz birinchi bo'lishingiz mumkin!",
        "ru": "Пока никто не завершил готовые тесты. Вы можете стать первым!",
    },
    "my_results_title": {
        "uz": (
            "📊 <b>Mening natijalarim:</b>\n\n"
            "👤 <b>Foydalanuvchi:</b> {name}\n"
            "📝 <b>Jami topshirilgan testlar:</b> {total_quizzes} ta\n"
            "🧠 <b>AI testlar:</b> {ai_quizzes} ta\n"
            "📚 <b>Tayyor testlar:</b> {premade_quizzes} ta\n"
            "🎯 <b>O'rtacha ko'rsatkich:</b> {avg_score}%\n"
            "⭐ <b>Eng yuqori ball (tayyor testlar):</b> {best_score} ta\n"
            "⚡ <b>Bugungi AI limiti:</b> {ai_used}/{ai_limit} ta ishlatildi\n"
        ),
        "ru": (
            "📊 <b>Мои результаты:</b>\n\n"
            "👤 <b>Пользователь:</b> {name}\n"
            "📝 <b>Всего пройдено тестов:</b> {total_quizzes}\n"
            "🧠 <b>Тестов с ИИ:</b> {ai_quizzes}\n"
            "📚 <b>Готовых тестов:</b> {premade_quizzes}\n"
            "🎯 <b>Средний результат:</b> {avg_score}%\n"
            "⭐ <b>Лучший балл (готовые тесты):</b> {best_score}\n"
            "⚡ <b>Сегодняшний лимит ИИ:</b> использовано {ai_used}/{ai_limit}\n"
        ),
    },
    "admin_access_denied": {
        "uz": "⛔️ Kechirasiz, bu buyruq faqat bot administratorlari uchun ruxsat etilgan.",
        "ru": "⛔️ Извините, эта команда доступна только администраторам бота.",
    },
    "admin_panel_title": {
        "uz": (
            "👑 <b>Admin boshqaruv paneli</b>\n\n"
            "👥 <b>Jami foydalanuvchilar:</b> {users_count} ta\n"
            "🏁 <b>Jami yakunlangan testlar:</b> {quizzes_count} ta\n"
            "🧠 <b>AI orqali yaratilgan testlar:</b> {ai_count} ta\n"
            "📚 <b>Mavjud tayyor savollar:</b> {premade_count} ta\n"
        ),
        "ru": (
            "👑 <b>Панель администратора</b>\n\n"
            "👥 <b>Всего пользователей:</b> {users_count}\n"
            "🏁 <b>Всего завершенных тестов:</b> {quizzes_count}\n"
            "🧠 <b>Тестов, созданных с ИИ:</b> {ai_count}\n"
            "📚 <b>Готовых вопросов в базе:</b> {premade_count}\n"
        ),
    },
    "btn_admin_add_question": {
        "uz": "➕ Yangi savol qo'shish",
        "ru": "➕ Добавить новый вопрос",
    },
    "btn_admin_refresh": {
        "uz": "🔄 Yangilash",
        "ru": "🔄 Обновить",
    },
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    """Returns localized message string formatted with kwargs."""
    if lang not in ("uz", "ru"):
        lang = "uz"
    entry = MESSAGES.get(key)
    if not entry:
        return key
    text = entry.get(lang) or entry.get("uz") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def format_seconds(seconds: int, lang: str = "uz") -> str:
    """Formats seconds into user-friendly minutes and seconds string."""
    mins = seconds // 60
    secs = seconds % 60
    if lang == "ru":
        if mins > 0:
            return f"{mins} мин. {secs} сек."
        return f"{secs} сек."
    if mins > 0:
        return f"{mins} daq. {secs} son."
    return f"{secs} son."
