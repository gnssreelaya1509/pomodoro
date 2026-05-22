import flet as ft
import asyncio
from timer_engine import TimerEngine # Correct path import


def main(page: ft.Page):
    page.title = "Pomodoro Timer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    engine = TimerEngine(duration_minutes=25)

    timer_text = ft.Text("25:00", size=60, weight="bold")
    progress_bar = ft.ProgressBar(value=1.0, width=400, color=ft.Colors.RED_400)

    async def update_timer():
        while True:
            if engine.tick():
                mins, secs = divmod(engine.remaining, 60)
                timer_text.value = f"{mins:02d}:{secs:02d}"
                progress_bar.value = engine.remaining / engine.duration
                page.update()
            await asyncio.sleep(1)

    def handle_toggle(e):
        is_running = engine.toggle()
        e.control.text = "Pause" if is_running else "Start"
        page.update()

    def handle_reset(e):
        engine.reset()
        timer_text.value = "25:00"
        progress_bar.value = 1.0
        start_btn.text = "Start"
        page.update()

    start_btn = ft.ElevatedButton("Start", on_click=handle_toggle)
    reset_btn = ft.ElevatedButton("Reset", on_click=handle_reset)

    page.add(
        ft.Column([
            ft.Text("Pomodoro Timer", size=30),
            timer_text,
            progress_bar,
            ft.Row([start_btn, reset_btn], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    asyncio.create_task(update_timer())


ft.app(target=main)