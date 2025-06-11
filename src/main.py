import os
from typing import Any
from file_statistics import analyze_directory
import dearpygui.dearpygui as dpg

chinese_font_path = os.path.join('fonts', 'ShanHaiJiGuJiangNanSongKeW-2.ttf')


def directory_selected(sender, app_data):
    '''当文件夹被选择时的回调函数'''
    selected_dir = app_data['file_path_name']
    if os.path.isdir(selected_dir):
        statistics = analyze_directory(selected_dir)
        update_display(statistics)


def update_display(statistics: dict[str, Any]):
    '''更新UI显示统计结果'''
    # 清除旧内容
    for child in dpg.get_item_children('results_window')[1]:
        dpg.delete_item(child)

    # 显示汇总信息
    dpg.add_text(f"总文件数: {statistics['total_files']}", parent='results_window')
    dpg.add_text(f"总行数: {statistics['total_lines']}", parent='results_window')
    dpg.add_separator(parent='results_window')

    # 按扩展名显示统计
    dpg.add_text('按文件类型统计:', parent='results_window')
    for ext, data in statistics['by_extension'].items():
        dpg.add_text(
            f"{ext}: {data['count']} 个文件, {data['lines']} 行",
            parent='results_window'
        )
    dpg.add_separator(parent='results_window')

    # 显示每种扩展名的行数前5文件
    for ext, files in statistics['top_files_by_extension'].items():
        if files:  # 只显示有文件的扩展名
            dpg.add_text(f"{ext} 行数前5的文件:", parent='results_window')
            for i, file in enumerate(files, 1):
                dpg.add_text(
                    f"{i}. {file['path']} - {file['lines']} 行",
                    parent='results_window',
                    indent=20
                )
            dpg.add_separator(parent='results_window')

    update_bar_charts(statistics)


def update_bar_charts(statistics: dict[str, Any]):
    def update_bar_chart_part1():
        with dpg.plot(label='文件数', parent='results_window',
                      height=300, width=-1, tag='file_count_chart'):
            x_axis_tag = 'file_count_x_axis'
            y_axis_tag = 'file_count_y_axis'

            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label='文件类型', tag=x_axis_tag)
            x_axis_ticks = tuple(zip(
                extensions,
                range(len(extensions)),
            ))
            dpg.set_axis_ticks(x_axis_tag, x_axis_ticks)
            dpg.set_axis_limits(x_axis_tag, 0, len(extensions))

            with dpg.plot_axis(dpg.mvYAxis, label='数量', tag=y_axis_tag):
                dpg.add_bar_series(
                    list(range(len(extensions))),
                    file_counts,
                    label='文件数',
                    weight=0.6
                )
            dpg.set_axis_limits(y_axis_tag, 0, max(file_counts) * 1.1)

        with dpg.plot(label='行数', parent='results_window',
                      height=300, width=-1, tag='file_lines_chart'):
            x_axis_tag = 'file_lines_x_axis'
            y_axis_tag = 'file_lines_y_axis'
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label='文件类型', tag=x_axis_tag)
            x_axis_ticks = tuple(zip(
                extensions,
                range(len(extensions)),
            ))
            dpg.set_axis_ticks(x_axis_tag, x_axis_ticks)
            dpg.set_axis_limits(x_axis_tag, 0, len(extensions))

            with dpg.plot_axis(dpg.mvYAxis, label='数量', tag=y_axis_tag):
                dpg.add_bar_series(
                    list(range(len(extensions))),
                    line_counts,
                    label='行数',
                    weight=0.6
                )
            dpg.set_axis_limits(y_axis_tag, 0, max(line_counts) * 1.1)

    def update_bar_chart_part2():
        '''为每个扩展名创建单独的柱状图'''
        for ext in extensions:
            files = statistics['top_files_by_extension'].get(ext, [])
            if not files:
                continue

            # 提取文件名和行数
            filenames = [os.path.basename(f['path']) for f in files]
            lines = [f['lines'] for f in files]

            with dpg.plot(label=f'{ext} 行数前5文件', parent='results_window',
                          height=300, width=-1, tag=f'top_files_chart_{ext}'):
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
                dpg.set_axis_limits(y_axis_tag, 0, max(lines) * 1.2)

                # 设置X轴标签
                x_axis_ticks = tuple(zip(
                    filenames,
                    range(len(filenames)),
                ))
                dpg.set_axis_ticks(x_axis_tag, x_axis_ticks)
            dpg.add_spacer(height=10, parent='results_window')

    # 删除旧的图表
    for tag in ['file_type_chart'] + [f'top_files_chart_{ext}' for ext in statistics['by_extension']]:
        if dpg.does_item_exist(tag):
            dpg.delete_item(tag)

    # 第一个图表：文件类型统计
    extensions = list(statistics['by_extension'].keys())
    file_counts = [data['count'] for data in statistics['by_extension'].values()]
    line_counts = [data['lines'] for data in statistics['by_extension'].values()]

    update_bar_chart_part1()
    dpg.add_spacer(height=20, parent='results_window')
    update_bar_chart_part2()


def add_font_for_dpg():
    with dpg.font_registry():
        with dpg.font(chinese_font_path, 18) as font1:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
            dpg.bind_font(font1)


def main():
    dpg.create_context()
    add_font_for_dpg()
    dpg.create_viewport(title='文件统计工具', width=800, height=600)

    with dpg.window(label='主窗口', tag='main_window'):
        # 文件夹选择组件
        dpg.add_text('选择要分析的文件夹:')
        dpg.add_button(
            label='选择文件夹',
            callback=lambda: dpg.show_item('file_dialog')
        )

        # 结果显示区域
        dpg.add_child_window(
            tag='results_window',
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
    dpg.set_primary_window('main_window', True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()
