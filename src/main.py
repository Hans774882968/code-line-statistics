import os
from typing import Any
from consts import *
from file_statistics import analyze_directory, SUPPORTED_EXTENSIONS
from theme import add_font_for_dpg, set_global_theme, set_operations_window_theme
from display_table import display_by_file_type
import dearpygui.dearpygui as dpg


def directory_selected(sender, app_data):
    '''当文件夹被选择时的回调函数'''
    selected_dir = app_data['file_path_name']
    if not os.path.isdir(selected_dir):
        return
    dir_selection_text = f'当前选择的文件夹：{selected_dir}'
    dpg.set_value(DIR_SELECTION_TAG, dir_selection_text)
    statistics = analyze_directory(selected_dir)
    update_display(statistics)


def update_display(statistics: dict[str, Any]):
    '''更新UI显示统计结果'''
    # 清除旧内容
    for child in dpg.get_item_children(RESULTS_WINDOW_TAG)[1]:
        dpg.delete_item(child)

    # 显示汇总信息
    dpg.add_text(f"总文件数: {statistics['total_files']}", parent=RESULTS_WINDOW_TAG)
    dpg.add_text(f"总行数: {statistics['total_lines']}", parent=RESULTS_WINDOW_TAG)

    display_by_file_type(statistics)

    # 显示每种扩展名的行数前5文件
    for ext, files in statistics['top_files_by_extension'].items():
        if not files:
            continue
        dpg.add_text(f"{ext} 行数前5的文件:", parent=RESULTS_WINDOW_TAG)
        for i, file in enumerate(files, 1):
            dpg.add_text(
                f"{i}. {file['path']} - {file['lines']} 行",
                parent=RESULTS_WINDOW_TAG,
                indent=20
            )
        dpg.add_separator(parent=RESULTS_WINDOW_TAG)

    update_bar_charts(statistics)


def set_bar_chart_y_axis_limits(y_axis_tag: str, values: list):
    if values:
        dpg.set_axis_limits(y_axis_tag, 0, max(values) * 1.2)


def update_bar_charts(statistics: dict[str, Any]):
    def update_bar_chart_part1():
        dpg.add_spacer(height=10, parent=RESULTS_WINDOW_TAG)

        FILE_COUNT_CHART_TAG = 'file_count_chart'
        with dpg.plot(label='文件类型 - 文件数', parent=RESULTS_WINDOW_TAG,
                      height=300, width=-1, tag=FILE_COUNT_CHART_TAG):
            x_axis_tag = 'file_count_x_axis'
            y_axis_tag = 'file_count_y_axis'

            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label='文件类型', tag=x_axis_tag)
            x_axis_ticks = tuple(zip(
                extensions,
                range(len(extensions)),
            ))
            dpg.set_axis_ticks(x_axis_tag, x_axis_ticks)
            dpg.set_axis_limits(x_axis_tag, -0.5, len(extensions) - 0.5)

            with dpg.plot_axis(dpg.mvYAxis, label='数量', tag=y_axis_tag):
                dpg.add_bar_series(
                    list(range(len(extensions))),
                    file_counts,
                    label='文件数',
                    weight=0.6
                )
                # 添加柱子上的数值标注
                for i, count in enumerate(file_counts):
                    dpg.add_plot_annotation(
                        label=str(count),
                        default_value=(i, count),
                        offset=ANNO_OFFSET,
                        color=ANNO_COLOR,
                        parent=FILE_COUNT_CHART_TAG
                    )

            set_bar_chart_y_axis_limits(y_axis_tag, file_counts)

        dpg.add_spacer(height=10, parent=RESULTS_WINDOW_TAG)

        FILE_LINES_CHART_TAG = 'file_lines_chart'
        with dpg.plot(label='文件类型 - 行数', parent=RESULTS_WINDOW_TAG,
                      height=300, width=-1, tag=FILE_LINES_CHART_TAG):
            x_axis_tag = 'file_lines_x_axis'
            y_axis_tag = 'file_lines_y_axis'
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label='文件类型', tag=x_axis_tag)
            x_axis_ticks = tuple(zip(
                extensions,
                range(len(extensions)),
            ))
            dpg.set_axis_ticks(x_axis_tag, x_axis_ticks)
            dpg.set_axis_limits(x_axis_tag, -0.5, len(extensions) - 0.5)

            with dpg.plot_axis(dpg.mvYAxis, label='数量', tag=y_axis_tag):
                dpg.add_bar_series(
                    list(range(len(extensions))),
                    line_counts,
                    label='行数',
                    weight=0.6
                )
                # 添加柱子上的数值标注
                for i, count in enumerate(line_counts):
                    dpg.add_plot_annotation(
                        label=str(count),
                        default_value=(i, count),
                        offset=ANNO_OFFSET,
                        color=ANNO_COLOR,
                        parent=FILE_LINES_CHART_TAG
                    )

            set_bar_chart_y_axis_limits(y_axis_tag, line_counts)

    def update_bar_chart_part2():
        '''为每个扩展名创建单独的柱状图'''
        for ext in extensions:
            files = statistics['top_files_by_extension'].get(ext, [])
            if not files:
                continue

            # 提取文件名和行数
            filenames = [os.path.basename(f['path']) for f in files]
            lines = [f['lines'] for f in files]

            TOP_FILES_BAR_CHART_TAG = f'top_files_chart_{ext}'

            with dpg.plot(label=f'{ext} 行数前5文件', parent=RESULTS_WINDOW_TAG,
                          height=300, width=-1, tag=TOP_FILES_BAR_CHART_TAG):
                x_axis_tag = f'x_axis_{ext}'
                y_axis_tag = f'y_axis_{ext}'
                dpg.add_plot_axis(dpg.mvXAxis, label='文件名', tag=x_axis_tag)
                with dpg.plot_axis(dpg.mvYAxis, label='行数', tag=y_axis_tag):
                    dpg.add_bar_series(
                        list(range(len(files))),
                        lines,
                        label='行数',
                        weight=0.6
                    )
                    # 添加柱子上的数值标注
                    for i, line_count in enumerate(lines):
                        dpg.add_plot_annotation(
                            label=str(line_count),
                            default_value=(i, line_count),
                            offset=ANNO_OFFSET,
                            color=ANNO_COLOR,
                            parent=TOP_FILES_BAR_CHART_TAG
                        )

                set_bar_chart_y_axis_limits(y_axis_tag, lines)

                # 设置X轴标签
                x_axis_ticks = tuple(zip(
                    filenames,
                    range(len(filenames)),
                ))
                dpg.set_axis_ticks(x_axis_tag, x_axis_ticks)
                dpg.set_axis_limits(x_axis_tag, -0.5, len(filenames) - 0.5)
            dpg.add_spacer(height=10, parent=RESULTS_WINDOW_TAG)

    # 删除旧的图表
    for tag in ['file_type_chart'] + [f'top_files_chart_{ext}' for ext in statistics['by_extension']]:
        if dpg.does_item_exist(tag):
            dpg.delete_item(tag)

    # 第一个图表：文件类型统计
    extensions = list(statistics['by_extension'].keys())
    file_counts = [data['count'] for data in statistics['by_extension'].values()]
    line_counts = [data['lines'] for data in statistics['by_extension'].values()]

    update_bar_chart_part1()
    dpg.add_spacer(height=20, parent=RESULTS_WINDOW_TAG)
    update_bar_chart_part2()


