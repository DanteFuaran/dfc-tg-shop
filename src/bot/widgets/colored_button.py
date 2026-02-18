"""Colored Button widgets for aiogram-dialog with style support."""
from typing import Optional, Union

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram_dialog.api.entities import ShowMode
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Text


class ColoredButton(Button):
    """
    Extended Button widget with color style support.
    
    Available styles:
    - "success" - 🟢 Green (confirmation, payment)  
    - "danger" - 🔴 Red (deletion, cancellation)
    - "primary" - 🔵 Blue (main action)
    - None - ⚪ Default gray
    """

    def __init__(
        self,
        text: Text,
        id: str,
        on_click=None,
        when: WhenCondition = None,
        style: Optional[str] = None,
    ):
        super().__init__(
            text=text,
            id=id,
            on_click=on_click,
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
        if self.style:
            btn_kwargs["style"] = self.style
        
        return [[InlineKeyboardButton(**btn_kwargs)]]


class ColoredSwitchTo(SwitchTo):
    """
    Extended SwitchTo widget with color style support.
    
    Available styles:
    - "success" - 🟢 Green (confirmation, payment)  
    - "danger" - 🔴 Red (deletion, cancellation)
    - "primary" - 🔵 Blue (main action)
    - None - ⚪ Default gray
    """

    def __init__(
        self,
        text: Text,
        id: str,
        state: State,
        on_click=None,
        show_mode: Optional[ShowMode] = None,
        when: WhenCondition = None,
        style: Optional[str] = None,
    ):
        super().__init__(
            text=text,
            id=id,
            state=state,
            on_click=on_click,
            show_mode=show_mode,
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
        if self.style:
            btn_kwargs["style"] = self.style
        
        return [[InlineKeyboardButton(**btn_kwargs)]]
