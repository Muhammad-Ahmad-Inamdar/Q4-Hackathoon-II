"""
Color utilities for CLI visual theme.

This module provides ANSI color codes and helper functions
to enhance the visual appearance of the CLI application.
"""

class Colors:
    """ANSI color codes for CLI output"""

    # Text colors
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Formatting
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'


def colored(text: str, color: str) -> str:
    """Add color to text and reset at the end"""
    return f"{color}{text}{Colors.RESET}"


def success(text: str) -> str:
    """Format success message in green"""
    return colored(text, Colors.GREEN)


def error(text: str) -> str:
    """Format error message in red"""
    return colored(text, Colors.RED)


def warning(text: str) -> str:
    """Format warning message in yellow"""
    return colored(text, Colors.YELLOW)


def info(text: str) -> str:
    """Format info message in blue"""
    return colored(text, Colors.BLUE)


def highlight(text: str) -> str:
    """Format highlighted text in yellow"""
    return colored(text, Colors.YELLOW)


def task_completed(text: str) -> str:
    """Format completed task indicator"""
    return colored("✓", Colors.GREEN) + f" {text}"


def task_pending(text: str) -> str:
    """Format pending task indicator"""
    return colored("O", Colors.YELLOW) + f" {text}"