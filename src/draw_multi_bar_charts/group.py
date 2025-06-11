import dearpygui.dearpygui as dpg

dpg.create_context()


def group1():
    # 第一个柱状图
    with dpg.plot(label="Bar Chart 1", height=300, width=390):
        dpg.add_plot_axis(dpg.mvXAxis, label="X Axis")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Y Axis")
        dpg.add_bar_series([1, 2, 3, 4], [10, 20, 30, 40], parent=y_axis)

    # 第二个柱状图
    with dpg.plot(label="Bar Chart 2", height=300, width=390):
        dpg.add_plot_axis(dpg.mvXAxis, label="X Axis")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Y Axis")
        dpg.add_bar_series([1, 2, 3, 4], [15, 25, 35, 45], parent=y_axis)


def group2():
    with dpg.plot(label="Bar Chart 3", height=300, width=390):
        dpg.add_plot_axis(dpg.mvXAxis, label="X Axis")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Y Axis")
        dpg.add_bar_series([1, 2, 3, 4], [10, 20, 30, 40], parent=y_axis)

    with dpg.plot(label="Bar Chart 4", height=300, width=390):
        dpg.add_plot_axis(dpg.mvXAxis, label="X Axis")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Y Axis")
        dpg.add_bar_series([1, 2, 3, 4], [15, 25, 35, 45], parent=y_axis)


with dpg.window(label="Multi Bar Charts"):
    with dpg.group(horizontal=True):
        group1()
    with dpg.group():
        group2()

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
