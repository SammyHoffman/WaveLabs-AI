"""
core/color_utils.py

Defines ANSI color codes and common message prefixes for console logs.
"""

from config.settings import USE_COLOR_LOGS

# If USE_COLOR_LOGS is False, set all color codes to empty strings
COLOR_RESET  = "\033[0m"   if USE_COLOR_LOGS else ""
COLOR_RED    = "\033[31m"  if USE_COLOR_LOGS else ""
COLOR_GREEN  = "\033[32m"  if USE_COLOR_LOGS else ""
COLOR_YELLOW = "\033[33m"  if USE_COLOR_LOGS else ""
COLOR_BLUE   = "\033[34m"  if USE_COLOR_LOGS else ""
COLOR_CYAN   = "\033[36m"  if USE_COLOR_LOGS else ""
COLOR_GREY   = "\033[37m"  if USE_COLOR_LOGS else ""

MSG_ERROR   = f"{COLOR_RED}[Error]{COLOR_RESET}: "
MSG_NOTICE  = f"{COLOR_YELLOW}[Notice]{COLOR_RESET}: "
MSG_DEBUG   = f"{COLOR_CYAN}[Debug]{COLOR_RESET}: "
MSG_SUCCESS = f"{COLOR_GREEN}[Success]{COLOR_RESET}: "
MSG_STATUS  = f"{COLOR_GREEN}[Status]{COLOR_RESET}: "
MSG_WARNING = f"{COLOR_BLUE}[Warning]{COLOR_RESET}: "
LINE_BREAK  = f"{COLOR_GREY}----------------------------------------{COLOR_RESET}"