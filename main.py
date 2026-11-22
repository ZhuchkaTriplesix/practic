"""
Кейс-задача № 2: Стилистическое преобразование чисел и анализ даты рождения.
"""

from datetime import date
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt
from rich.align import Align

console = Console()

# Матрицы 5x7 для цифр 0-9 и пробела для электронного табло со звездочками (*)
DIGITS_5X7: dict[str, list[str]] = {
    "0": [
        " *** ",
        "*   *",
        "*   *",
        "*   *",
        "*   *",
        "*   *",
        " *** ",
    ],
    "1": [
        "  *  ",
        " **  ",
        "  *  ",
        "  *  ",
        "  *  ",
        "  *  ",
        " *** ",
    ],
    "2": [
        " *** ",
        "*   *",
        "    *",
        "   * ",
        "  *  ",
        " *   ",
        "*****",
    ],
    "3": [
        " *** ",
        "*   *",
        "    *",
        " *** ",
        "    *",
        "*   *",
        " *** ",
    ],
    "4": [
        "*   *",
        "*   *",
        "*   *",
        "*****",
        "    *",
        "    *",
        "    *",
    ],
    "5": [
        "*****",
        "*    ",
        "**** ",
        "    *",
        "    *",
        "*   *",
        " *** ",
    ],
    "6": [
        " *** ",
        "*    ",
        "**** ",
        "*   *",
        "*   *",
        "*   *",
        " *** ",
    ],
    "7": [
        "*****",
        "    *",
        "   * ",
        "  *  ",
        "  *  ",
        "  *  ",
        "  *  ",
    ],
    "8": [
        " *** ",
        "*   *",
        "*   *",
        " *** ",
        "*   *",
        "*   *",
        " *** ",
    ],
    "9": [
        " *** ",
        "*   *",
        "*   *",
        " ****",
        "    *",
        "    *",
        " *** ",
    ],
    " ": [
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
    ],
}


def get_weekday_name(birth_date: date) -> str:
    """Определяет, какому дню недели соответствует заданная дата.

    :param birth_date: Дата рождения
    :return: Название дня недели на русском языке
    """
    weekdays = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье",
    ]
    # weekday() возвращает 0 для понедельника и 6 для воскресенья
    return weekdays[birth_date.weekday()]


