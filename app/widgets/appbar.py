"""Единый мобильный AppBar."""
import flet as ft
from app import theme as T

def appbar(title: str, back=None, actions=None, large: bool = False) -> ft.AppBar:
    return ft.AppBar(
        title=ft.Text(
            title,
            color=T.TEXT_PRIMARY,
            size=T.FS_LARGE_TITLE if large else T.FS_TITLE,
            weight=ft.FontWeight.W_700,
        ),
        bgcolor=T.BACKGROUND,
        elevation=0,
        center_title=False,
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
            icon_color=T.PRIMARY,
            icon_size=20,
            on_click=back,
        ) if back else None,
        actions=actions or [],
    )
