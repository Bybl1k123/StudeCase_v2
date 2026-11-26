"""Экран 3: Просмотр заметки/файла."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.widgets.chips import tag_chip
from app.services.files_service import open_external_file

def show_viewer(page: ft.Page, file: dict, current_folder: dict, on_back, on_review, on_delete, toast):
    file_path = file.get("path")
    
    if file_path and file.get("type") != "note":
        if open_external_file(file_path):
            return
        else:
            toast("Не удалось открыть файл")
            return

    content = file.get("content", "Нет содержимого") if file.get("type") == "note" else f"Этот файл ({file['name']}) не удалось открыть автоматически."

    view = ft.View(
        route="/viewer",
        padding=0,
        bgcolor=T.BACKGROUND,
        controls=[
            appbar(
                file.get("name", "Файл"),
                back=lambda e: on_back(current_folder),
                actions=[
                    ft.IconButton(ft.Icons.SCHOOL_OUTLINED, icon_color=T.PRIMARY, tooltip="Повторить", on_click=lambda e: on_review()),
                ],
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(f'{file.get("type", "Файл").upper()} · {file.get("date", "")}', size=T.FS_TINY, color=T.TEXT_HINT, weight=ft.FontWeight.W_600),
                    ft.Row([tag_chip(t) for t in file.get("tags", [])], wrap=True),
                    ft.Divider(height=1, color=T.DIVIDER),
                    ft.Text(content, size=T.FS_BODY, color=T.TEXT_PRIMARY, selectable=True),
                ], spacing=T.GAP, scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=20,
                bgcolor=T.SURFACE,
                margin=ft.Margin.only(left=T.PAD_SCREEN, right=T.PAD_SCREEN, top=8),
                border_radius=T.R_CARD,
                shadow=ft.BoxShadow(blur_radius=10, color=T.SHADOW_SOFT, offset=ft.Offset(0, 2)),
            ),
            ft.Container(
                content=ft.FilledButton(
                    "Удалить заметку",
                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                    height=48,
                    width=float("inf"),
                    style=ft.ButtonStyle(bgcolor=T.DANGER_BG, color=T.DANGER, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
                    on_click=lambda e: on_delete(file),
                ),
                padding=T.PAD_SCREEN,
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()
