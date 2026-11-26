"""Виджеты карточек и заглушек."""
import flet as ft
from app import theme as T
from app.widgets.chips import tag_chip

def icon_for_type(file_type: str) -> tuple[str, str, str]:
    return {
        "note":  (ft.Icons.EDIT_NOTE_ROUNDED, T.NOTE_COLOR, T.NOTE_BG),
        "image": (ft.Icons.IMAGE_ROUNDED, T.IMAGE_COLOR, T.IMAGE_BG),
        "pdf":   (ft.Icons.PICTURE_AS_PDF_ROUNDED, T.PDF_COLOR, T.PDF_BG),
        "doc":   (ft.Icons.DESCRIPTION_ROUNDED, T.NOTE_COLOR, T.NOTE_BG),
    }.get(file_type, (ft.Icons.INSERT_DRIVE_FILE_ROUNDED, T.FILE_COLOR, T.FILE_BG))

def file_card(f: dict, on_click, on_delete, on_tag_click) -> ft.Container:
    icon, color, bg_color = icon_for_type(f["type"])
    
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=22),
                    width=42,
                    height=42,
                    bgcolor=bg_color,
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column([
                    ft.Text(
                        f["name"],
                        size=T.FS_BODY,
                        color=T.TEXT_PRIMARY,
                        weight=ft.FontWeight.W_600,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        f["preview"],
                        size=T.FS_SMALL,
                        color=T.TEXT_SECONDARY,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ], spacing=2, expand=True),
                ft.IconButton(
                    icon=ft.Icons.LOCAL_OFFER_OUTLINED,
                    icon_color=T.TEXT_HINT,
                    icon_size=20,
                    tooltip="Теги",
                    on_click=lambda e: on_tag_click(f),
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                    icon_color=T.TEXT_HINT,
                    icon_size=20,
                    tooltip="Удалить",
                    on_click=lambda e: on_delete(f),
                ),
            ], spacing=T.GAP_SM, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            ft.Row(
                [tag_chip(t) for t in f.get("tags", [])] +
                [ft.Text(f["date"], size=T.FS_TINY, color=T.TEXT_HINT)],
                spacing=T.GAP_SM,
                wrap=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ], spacing=T.GAP_SM),
        bgcolor=T.SURFACE,
        border_radius=T.R_CARD,
        padding=T.PAD_CARD,
        margin=ft.Margin.only(bottom=T.GAP),
        on_click=on_click,
        ink=True,
        shadow=ft.BoxShadow(blur_radius=10, color=T.SHADOW_SOFT, offset=ft.Offset(0, 2)),
    )

def empty_state(icon: str, text: str) -> ft.Container:
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(icon, size=48, color=T.TEXT_HINT),
                padding=20,
                bgcolor=T.SURFACE,
                border_radius=50,
            ),
            ft.Text(text, size=T.FS_BODY, color=T.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=T.GAP),
        alignment=ft.Alignment.CENTER,
        padding=48,
    )
