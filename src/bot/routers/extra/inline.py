from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from loguru import logger

router = Router(name=__name__)


@router.inline_query()
async def on_invite_inline(query: InlineQuery) -> None:
    """Handle inline query from mini-app switchInlineQuery (invite friend flow)."""
    text = (query.query or "").strip()
    if not text:
        await query.answer([], cache_time=1)
        return

    preview = text[:80] + ("…" if len(text) > 80 else "")
    result = InlineQueryResultArticle(
        id="invite",
        title="📨 Отправить приглашение",
        description=preview,
        input_message_content=InputTextMessageContent(message_text=text),
    )
    logger.debug(f"Inline invite query from user {query.from_user.id}")
    await query.answer([result], cache_time=1, is_personal=True)
