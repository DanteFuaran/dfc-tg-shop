"""Colored Start widget for aiogram-dialog with style support."""
from typing import Optional

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram_dialog.api.entities import Data, ShowMode, StartMode
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Text


class ColoredStart(Start):
    """
    Extended Start widget with color style support.
    
    Available styles:
    - "primary" - 🔵 Blue (main action)
    - "success" - 🟢 Green (confirmation, payment)  
    - "danger" - 🔴 Red (deletion, cancellation)
    - None - ⚪ Default gray
    """

    def __init__(
        self,
        text: Text,
        id: str,
        state: State,
        data: Data = None,
        on_click=None,
        show_mode: Optional[ShowMode] = None,
        mode: StartMode = StartMode.NORMAL,
        when: WhenCondition = None,
        style: Optional[str] = None,
    ):
        super().__init__(
            text=text,
            id=id,
            state=state,
            data=data,
            on_click=on_click,
            show_mode=show_mode,
            mode=mode,
            when=when,
        )
        self.style = style

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        """Render keyboard with style support."""
        btn_kwargs = {
            "text": await self.text.render_text(data, manager),
            "callback_data": self._own_callback_data(),
        }
        # Add style if specified (Telegram Bot API 9.4+)
        if self.style:
            btn_kwargs["style"] = self.style
        
        return [[InlineKeyboardButton(**btn_kwargs)]]
