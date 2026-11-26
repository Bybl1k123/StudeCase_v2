"""Экран 2: Список файлов и подпапок в папке."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.widgets.cards import file_card, empty_state
from app.demo_data import DEMO_FILES, DEMO_TREE
from app.widgets.dialogs import show_create_note_dialog, show_action_sheet


def find_folder_in_tree(nodes: list, target_id: int) -> dict | None:
    for n in nodes:
        if n["id"] == target_id:
            return n
        found = find_folder_in_tree(n.get("children", []), target_id)
        if found:
            return found
    return None


def show_files(
    page: ft.Page, folder: dict, on_back, on_open_folder,
    on_delete_folder, on_view_file, on_delete_file, on_create_note,
    on_create_folder, on_edit_tags, file_picker, navbar: ft.NavigationBar
):
    folder_id = folder.get("id")
    current_node = find_folder_in_tree(DEMO_TREE, folder_id) or folder
    subfolders = current_node.get("children", [])
    files = [f for f in DEMO_FILES if f.get("folder_id") == folder_id]

    items = []

    for sub in subfolders:
        items.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.FOLDER_ROUNDED, color=T.FOLDER_COLOR, size=22),
                        width=42, height=42, bgcolor=T.FOLDER_BG, border_radius=12, alignment=ft.Alignment.CENTER
                    ),
                    ft.Text(sub["name"], size=T.FS_BODY, color=T.TEXT_PRIMARY, weight=ft.FontWeight.W_600, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                        icon_color=T.TEXT_HINT,
                        icon_size=20,
                        tooltip="Удалить подпапку",
                        on_click=lambda e, s=sub: on_delete_folder(s),
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=T.TEXT_HINT, size=20),
                ], spacing=T.GAP_SM),
                bgcolor=T.SURFACE,
                border_radius=T.R_CARD,
                padding=T.PAD_CARD,
                margin=ft.Margin.only(bottom=T.GAP),
                on_click=lambda e, s=sub: on_open_folder(s),
                ink=True,
                shadow=ft.BoxShadow(blur_radius=10, color=T.SHADOW_SOFT, offset=ft.Offset(0, 2)),
            )
        )

    for f in files:
        items.append(
            file_card(
                f,
                on_click=lambda e, f=f: on_view_file(f),
                on_delete=on_delete_file,
                on_tag_click=on_edit_tags
            )
        )

    if items:
        content = ft.Column(items, scroll=ft.ScrollMode.AUTO, spacing=0)
    else:
        content = empty_state(ft.Icons.FOLDER_OPEN_ROUNDED, "В этой папке пока пусто.\nНажмите «+», чтобы добавить материал.")

    def open_add_menu(e):
        show_action_sheet(
            page,
            on_create_folder=lambda: on_create_folder(folder_id),
            on_create_note=lambda: show_create_note_dialog(
                page, lambda title, text, tags: on_create_note(folder, title, text, tags)
            ),
            on_upload_file=lambda: page.run_task(file_picker),
        )

    view = ft.View(
        route="/files",
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
            appbar(
                folder["name"],
                back=lambda e: on_back(),
                actions=[
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE_ROUNDED,
                        icon_color=T.DANGER,
                        tooltip="Удалить папку",
                        on_click=lambda e: on_delete_folder(current_node)
                    ),
                ],
            ),
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
