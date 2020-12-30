
class PrintColors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    DEFAULT = "\033[39m"


def colorize(text, color=PrintColors.DEFAULT):
    return f"{color}{text}{PrintColors.DEFAULT}"