def is_leap_year(year: int) -> bool:
    """Определяет, является ли год високосным.

    Год високосный, если он кратен 4, но не кратен 100, либо кратен 400.
    :param year: Год
    :return: True, если год високосный, иначе False
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def calculate_age(birth_date: date, today: date | None = None) -> int:
    """Вычисляет количество полных лет пользователя на текущую дату.

    :param birth_date: Дата рождения
    :param today: Текущая дата (по умолчанию date.today())
    :return: Полных лет
    """
    if today is None:
        today = date.today()

    # Проверяем, наступил ли уже день рождения в текущем году
    has_birthday_occurred = (today.month, today.day) >= (
        birth_date.month,
        birth_date.day,
    )
    age = today.year - birth_date.year - (0 if has_birthday_occurred else 1)
    return age


def format_russian_years(years: int) -> str:
    """Возвращает строку с правильным склонением слова 'год/года/лет'."""
    if 11 <= (years % 100) <= 14:
        return f"{years} лет"
    last_digit = years % 10
    if last_digit == 1:
        return f"{years} год"
    if 2 <= last_digit <= 4:
        return f"{years} года"
    return f"{years} лет"


def render_scoreboard_date(day: int, month: int, year: int) -> str:
    """Преобразует дату в строковый формат дд мм гггг,

    где цифры прорисованы звёздочками (*), как на электронном табло.
    """
    # Формируем строку 'дд  мм  гггг' с разделением групп пробелами
    date_str = f"{day:02d}  {month:02d}  {year:04d}"

    height = 7
    lines = ["" for _ in range(height)]

    for char in date_str:
        pattern = DIGITS_5X7.get(char, DIGITS_5X7[" "])
        for row in range(height):
            lines[row] += pattern[row] + "  "

    return "\n".join(lines)


def request_birth_date() -> tuple[int, int, int, date]:
    """Последовательно запрашивает у пользователя день, месяц и год рождения

    с валидацией корректности введённой даты.
    """
    console.print(
        Panel.fit(
            "[bold cyan]Введите данные вашего рождения[/bold cyan]\n"
            "[dim]Программа последовательно запросит день, месяц и год[/dim]",
            border_style="cyan",
        )
    )

    current_year = date.today().year

    while True:
        try:
            day = IntPrompt.ask("[bold yellow]➔ Введите день рождения (1-31)[/bold yellow]")
            month = IntPrompt.ask("[bold yellow]➔ Введите месяц рождения (1-12)[/bold yellow]")
            year = IntPrompt.ask(
                f"[bold yellow]➔ Введите год рождения (1900-{current_year})[/bold yellow]"
            )

            if year < 1900 or year > current_year:
                console.print(
                    f"[bold red]Ошибка:[/bold red] Год должен быть в диапазоне от 1900 до {current_year}!\n"
                )
                continue

            birth_date = date(year, month, day)

            if birth_date > date.today():
                console.print(
                    "[bold red]Ошибка:[/bold red] Дата рождения не может быть в будущем!\n"
                )
                continue

            return day, month, year, birth_date

        except ValueError as err:
            console.print(
                f"[bold red]Ошибка:[/bold red] Некорректная дата (например, 31 февраля или недопустимый месяц). Попробуйте снова.\n"
            )


def main() -> None:
    if console.is_terminal:
        console.clear()
    console.print(
        Panel(
            Align.center(
                "[bold magenta]АНАЛИЗАТОР ДАТЫ РОЖДЕНИЯ & ЦИФРОВОЕ ТАБЛО[/bold magenta]\n"
                "[dim]Кейс-задача № 2: Стилистическое преобразование чисел[/dim]"
            ),
            border_style="magenta",
            padding=(1, 2),
        )
    )

    # 1. Последовательный запрос даты
    day, month, year, birth_date = request_birth_date()

    # 2. Определение дня недели
    weekday = get_weekday_name(birth_date)

    # 3. Определение високосности года
    leap = is_leap_year(year)
    leap_str = (
        "[bold green]Да (високосный)[/bold green]"
        if leap
        else "[dim]Нет (обычный)[/dim]"
    )

    # 4. Определение возраста
    age = calculate_age(birth_date)
    age_str = format_russian_years(age)

    # Формирование итоговой таблицы результатов
    table = Table(
        title="[bold yellow]Результаты анализа даты[/bold yellow]",
        show_header=True,
        header_style="bold cyan",
        border_style="bright_blue",
    )
    table.add_column("Параметр", style="bold white", width=25)
    table.add_column("Значение", style="bold green", width=35)

    table.add_row("Дата рождения", f"{day:02d}.{month:02d}.{year:04d}")
    table.add_row("День недели", f"{weekday}")
    table.add_row("Високосный год", f"{leap_str}")
    table.add_row("Текущий возраст", f"{age_str}")

    console.print("\n")
    console.print(table)

    # 5. Вывод электронного табло со звездочками в формате дд мм гггг
    scoreboard_art = render_scoreboard_date(day, month, year)

    board_panel = Panel(
        Align.center(f"[bold bright_green]{scoreboard_art}[/bold bright_green]"),
        title="[bold bright_yellow]⚡ ЭЛЕКТРОННОЕ ТАБЛО (ДД ММ ГГГГ) ⚡[/bold bright_yellow]",
        subtitle="[dim green]Стилизованный вывод цифр символами (*)[/dim green]",
        border_style="bright_green",
        padding=(1, 2),
    )

    console.print("\n")
    console.print(board_panel)
    console.print("\n[dim green]✔ Программа успешно завершила работу.[/dim green]\n")


if __name__ == "__main__":
    main()
