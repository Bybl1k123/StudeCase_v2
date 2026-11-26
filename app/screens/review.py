"""Экран 5: Повторение."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.widgets.cards import empty_state
from app.demo_data import DEMO_FILES

def show_review(page: ft.Page, folder: dict, on_back):
    notes = [f for f in DEMO_FILES if f.get("folder_id") == folder.get("id") and f.get("type") == "note"]
    idx = {"i": 0}
    total = len(notes)

    if total == 0:
        view = ft.View(
            route="/review",
            padding=0,
            bgcolor=T.BACKGROUND,
            controls=[
                appbar("Повторение", back=lambda e: on_back()),
                ft.Container(
                    content=empty_state(ft.Icons.STYLE_OUTLINED, "В этой папке нет заметок для повторения."),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                )
            ]
        )
        page.views.clear()
        page.views.append(view)
        page.update()
        return

    progress = ft.ProgressBar(value=0, color=T.PRIMARY, bgcolor=T.DIVIDER, bar_height=4)
    counter = ft.Container(
        content=ft.Text(f"1 / {total}", size=T.FS_SMALL, color=T.PRIMARY, weight=ft.FontWeight.W_600),
        bgcolor=T.PRIMARY_LIGHT,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=12,
        margin=ft.Margin.only(right=16),
    )
    card_title = ft.Text("", size=T.FS_TITLE, weight=ft.FontWeight.W_700, color=T.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)
    
    answer_text = ft.Text("", size=T.FS_BODY, color=T.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)
    answer_box = ft.Container(
        content=ft.Column([
            ft.Divider(height=1, color=T.DIVIDER),
            answer_text,
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        visible=False,
        padding=ft.Padding.only(top=8),
    )
    
    show_answer_btn = ft.FilledButton(
        "Показать ответ",
        height=48,
        width=220,
        style=ft.ButtonStyle(bgcolor=T.PRIMARY, color=T.TEXT_ON_PRIMARY, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
        on_click=lambda e: show_answer(),
    )
    
    quality_row = ft.Row([
        ft.Container(
            content=ft.Text(str(i), size=T.FS_HEADING, weight=ft.FontWeight.W_600, color=T.TEXT_PRIMARY),
            height=48,
            expand=True,
            bgcolor=T.SURFACE,
            border_radius=T.R_BUTTON,
            alignment=ft.Alignment.CENTER,
            shadow=ft.BoxShadow(blur_radius=6, color=T.SHADOW_SOFT, offset=ft.Offset(0, 2)),
            ink=True,
            on_click=lambda e, q=i: answer(q),
        ) for i in range(6)
    ], spacing=6)
    
    quality_labels = ft.Row([
        ft.Text("Совсем забыл", size=T.FS_TINY, color=T.TEXT_HINT),
        ft.Text("Очень легко", size=T.FS_TINY, color=T.TEXT_HINT),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    rating_block = ft.Column([
        ft.Text("Насколько легко вспомнил?", size=T.FS_SMALL, color=T.TEXT_SECONDARY, weight=ft.FontWeight.W_500),
        quality_row,
        quality_labels,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)

    def render_current():
        if idx["i"] >= total:
            card_title.value = "🎉 Всё повторено!"
            answer_text.value = "Отличная работа! Все карточки в этой папке пройдены."
            answer_box.visible = True
            show_answer_btn.visible = False
            rating_block.visible = False
            progress.value = 1
            counter.content.value = f"{total} / {total}"
            page.update()
            return
        
        item = notes[idx["i"]]
        card_title.value = item["name"]
        answer_text.value = item.get("content", "Нет содержимого")
        answer_box.visible = False
        show_answer_btn.visible = True
        rating_block.visible = True
        counter.content.value = f'{idx["i"] + 1} / {total}'
        progress.value = idx["i"] / total
        page.update()

    def show_answer():
        answer_box.visible = True
        show_answer_btn.visible = False
        page.update()

    def answer(quality: int):
        idx["i"] += 1
        render_current()

    view = ft.View(
        route="/review",
        padding=0,
        bgcolor=T.BACKGROUND,
        controls=[
            appbar(folder["name"], back=lambda e: on_back(), actions=[counter]),
            progress,
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([card_title, answer_box, show_answer_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                        bgcolor=T.SURFACE,
                        border_radius=T.R_CARD,
                        padding=24,
                        width=float("inf"),
                        shadow=ft.BoxShadow(blur_radius=14, color=T.SHADOW_CARD, offset=ft.Offset(0, 4)),
                    ),
                    rating_block,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                padding=ft.Padding.only(left=T.PAD_SCREEN, right=T.PAD_SCREEN, top=24, bottom=28),
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()
    render_current()
