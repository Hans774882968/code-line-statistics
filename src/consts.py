import os
from utils import resource_path

CHINESE_FONT_PATH = resource_path(os.path.join('fonts', 'ShanHaiJiGuJiangNanSongKeW-2.ttf'))
SMALL_ICON_PATH = resource_path(os.path.join('icons', 'dashboard-32.ico'))
LARGE_ICON_PATH = resource_path(os.path.join('icons', 'dashboard-256.ico'))
INFO_CIRCLE_ICON_PATH = resource_path(os.path.join('icons', 'info-circle-32.png'))
INFO_CIRCLE_ICON_TAG = 'info_circle_icon'
MAIN_WINDOW_TAG = 'main_window'
OPERATIONS_WINDOW_TAG = 'operations_window'
DIR_SELECTION_TAG = 'dir_selection'
RESULTS_WINDOW_TAG = 'results_window'
FILE_TYPE_DIV_TAG = 'file_type_div'
ICON_TEXT_THEME = 'icon_text_theme'
OPERATIONS_WINDOW_THEME = 'operations_window_theme'
BY_FILE_TYPE_TABLE_DIV = 'by_file_type_table_div'
EXTENSION_TABLE_TAG = 'extension_table'
EXTENSION_TABLE_SORT_BTN1 = 'file_type_table_sort_btn1'
EXTENSION_TABLE_SORT_BTN2 = 'file_type_table_sort_btn2'
EXTENSION_TABLE_SORT_BTN3 = 'file_type_table_sort_btn3'

# 和 dearpygui 提供的背景色相同
ANNO_COLOR = (37, 37, 38, 255)
# 紧挨着柱子上边
ANNO_OFFSET = (0, -5)
