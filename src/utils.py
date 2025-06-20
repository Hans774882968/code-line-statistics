import os
import sys


def resource_path(relative_path):
    ''' Get absolute path to resource, works for dev and for PyInstaller '''
    base_path = getattr(sys, '_MEIPASS', os.getcwd())
    return os.path.join(base_path, relative_path)


def get_up_or_down_arrow(direction: int) -> str:
    return '^' if direction == 1 else 'v'


def get_up_or_down_arrow_extend(direction: int) -> str:
    return '' if direction == 0 else f' {get_up_or_down_arrow(direction)}'
