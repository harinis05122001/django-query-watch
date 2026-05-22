# django_query_watch/logger.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .formatter import truncate_sql
from .constants import LOG_PREFIX

console = Console()


def log_slow_query(sql: str, duration_ms: float, request_path: str):
    content = Text()
    content.append("Execution Time: ", style="bold white")
    content.append(f"{duration_ms}ms\n", style="bold red")
    content.append("Request:        ", style="bold white")
    content.append(f"{request_path}\n\n", style="cyan")
    content.append("SQL:\n", style="bold white")
    content.append(truncate_sql(sql), style="yellow")

    console.print(
        Panel(
            content,
            title=f"{LOG_PREFIX} ⚠ Slow Query Detected",
            title_align="left",
            border_style="red",
            padding=(1, 2),
        )
    )


def log_duplicate_query(sql: str, count: int):
    content = Text()
    content.append("Repeated: ", style="bold white")
    content.append(f"{count} times\n\n", style="bold yellow")
    content.append("SQL:\n", style="bold white")
    content.append(truncate_sql(sql), style="yellow")

    console.print(
        Panel(
            content,
            title=f"{LOG_PREFIX} ⚠ Duplicate Query Detected",
            title_align="left",
            border_style="yellow",
            padding=(1, 2),
        )
    )


def log_summary(path: str, summary: dict):
    slow = summary["slow_queries"]
    dupes = summary["duplicate_queries"]
    total = summary["total_queries"]
    time_ms = summary["total_time_ms"]

    # Pick color based on health
    if slow > 0 or dupes > 0:
        border = "yellow"
        status = "⚠"
    else:
        border = "green"
        status = "✔"

    content = Text()
    content.append("Path:             ", style="bold white")
    content.append(f"{path}\n", style="cyan")
    content.append("Total Queries:    ", style="bold white")
    content.append(f"{total}\n", style="white")
    content.append("Total Time:       ", style="bold white")
    content.append(f"{time_ms}ms\n", style="white")
    content.append("Slow Queries:     ", style="bold white")
    content.append(f"{slow}\n", style="red" if slow > 0 else "green")
    content.append("Duplicate Queries:", style="bold white")
    content.append(f" {dupes}", style="yellow" if dupes > 0 else "green")

    console.print(
        Panel(
            content,
            title=f"{LOG_PREFIX} {status} Request Summary",
            title_align="left",
            border_style=border,
            padding=(1, 2),
        )
    )
