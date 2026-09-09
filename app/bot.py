import sys
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.config import settings, setup_logging
from app.core.database import db
from app.handlers import all_routers

logger = logging.getLogger("app.bot")


async def setup_bot_commands(bot: Bot) -> None:
    """Configures command suggestions in Telegram UI."""
    commands = [
        BotCommand(command="start", description="Botni qayta ishga tushirish / Перезапустить"),
        BotCommand(command="cancel", description="Jarayonni bekor qilish / Отмена"),
        BotCommand(command="help", description="Yordam va qo'llanma / Помощь"),
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        logger.warning("Bot komandalarini o'rnatishda ogohlantirish: %s", str(e))


async def on_startup(bot: Bot) -> None:
    """Startup lifecycle hook."""
    logger.info("Fika Quiz boti ishga tushirilmoqda...")
    # Initialize SQLite database
    await db.init_db()
    logger.info("Ma'lumotlar bazasi tayyor: %s", settings.DATABASE_PATH)

    # Check Gemini configuration status
    if settings.has_gemini:
        logger.info("Gemini AI xizmati faollashtirilgan (Model: %s)", settings.GEMINI_MODEL)
    else:
        logger.warning(
            "Diqqat: GEMINI_API_KEY sozlanmagan! Sun'iy intellekt orqali test yaratish funksiyasi o'chiq bo'ladi. "
            "Tayyor testlar (Fizika, Ingliz tili, IT) to'liq ishlashda davom etadi."
        )

    await setup_bot_commands(bot)
    me = await bot.get_me()
    logger.info("Bot muvaffaqiyatli ishga tushdi: @%s (%d)", me.username, me.id)


async def on_shutdown(bot: Bot) -> None:
    """Shutdown lifecycle hook."""
    logger.info("Bot to'xtatilmoqda...")
    await bot.session.close()
    logger.info("Barcha sessiyalar xavfsiz yopildi.")


def create_dispatcher() -> Dispatcher:
    """Creates and configures Dispatcher with routers and lifecycle hooks."""
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Register handlers
    for router in all_routers:
        dp.include_router(router)

    return dp


async def main() -> None:
    """Main entry point for local long-polling execution."""
    setup_logging()

    # Validate Telegram token without leaking secrets
    try:
        settings.validate_bot_token()
    except ValueError as err:
        logger.critical(
            "XATOLIK: %s\nBotni ishga tushirish uchun .env faylida TELEGRAM_BOT_TOKEN parametrini to'ldiring.",
            str(err),
        )
        sys.exit(1)

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = create_dispatcher()

    # Cloud platforms (Render, Railway, Koyeb) support:
    # If $PORT is provided, start a minimal health check endpoint
    port = os.getenv("PORT")
    web_runner = None
    if port:
        try:
            from aiohttp import web

            async def handle_ping(request: web.Request) -> web.Response:
                return web.Response(text="Fika Quiz Telegram Bot is active and running!")

            web_app = web.Application()
            web_app.router.add_get("/", handle_ping)
            web_app.router.add_get("/health", handle_ping)
            web_runner = web.AppRunner(web_app)
            await web_runner.setup()
            site = web.TCPSite(web_runner, "0.0.0.0", int(port))
            await site.start()
            logger.info("Render/Cloud health check server ishga tushirildi (Port: %s)", port)
        except Exception as e:
            logger.warning("Cloud health check serverini ishga tushirishda ogohlantirish: %s", str(e))

    logger.info("Long polling so'rovlari boshlanmoqda...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        if web_runner:
            await web_runner.cleanup()
        await bot.session.close()
