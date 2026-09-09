"""Preloaded curated quiz questions for Physics, English, and IT in Uzbek and Russian."""

PRELOADED_QUESTIONS = [
    # ------------------ FIZIKA / ФИЗИКА (UZBEK) ------------------
    {
        "category": "physics",
        "lang": "uz",
        "question": "Nyutonning ikkinchi qonuni qaysi formula bilan ifodalanadi?",
        "options": ["F = m * a", "E = m * c²", "P = U * I", "v = s / t"],
        "correct_index": 0,
        "explanation": "Nyutonning ikkinchi qonuniga ko'ra, jismga ta'sir qiluvchi kuch uning massasi va tezlanishi ko'paytmasiga teng (F = m * a)."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Yorug'likning vakuumdagi tezligi taxminan qanchaga teng?",
        "options": ["300 000 km/s", "150 000 km/s", "30 000 km/s", "3 000 km/s"],
        "correct_index": 0,
        "explanation": "Yorug'likning vakuumdagi tezligi universal doimiy kattalik bo'lib, taxminan 300 000 km/s (3 * 10^8 m/s) ga teng."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Elektr toki kuchi qaysi birlikda o'lchanadi?",
        "options": ["Amper", "Volt", "Om", "Vatt"],
        "correct_index": 0,
        "explanation": "Xalqaro birliklar sistemasida (SI) tok kuchi Amper (A) bilan o'lchanadi."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Erkin tushish tezlanishi (g) ning Yerdagi o'rtacha qiymati qancha?",
        "options": ["9.8 m/s²", "10.5 m/s²", "8.9 m/s²", "12.0 m/s²"],
        "correct_index": 0,
        "explanation": "Yer sirtida erkin tushish tezlanishi o'rtacha 9.8 m/s² (taxminan 9.81 m/s²) ga teng."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Ohm qonuniga ko'ra, zanjir qismidagi tok kuchi (I) qanday topiladi?",
        "options": ["I = U / R", "I = U * R", "I = R / U", "I = U² * R"],
        "correct_index": 0,
        "explanation": "Zanjir qismi uchun Ohm qonuni: I = U / R, ya'ni tok kuchi kuchlanishga to'g'ri, qarshilikka teskari mutanosib."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Termodinamikaning birinchi qonuni qaysi fundamental qonunning ifodasidir?",
        "options": ["Energiyaning saqlanish qonuni", "Inersiya qonuni", "Arximed qonuni", "Paskal qonuni"],
        "correct_index": 0,
        "explanation": "Termodinamikaning birinchi qonuni issiqlik jarayonlarida energiyaning saqlanish va aylanish qonunidir."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Suyuqlik yoki gazga botirilgan jismga ta'sir qiluvchi itaruvchi kuch qanday ataladi?",
        "options": ["Arximed kuchi", "Ishqalanish kuchi", "Gravitatsiya kuchi", "Kulon kuchi"],
        "correct_index": 0,
        "explanation": "Suyuqlik yoki gaz ichidagi jismga pastdan yuqoriga yo'nalgan itaruvchi kuch Arximed kuchi deyiladi."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Kinetik energiyani hisoblash formulasi qaysi?",
        "options": ["E = (m * v²) / 2", "E = m * g * h", "E = k * x² / 2", "E = F * s"],
        "correct_index": 0,
        "explanation": "Harakatdagi jismning kinetik energiyasi uning massasi va tezligi kvadratining yarmiga teng: E_k = (m * v²) / 2."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Qaysi zarracha manfiy elementar elektr zaryadiga ega?",
        "options": ["Elektron", "Proton", "Neytron", "Foton"],
        "correct_index": 0,
        "explanation": "Elektron manfiy (-1.6 * 10^-19 Kl), proton musbat zaryadga ega, neytron esa neytraldir."
    },
    {
        "category": "physics",
        "lang": "uz",
        "question": "Tovush to'lqinlari qaysi muhitda tarqala olmaydi?",
        "options": ["Vakuumda", "Suvda", "Temirda", "Havoda"],
        "correct_index": 0,
        "explanation": "Tovush mexanik to'lqin bo'lganligi sababli uning tarqalishi uchun moddiy muhit zarur. Vakuumda modda bo'lmagani uchun tovush tarqala olmaydi."
    },

    # ------------------ FIZIKA / ФИЗИКА (RUSSIAN) ------------------
    {
        "category": "physics",
        "lang": "ru",
        "question": "Какой формулой выражается второй закон Ньютона?",
        "options": ["F = m * a", "E = m * c²", "P = U * I", "v = s / t"],
        "correct_index": 0,
        "explanation": "Второй закон Ньютона гласит: сила равна произведению массы тела на его ускорение (F = m * a)."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "Чему примерно равна скорость света в вакууме?",
        "options": ["300 000 км/с", "150 000 км/с", "30 000 км/с", "3 000 км/с"],
        "correct_index": 0,
        "explanation": "Скорость света в вакууме — фундаментальная физическая постоянная, равная примерно 300 000 км/с."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "В каких единицах в системе СИ измеряется сила электрического тока?",
        "options": ["Ампер", "Вольт", "Ом", "Ватт"],
        "correct_index": 0,
        "explanation": "В Международной системе единиц (СИ) сила тока измеряется в Амперах (А)."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "Каково среднее значение ускорения свободного падения (g) на Земле?",
        "options": ["9.8 м/с²", "10.5 м/с²", "8.9 м/с²", "12.0 м/с²"],
        "correct_index": 0,
        "explanation": "У поверхности Земли ускорение свободного падения в среднем составляет 9.8 м/с²."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "Как согласно закону Ома для участка цепи определяется сила тока (I)?",
        "options": ["I = U / R", "I = U * R", "I = R / U", "I = U² * R"],
        "correct_index": 0,
        "explanation": "Закон Ома для участка цепи: сила тока прямо пропорциональна напряжению и обратно пропорциональна сопротивлению (I = U / R)."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "Проявлением какого фундаментального закона является первый закон термодинамики?",
        "options": ["Закон сохранения энергии", "Закон инерции", "Закон Архимеда", "Закон Паскаля"],
        "correct_index": 0,
        "explanation": "Первый закон термодинамики представляет собой закон сохранения и превращения энергии в тепловых процессах."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "Как называется выталкивающая сила, действующая на погруженное в жидкость или газ тело?",
        "options": ["Сила Архимеда", "Сила трения", "Сила тяжести", "Сила Кулона"],
        "correct_index": 0,
        "explanation": "Выталкивающая сила, действующая на погруженное в жидкость или газ тело, называется силой Архимеда."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "Какая формула используется для вычисления кинетической энергии тела?",
        "options": ["E = (m * v²) / 2", "E = m * g * h", "E = k * x² / 2", "E = F * s"],
        "correct_index": 0,
        "explanation": "Кинетическая энергия движущегося тела рассчитывается по формуле: E = (m * v²) / 2."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "Какая из элементарных частиц обладает отрицательным зарядом?",
        "options": ["Электрон", "Протон", "Нейтрон", "Фотон"],
        "correct_index": 0,
        "explanation": "Электрон заряжен отрицательно (-1.6 * 10^-19 Кл), протон — положительно, а нейтрон нейтрален."
    },
    {
        "category": "physics",
        "lang": "ru",
        "question": "В какой среде звуковые волны не могут распространяться?",
        "options": ["В вакууме", "В воде", "В железе", "В воздухе"],
        "correct_index": 0,
        "explanation": "Звук — это механическая волна, требующая упругой среды. В вакууме нет частиц, поэтому звук там не распространяется."
    },

    # ------------------ INGLIZ TILI / АНГЛИЙСКИЙ (UZBEK) ------------------
    {
        "category": "english",
        "lang": "uz",
        "question": "Qaysi gapda Present Perfect zamoni to'g'ri qo'llangan?",
        "options": [
            "She has lived in London for three years.",
            "She have lived in London yesterday.",
            "She is lived in London since Monday.",
            "She has living in London now."
        ],
        "correct_index": 0,
        "explanation": "'She' olmoshi bilan 'has' va fe'lning 3-shakli (V3 - lived) ishlatiladi: 'She has lived in London for three years.'"
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "'Cautious' so'zining sinonimi qaysi?",
        "options": ["Careful", "Dangerous", "Brave", "Rapid"],
        "correct_index": 0,
        "explanation": "'Cautious' so'zi ehtiyotkor, hushyor ma'nosini bildiradi va uning eng to'g'ri sinonimi 'Careful' hisoblanadi."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "To'g'ri modal fe'lni tanlang: 'You ______ wear a helmet when riding a motorcycle. It is the law.'",
        "options": ["must", "might", "could", "should not"],
        "correct_index": 0,
        "explanation": "Qonuniy qat'iy majburiyat yoki qoidalar uchun 'must' modal fe'li qo'llaniladi."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "Qaysi so'z 'child' so'zining ko'plik shakli?",
        "options": ["children", "childs", "childrens", "childes"],
        "correct_index": 0,
        "explanation": "'Child' noto'g'ri o'zgaruvchi ot bo'lib, ko'plik shakli 'children' bo'ladi."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "Bo'sh o'rinni to'ldiring: 'If I ______ enough money, I would travel around the world.'",
        "options": ["had", "have", "will have", "would have"],
        "correct_index": 0,
        "explanation": "Second Conditional (norasmiy/orzudagi shart mayli): If + Past Simple (had), would + bare infinitive."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "'Give up' iboraviy fe'li (phrasal verb) qanday ma'noni anglatadi?",
        "options": ["To'xtatmoq, voz kechmoq", "Hadyo qilmoq", "Boshlamoq", "Qidirmoq"],
        "correct_index": 0,
        "explanation": "'Give up' biror narsani tashlamoq, chekinmoq yoki undan voz kechmoq (surrender/quit) ma'nosida keladi."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "Qaysi predlog to'g'ri keladi: 'I am interested ______ modern technology.'?",
        "options": ["in", "at", "on", "about"],
        "correct_index": 0,
        "explanation": "'Interested' sifatidan keyin har doim 'in' predlogi ishlatiladi (interested in something)."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "'Go' fe'lining o'tgan zamon (Past Simple) shakli qaysi?",
        "options": ["went", "gone", "goed", "goes"],
        "correct_index": 0,
        "explanation": "'Go' noto'g'ri fe'li: go - went - gone. Past Simple shakli 'went'."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "Qaysi biri 'abundant' so'ziga antonim (qarama-qarshi ma'noli)?",
        "options": ["Scarce", "Plentiful", "Rich", "Huge"],
        "correct_index": 0,
        "explanation": "'Abundant' serob, mo'l-ko'l degani. Uning antonimi 'Scarce' (taqchil, kamyob)."
    },
    {
        "category": "english",
        "lang": "uz",
        "question": "To'g'ri nisbiy olmoshni tanlang: 'The book ______ you lent me was amazing.'",
        "options": ["which", "who", "whom", "whose"],
        "correct_index": 0,
        "explanation": "Jonsiz buyumlar (The book) uchun 'which' yoki 'that' qo'llaniladi."
    },

    # ------------------ INGLIZ TILI / АНГЛИЙСКИЙ (RUSSIAN) ------------------
    {
        "category": "english",
        "lang": "ru",
        "question": "В каком предложении правильно использовано время Present Perfect?",
        "options": [
            "She has lived in London for three years.",
            "She have lived in London yesterday.",
            "She is lived in London since Monday.",
            "She has living in London now."
        ],
        "correct_index": 0,
        "explanation": "С местоимением 'She' используется вспомогательный глагол 'has' и 3-я форма глагола: 'She has lived...'."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Какой синоним у слова 'Cautious'?",
        "options": ["Careful", "Dangerous", "Brave", "Rapid"],
        "correct_index": 0,
        "explanation": "'Cautious' переводится как 'осторожный, осмотрительный'. Его прямой синоним — 'Careful'."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Выберите подходящий модальный глагол: 'You ______ wear a helmet when riding a motorcycle. It is the law.'",
        "options": ["must", "might", "could", "should not"],
        "correct_index": 0,
        "explanation": "Для выражения строгой обязанности или закона используется модальный глагол 'must'."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Какая форма множественного числа у слова 'child'?",
        "options": ["children", "childs", "childrens", "childes"],
        "correct_index": 0,
        "explanation": "Слово 'child' — исключение. Множественное число образуется как 'children'."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Заполните пропуск: 'If I ______ enough money, I would travel around the world.'",
        "options": ["had", "have", "will have", "would have"],
        "correct_index": 0,
        "explanation": "Second Conditional (нереальное условие в настоящем): If + Past Simple (had), would + глагол."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Что означает фразовый глагол 'Give up'?",
        "options": ["Сдаваться, бросать", "Дарить", "Начинать", "Искать"],
        "correct_index": 0,
        "explanation": "'Give up' означает сдаться, прекратить попытки или бросить какую-либо привычку."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Какой предлог употребляется с прилагательным 'interested': 'I am interested ______ modern technology.'?",
        "options": ["in", "at", "on", "about"],
        "correct_index": 0,
        "explanation": "Устойчивая конструкция в английском языке: to be interested in something (интересоваться чем-либо)."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Какова форма прошедшего времени (Past Simple) неправильного глагола 'go'?",
        "options": ["went", "gone", "goed", "goes"],
        "correct_index": 0,
        "explanation": "Формы неправильного глагола: go — went — gone. Во времени Past Simple используется 'went'."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Что является антонимом к слову 'Abundant' (изобильный)?",
        "options": ["Scarce", "Plentiful", "Rich", "Huge"],
        "correct_index": 0,
        "explanation": "'Abundant' означает обильный, богатый. Антонимом является 'Scarce' (скудный, дефицитный)."
    },
    {
        "category": "english",
        "lang": "ru",
        "question": "Выберите правильное относительное местоимение: 'The book ______ you lent me was amazing.'",
        "options": ["which", "who", "whom", "whose"],
        "correct_index": 0,
        "explanation": "Для неодушевленных предметов (the book) в придаточных предложениях используется 'which' или 'that'."
    },

    # ------------------ IT VA DASTURLASH / IT (UZBEK) ------------------
    {
        "category": "it",
        "lang": "uz",
        "question": "Python dasturlash tilida qaysi ma'lumot turi o'zgarmas (immutable) hisoblanadi?",
        "options": ["tuple", "list", "dict", "set"],
        "correct_index": 0,
        "explanation": "Pythonda tuple (kortej), int, float, str kabilar immutable (o'zgarmas), list, dict, set esa mutable (o'zgaruvchan) hisoblanadi."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "HTTP protokoli bo'yicha 404 xatolik kodi nimani bildiradi?",
        "options": ["Not Found (Resurs topilmadi)", "Unauthorized (Ruxsat yo'q)", "Internal Server Error", "Bad Request"],
        "correct_index": 0,
        "explanation": "404 Not Found — so'ralgan resurs yoki sahifa serverda topilmaganligini anglatadi."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "Ma'lumotlar bazasida Birlamchi kalit (Primary Key) ning asosiy vazifasi nima?",
        "options": [
            "Har bir qatorni yagona identifikatsiya qilish",
            "Jadvaldagi yozuvlarni shifrlash",
            "Barcha matnlarni katta harfga o'tkazish",
            "Fayllarni diskka nusxalash"
        ],
        "correct_index": 0,
        "explanation": "Primary Key jadvalning har bir yozuvini (qatorini) yagona va takrorlanmas tarzda aniqlash uchun xizmat qiladi."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "Git tizimida yangi o'zgarishlarni mahalliy omborga (repository) qayd qilish uchun qaysi buyruq ishlatiladi?",
        "options": ["git commit", "git push", "git pull", "git clone"],
        "correct_index": 0,
        "explanation": "'git commit' o'zgarishlarni mahalliy commit sifatida saqlaydi, 'git push' esa ularni masofaviy serverga yuklaydi."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "Binary Search (ikkilik qidiruv) algoritmining vaqt bo'yicha murakkabligi (Big-O) qancha?",
        "options": ["O(log n)", "O(n)", "O(n²)", "O(1)"],
        "correct_index": 0,
        "explanation": "Tartiblangan massivda ikkilik qidiruv har qadamda qidiruv sohasini 2 marta qisqartiradi, shuning uchun uning murakkabligi O(log n)."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "OSI (Open Systems Interconnection) modelida jami nechta pog'ona (layer) mavjud?",
        "options": ["7 ta", "4 ta", "5 ta", "8 ta"],
        "correct_index": 0,
        "explanation": "OSI modeli 7 ta pog'onadan iborat: Physical, Data Link, Network, Transport, Session, Presentation, Application."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "SQL so'rovida qatorlarni filtrlash uchun qaysi kalit so'z ishlatiladi?",
        "options": ["WHERE", "ORDER BY", "GROUP BY", "SELECT"],
        "correct_index": 0,
        "explanation": "SQL tilida shart bo'yicha ma'lumotlarni saralab (filtrlab) olish uchun WHERE bandi qo'llaniladi."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "Dasturlashda FIFO (First-In, First-Out) tamoyili qaysi ma'lumotlar tuzilmasiga xos?",
        "options": ["Queue (Navbat)", "Stack (Stek)", "Tree (Daraxt)", "Graph (Graf)"],
        "correct_index": 0,
        "explanation": "Queue (navbat) birinchi kelgan birinchi chiqadigan (FIFO) tuzilmadir. Stack esa LIFO (Last-In, First-Out) tamoyilida ishlaydi."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "Web brauzerlarda interaktivlik va sahifaning dinamik ishlashini ta'minlovchi asosiy dasturlash tili qaysi?",
        "options": ["JavaScript", "Python", "C++", "SQL"],
        "correct_index": 0,
        "explanation": "Barcha zamonaviy veb-brauzerlar mijoz tomonidagi (frontend) interaktivlik uchun JavaScript tilini bajaradi."
    },
    {
        "category": "it",
        "lang": "uz",
        "question": "Asinxron dasturlashda (masalan, Python asyncio) 'coroutine'ni kutish uchun qaysi kalit so'z ishlatiladi?",
        "options": ["await", "yield", "defer", "promise"],
        "correct_index": 0,
        "explanation": "Python asinxron dasturlashda asinxron funksiya natijasini kutib olish uchun 'await' kalit so'zi yoziladi."
    },

    # ------------------ IT VA DASTURLASH / IT (RUSSIAN) ------------------
    {
        "category": "it",
        "lang": "ru",
        "question": "Какой из типов данных в языке Python является неизменяемым (immutable)?",
        "options": ["tuple", "list", "dict", "set"],
        "correct_index": 0,
        "explanation": "В Python кортежи (tuple), числа и строки являются неизменяемыми (immutable), а списки, словари и множества — изменяемыми."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Что означает HTTP статус-код ошибки 404?",
        "options": ["Not Found (Ресурс не найден)", "Unauthorized (Не авторизован)", "Internal Server Error", "Bad Request"],
        "correct_index": 0,
        "explanation": "Код 404 Not Found сообщает клиенту, что запрашиваемый ресурс или веб-страница не найдены на сервере."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Каково основное назначение первичного ключа (Primary Key) в реляционной базе данных?",
        "options": [
            "Уникальная идентификация каждой строки таблицы",
            "Шифрование данных таблицы",
            "Перевод текста в верхний регистр",
            "Резервное копирование таблицы"
        ],
        "correct_index": 0,
        "explanation": "Первичный ключ гарантирует уникальность каждой записи (строки) в таблице реляционной базы данных."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Какая команда Git используется для фиксации подготовленных изменений в локальном репозитории?",
        "options": ["git commit", "git push", "git pull", "git clone"],
        "correct_index": 0,
        "explanation": "Команда 'git commit' фиксирует изменения в локальной истории репозитория."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Какова временная сложность (Big-O) алгоритма бинарного поиска (Binary Search)?",
        "options": ["O(log n)", "O(n)", "O(n²)", "O(1)"],
        "correct_index": 0,
        "explanation": "Бинарный поиск делит диапазон поиска пополам на каждой итерации, обеспечивая сложность O(log n)."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Сколько уровней (слоев) содержит эталонная модель взаимодействия открытых систем (OSI)?",
        "options": ["7", "4", "5", "8"],
        "correct_index": 0,
        "explanation": "Модель OSI состоит из 7 уровней: физический, канальный, сетевой, транспортный, сеансовый, представления и прикладной."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Какое ключевое слово в SQL используется для фильтрации строк по заданному условию?",
        "options": ["WHERE", "ORDER BY", "GROUP BY", "SELECT"],
        "correct_index": 0,
        "explanation": "В SQL условие выборки и фильтрация строк задаются с помощью оператора WHERE."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Для какой структуры данных характерен принцип FIFO (First-In, First-Out)?",
        "options": ["Очередь (Queue)", "Стек (Stack)", "Дерево (Tree)", "Граф (Graph)"],
        "correct_index": 0,
        "explanation": "Очередь работает по принципу FIFO (первым пришел — первым ушел). Стек работает по принципу LIFO."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Какой язык программирования является основным для обеспечения динамичности и интерактивности в веб-браузерах?",
        "options": ["JavaScript", "Python", "C++", "SQL"],
        "correct_index": 0,
        "explanation": "JavaScript является стандартом клиентской разработки во всех современных браузерах."
    },
    {
        "category": "it",
        "lang": "ru",
        "question": "Какое ключевое слово в Python (asyncio) используется для ожидания выполнения корутины?",
        "options": ["await", "yield", "defer", "promise"],
        "correct_index": 0,
        "explanation": "Ключевое слово 'await' приостанавливает выполнение текущей асинхронной функции до завершения корутины."
    },
]
