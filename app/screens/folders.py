"""Экран 1: Корневые папки."""
import flet as ft
from app import theme as T
from app.demo_data import DEMO_TREE, DEMO_FILES
from app.widgets.appbar import appbar
from app.widgets.cards import empty_state
from app.widgets.dialogs import show_action_sheet


def show_folders(page: ft.Page, on_open_folder, on_delete_folder, on_create_folder, file_picker, navbar: ft.NavigationBar):
    cards = []
    for node in DEMO_TREE:
        sub_count = len(node.get("children", []))
        files_count = len([f for f in DEMO_FILES if f.get("folder_id") == node["id"]])
        meta = []
        if sub_count:
            meta.append(f"папок: {sub_count}")
        if files_count:
            meta.append(f"файлов: {files_count}")
        subtitle = " · ".join(meta) if meta else "Пустая папка"

        cards.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.FOLDER_ROUNDED, color=T.FOLDER_COLOR, size=24),
                        width=44,
                        height=44,
                        bgcolor=T.FOLDER_BG,
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column([
                        ft.Text(node["name"], size=T.FS_BODY, weight=ft.FontWeight.W_600, color=T.TEXT_PRIMARY),
                        ft.Text(subtitle, size=T.FS_SMALL, color=T.TEXT_SECONDARY),
                    ], spacing=2, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                        icon_color=T.TEXT_HINT,
                        icon_size=20,
                        tooltip="Удалить папку",
                        on_click=lambda e, n=node: on_delete_folder(n),
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=T.TEXT_HINT, size=22),
                ], spacing=T.PAD_ROW),
                bgcolor=T.SURFACE,
                border_radius=T.R_CARD,
                padding=T.PAD_CARD,
                margin=ft.Margin.only(bottom=T.GAP),
                on_click=lambda e, n=node: on_open_folder(n),
                ink=True,
                shadow=ft.BoxShadow(blur_radius=10, color=T.SHADOW_SOFT, offset=ft.Offset(0, 2)),
            )
        )

    content = (
        ft.Column(cards, spacing=0, scroll=ft.ScrollMode.AUTO)
        if cards
        else empty_state(ft.Icons.FOLDER_OPEN_ROUNDED, "Папок пока нет.\nНажмите «+», чтобы создать.")
    )

    def open_add_menu(e):
        show_action_sheet(
            page,
            on_create_folder=lambda: on_create_folder(),
            on_upload_file=(lambda: page.run_task(file_picker)) if DEMO_TREE else None,
        )

    view = ft.View(
        route="/",
        padding=0,
        bgcolor=T.BACKGROUND,
        navigation_bar=navbar,
        floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD_ROUNDED,
            bgcolor=T.PRIMARY,
            foreground_color=T.TEXT_ON_PRIMARY,
            shape=ft.CircleBorder(),
            on_click=open_add_menu,
        ),
        controls=[
            appbar("StudeCase", large=True),
            ft.Container(
                content=content,
                expand=True,
                padding=ft.Padding.only(left=T.PAD_SCREEN, right=T.PAD_SCREEN, top=4, bottom=70),
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()
