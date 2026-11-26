"""Нижние мобильные шторки (Bottom Sheets) на базе Stack + Container."""
import flet as ft
from app import theme as T


def _wrap_bottom_sheet(page: ft.Page, title: str, body_controls: list):
    """Создает надежную нижнюю панель с затемнением, работающим крестиком и автозакрытием."""
    overlay_layer = None

    def close_sheet(e=None):
        if overlay_layer and overlay_layer in page.overlay:
            page.overlay.remove(overlay_layer)
            page.update()

    drag_handle = ft.Container(
        width=40,
        height=4,
        bgcolor=T.DIVIDER,
        border_radius=2,
        margin=ft.Margin.only(bottom=8),
    )

    header = ft.Row([
        ft.Text(title, size=T.FS_TITLE, weight=ft.FontWeight.W_700, color=T.TEXT_PRIMARY),
        ft.IconButton(
            icon=ft.Icons.CLOSE_ROUNDED,
            icon_color=T.TEXT_SECONDARY,
            on_click=close_sheet,
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    card = ft.Container(
        bgcolor=T.SURFACE,
        border_radius=ft.BorderRadius.only(top_left=T.R_SHEET, top_right=T.R_SHEET),
        padding=ft.Padding.only(left=20, right=20, top=12, bottom=28),
        on_click=lambda e: None,  # перехватываем клик, чтобы не закрывалось при нажатии на саму панель
        content=ft.Column(
            [ft.Row([drag_handle], alignment=ft.MainAxisAlignment.CENTER), header] + body_controls,
            spacing=14,
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    backdrop = ft.Container(
        bgcolor="#66000000",
        expand=True,
        on_click=close_sheet,  # закрытие при нажатии мимо шторки
    )

    overlay_layer = ft.Container(
        expand=True,
        content=ft.Stack([
            backdrop,
            ft.Column(
                [ft.Container(expand=True), card],
                spacing=0,
            ),
        ]),
    )

    page.overlay.append(overlay_layer)
    page.update()
    return close_sheet


def show_action_sheet(page: ft.Page, on_create_folder, on_create_note=None, on_upload_file=None):
    """Меню быстрого создания по нажатию на '+'."""
    close_fn = None

    def action_tile(icon: str, color: str, bg: str, title: str, subtitle: str, callback=None):
        def handle_click(e):
            if close_fn:
                close_fn()
            if callback:
                callback()

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=24),
                    width=46, height=46, bgcolor=bg, border_radius=14, alignment=ft.Alignment.CENTER
                ),
                ft.Column([
                    ft.Text(title, size=T.FS_BODY, weight=ft.FontWeight.W_600, color=T.TEXT_PRIMARY),
                    ft.Text(subtitle, size=T.FS_SMALL, color=T.TEXT_SECONDARY),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=T.TEXT_HINT),
            ], spacing=12),
            padding=12,
            bgcolor=T.SURFACE_ALT,
            border_radius=T.R_CARD,
            ink=True,
            on_click=handle_click,
        )

    tiles = [
        action_tile(
            ft.Icons.CREATE_NEW_FOLDER_ROUNDED, T.FOLDER_COLOR, T.FOLDER_BG,
            "Новая папка", "Создать раздел для предмета", callback=on_create_folder
        )
    ]
    if on_create_note:
        tiles.append(
            action_tile(
                ft.Icons.EDIT_NOTE_ROUNDED, T.NOTE_COLOR, T.NOTE_BG,
                "Новая заметка", "Конспект или карточка для повторения", callback=on_create_note
            )
        )
    if on_upload_file:
        tiles.append(
            action_tile(
                ft.Icons.UPLOAD_FILE_ROUNDED, T.IMAGE_COLOR, T.IMAGE_BG,
                "Загрузить файл", "PDF, документ или изображение", callback=on_upload_file
            )
        )

    close_fn = _wrap_bottom_sheet(page, "Добавить", tiles)


def show_create_note_dialog(page: ft.Page, on_save):
    title_field = ft.TextField(label="Название (Тема)", border_radius=T.R_FIELD, autofocus=True)
    content_field = ft.TextField(label="Содержимое (Ответ)", multiline=True, min_lines=3, max_lines=5, border_radius=T.R_FIELD)
    tags_field = ft.TextField(label="Теги (через запятую)", hint_text="математика, формулы", border_radius=T.R_FIELD)
    close_fn = None

    def save(e):
        title = title_field.value.strip()
        content = content_field.value.strip()
        tags_raw = tags_field.value.strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        if not title or not content:
            return
        if close_fn:
            close_fn()
        on_save(title, content, tags)

    submit_btn = ft.FilledButton(
        "Создать заметку",
        height=48,
        style=ft.ButtonStyle(bgcolor=T.PRIMARY, color=T.TEXT_ON_PRIMARY, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
        on_click=save,
    )
    close_fn = _wrap_bottom_sheet(page, "Новая заметка", [title_field, content_field, tags_field, submit_btn])


def show_add_tags_dialog(page: ft.Page, file: dict, on_save):
    tags_field = ft.TextField(
        label="Теги (через запятую)",
        value=",".join(file.get("tags", [])),
        hint_text="например: математика, важное",
        border_radius=T.R_FIELD,
        autofocus=True,
    )
    close_fn = None

    def save(e):
        tags_raw = tags_field.value.strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        if close_fn:
            close_fn()
        on_save(file, tags)

    submit_btn = ft.FilledButton(
        "Сохранить теги",
        height=48,
        style=ft.ButtonStyle(bgcolor=T.PRIMARY, color=T.TEXT_ON_PRIMARY, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
        on_click=save,
    )
    close_fn = _wrap_bottom_sheet(page, "Теги файла", [tags_field, submit_btn])


def show_create_folder_dialog(page: ft.Page, folders_tree: list, on_save, default_parent_id: int = None):
    name_field = ft.TextField(
        label="Название папки",
        hint_text="Например: Физика",
        border_radius=T.R_FIELD,
        autofocus=True,
    )

    options = [ft.dropdown.Option(key="root", text="Корневой уровень (без родителя)")]

    def collect_options(nodes, prefix=""):
        for n in nodes:
            options.append(ft.dropdown.Option(key=str(n["id"]), text=f"{prefix}{n['name']}"))
            collect_options(n.get("children", []), prefix + "— ")

    collect_options(folders_tree)

    parent_dropdown = ft.Dropdown(
        label="Родительская папка",
        value=str(default_parent_id) if default_parent_id is not None else "root",
        options=options,
        border_radius=T.R_FIELD,
    )
    close_fn = None

    def save(e):
        name = name_field.value.strip()
        if not name:
            return
        parent_id = None if parent_dropdown.value == "root" else int(parent_dropdown.value)
        if close_fn:
            close_fn()
        on_save(name, parent_id)

    submit_btn = ft.FilledButton(
        "Создать папку",
        height=48,
        style=ft.ButtonStyle(bgcolor=T.PRIMARY, color=T.TEXT_ON_PRIMARY, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
        on_click=save,
    )
    close_fn = _wrap_bottom_sheet(page, "Новая папка", [name_field, parent_dropdown, submit_btn])
