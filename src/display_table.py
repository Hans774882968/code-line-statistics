from typing import Any, Tuple
from copy import deepcopy
import dearpygui.dearpygui as dpg
from consts import *
from utils import get_up_or_down_arrow_extend

# 0: 不按该列排序 1: 按该列升序排序 -1: 按该列降序排序
sort_state = {'count': 0, 'lines': 0}


def sort_callback1(sender, app_data, user_data: list[Tuple[str, dict[str, Any]]]):
    global sort_state
    sort_state['count'] = -1 if sort_state['count'] == 0 else -sort_state['count']  # Toggle
    sort_state['lines'] = 0  # Reset other sort

    if sort_state['count'] != 0:
        user_data.sort(
            key=lambda x: x[1]['count'],
            reverse=sort_state['count'] == -1
        )

    dpg.delete_item(EXTENSION_TABLE_TAG)
    render_table(user_data)


def sort_callback2(sender, app_data, user_data: list[Tuple[str, dict[str, Any]]]):
    global sort_state
    sort_state['lines'] = -1 if sort_state['lines'] == 0 else -sort_state['lines']  # Toggle
    sort_state['count'] = 0  # Reset other sort

    if sort_state['lines'] != 0:
        user_data.sort(
            key=lambda x: x[1]['lines'],
            reverse=sort_state['lines'] == -1
        )

    dpg.delete_item(EXTENSION_TABLE_TAG)
    render_table(user_data)


def sort_callback3(sender, app_data, user_data: list[Tuple[str, dict[str, Any]]]):
    global sort_state
    sort_state['lines'] = 0
    sort_state['count'] = 0

    dpg.delete_item(EXTENSION_TABLE_TAG)
    render_table(user_data)


def render_table(by_extension_data: list[Tuple[str, dict[str, Any]]]):
    global sort_state
    with dpg.table(
        parent=BY_FILE_TYPE_TABLE_DIV,
        tag=EXTENSION_TABLE_TAG,
        header_row=True,
        resizable=True,
        policy=dpg.mvTable_SizingStretchProp,
        borders_outerH=True,
        borders_innerV=True,
        borders_innerH=True,
        borders_outerV=True
    ):
        dpg.add_table_column(label='后缀名')
        dpg.add_table_column(label=f'文件数{get_up_or_down_arrow_extend(sort_state["count"])}')
        dpg.add_table_column(label=f'行数{get_up_or_down_arrow_extend(sort_state["lines"])}')
        for ext, data in by_extension_data:
            with dpg.table_row():
                with dpg.table_cell():
                    dpg.add_text(ext)
                with dpg.table_cell():
                    dpg.add_text(data['count'])
                with dpg.table_cell():
                    dpg.add_text(data['lines'])


def display_by_file_type(statistics: dict[str, Any]):
    # 按扩展名显示统计
    dpg.add_child_window(
        tag=BY_FILE_TYPE_TABLE_DIV,
        parent=RESULTS_WINDOW_TAG,
        autosize_x=True,
        height=300
    )
    dpg.add_text('按文件类型统计:', parent=BY_FILE_TYPE_TABLE_DIV)
    if not statistics['by_extension']:
        dpg.add_text('啥都木有~', parent=BY_FILE_TYPE_TABLE_DIV)
        return

    by_extension_data = list(statistics['by_extension'].items())
    original_by_extension_data = deepcopy(by_extension_data)

    with dpg.group(parent=BY_FILE_TYPE_TABLE_DIV, horizontal=True):
        dpg.add_button(
            label='按文件数排序',
            tag=EXTENSION_TABLE_SORT_BTN1,
            callback=sort_callback1,
            user_data=by_extension_data
        )
        dpg.add_button(
            label='按行数排序',
            tag=EXTENSION_TABLE_SORT_BTN2,
            callback=sort_callback2,
            user_data=by_extension_data
        )
        dpg.add_button(
            label='重置',
            tag=EXTENSION_TABLE_SORT_BTN3,
            callback=sort_callback3,
            user_data=original_by_extension_data
        )
    render_table(by_extension_data)