def operations_window_layout():
    width, height, _, data = dpg.load_image(INFO_CIRCLE_ICON_PATH)
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag=INFO_CIRCLE_ICON_TAG)

    set_operations_window_theme()

    with dpg.group(horizontal=True, parent=OPERATIONS_WINDOW_TAG, tag=FILE_TYPE_DIV_TAG):
        dpg.add_image(INFO_CIRCLE_ICON_TAG, parent=FILE_TYPE_DIV_TAG, width=18, height=18)
        dpg.add_text(f'目前支持分析的文件类型：{SUPPORTED_EXTENSIONS}', parent=FILE_TYPE_DIV_TAG)

    dpg.bind_item_theme(OPERATIONS_WINDOW_TAG, OPERATIONS_WINDOW_THEME)
    dpg.bind_item_theme(FILE_TYPE_DIV_TAG, ICON_TEXT_THEME)

    dpg.add_text('选择要分析的文件夹:', tag=DIR_SELECTION_TAG, parent=OPERATIONS_WINDOW_TAG)
    dpg.add_button(
        label='选择文件夹',
        callback=lambda: dpg.show_item('file_dialog'),
        parent=OPERATIONS_WINDOW_TAG
    )


def main():
    dpg.create_context()
    add_font_for_dpg()
    set_global_theme()
    dpg.create_viewport(title='File Line Statistics', width=800, height=600, small_icon=SMALL_ICON_PATH, large_icon=LARGE_ICON_PATH)

    with dpg.window(label='主窗口', tag=MAIN_WINDOW_TAG):
        dpg.add_child_window(
            tag=OPERATIONS_WINDOW_TAG,
            autosize_x=True,
            height=128
        )
        operations_window_layout()

        # 结果显示区域
        dpg.add_child_window(
            tag=RESULTS_WINDOW_TAG,
            autosize_x=True,
            height=-1
        )

    with dpg.file_dialog(
        directory_selector=True,
        show=False,
        callback=directory_selected,
        tag='file_dialog',
        width=500,
        height=400
    ):
        pass

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(MAIN_WINDOW_TAG, True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()
