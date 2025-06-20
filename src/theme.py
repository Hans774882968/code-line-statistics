from consts import *
import dearpygui.dearpygui as dpg


def add_font_for_dpg():
    with dpg.font_registry():
        with dpg.font(CHINESE_FONT_PATH, 18) as font1:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
            dpg.bind_font(font1)


def set_global_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_FramePadding,
                0, 4,
                category=dpg.mvThemeCat_Core
            )

        dpg.bind_theme(global_theme)


def set_operations_window_theme():
    with dpg.theme(tag=OPERATIONS_WINDOW_THEME):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_FramePadding,
                0, 12,
                category=dpg.mvThemeCat_Core
            )
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_style(
                dpg.mvStyleVar_FramePadding,
                8, 8,
                category=dpg.mvThemeCat_Core
            )

    with dpg.theme(tag=ICON_TEXT_THEME):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_ItemSpacing,
                8, 0,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_FramePadding,
                0, 0,
                category=dpg.mvThemeCat_Core
            )
