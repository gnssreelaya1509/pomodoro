import flet as ft
import asyncio
from timer_engine import TimerEngine


def main(page: ft.Page):
    page.title = "Pomodoro Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    # Initialize with default 25 minutes
    engine = TimerEngine(duration_minutes=25)

    timer_text = ft.Text("25:00", size=40, weight="bold", color=ft.Colors.BLUE_GREY_800)
    progress_ring = ft.ProgressRing(width=200, height=200, stroke_width=10, value=1.0, color=ft.Colors.RED_400)

    async def update_timer():
        while True:
            if engine.tick():
                mins, secs = divmod(engine.remaining, 60)
                timer_text.value = f"{mins:02d}:{secs:02d}"
                progress_ring.value = engine.remaining / engine.duration
                page.update()
            await asyncio.sleep(1)

    def change_duration(e):
        new_duration = int(time_dropdown.value)
        engine.duration = new_duration * 60
        engine.reset()
        timer_text.value = f"{new_duration:02d}:00"
        progress_ring.value = 1.0
        start_btn.text = "Start"
        start_btn.icon = "play_arrow"
        page.update()

    # Dropdown configuration
    time_dropdown = ft.Dropdown(
        label="Select Duration (min)",
        width=200,
        options=[
            ft.dropdown.Option("5"),
            ft.dropdown.Option("25"),
            ft.dropdown.Option("45"),
        ],
        value="25",
    )
    time_dropdown.on_change = change_duration

    def handle_toggle(e):
        is_running = engine.toggle()
        start_btn.icon = "pause" if is_running else "play_arrow"
        start_btn.text = "Pause" if is_running else "Start"
        page.update()

    def handle_reset(e):
        engine.reset()
        mins = int(time_dropdown.value)
        timer_text.value = f"{mins:02d}:00"
        progress_ring.value = 1.0
        start_btn.text = "Start"
        start_btn.icon = "play_arrow"
        page.update()

    start_btn = ft.ElevatedButton("Start", icon="play_arrow", on_click=handle_toggle, bgcolor=ft.Colors.BLUE_200)
    reset_btn = ft.ElevatedButton("Reset", icon="restart_alt", on_click=handle_reset)

    # Perfectly centered layout using Container alignment
    # Perfectly centered layout
    page.add(
        ft.Column([
            ft.Text("Focus Session", size=24, weight="w500"),
            time_dropdown,
            ft.Container(
                content=ft.Stack([
                    progress_ring,
                    ft.Container(
                        content=timer_text,
                        # Use absolute centering within the container
                        top=0, left=0, right=0, bottom=0,
                        alignment=ft.Alignment.CENTER
                    )
                ]),
                height=220,
                width=220,  # Increased width slightly
            ),
            ft.Row([start_btn, reset_btn], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    asyncio.create_task(update_timer())


ft.app(target=main)