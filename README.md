[TOC]

# uv初体验：用Dear PyGui写一个Python代码行数统计应用

## 引言

看了这个视频，想试试。

## 安装uv、初始化项目

执行命令：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

输出：

```
Downloading uv 0.7.12 (x86_64-pc-windows-msvc)
Installing to ~\.local\bin
  uv.exe
  uvx.exe
  uvw.exe
everything's installed!

To add ~\.local\bin to your PATH, either restart your shell or run:

    set Path=~\.local\bin;%Path%   (cmd)
    $env:Path = "~\.local\bin;$env:Path"   (powershell)
```

输入`uv --version`可检查uv是否安装成功。

输入`uv init code-line-statistics`，没有任何交互，即可创建一个模板项目。为了指定这个项目使用Python 3.10，执行：`uv python pin 3.10`。

我们Dear PyGui来实现GUI程序，装一下：`uv add dearpygui`

然后准备一段Dear PyGui Hello World代码：

```python
import dearpygui.dearpygui as dpg


def main():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=300)

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")
        dpg.add_button(label="Save")
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
```

运行：`uv run main.py`

## 常规：解决字体问题

在网上随便找了一个中文字体：[传送门](https://www.fonts.net.cn/fonts-zh/tag-songti-1.html)。然后改代码：

```python
chinese_font_path = os.path.join('fonts', 'ShanHaiJiGuJiangNanSongKeW-2.ttf')

def add_font_for_dpg():
    with dpg.font_registry():
        with dpg.font(chinese_font_path, 18) as font1:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
            dpg.bind_font(font1)
```

在`dpg.create_context()`之后调用即可。但是，窗口标题的中文仍然是乱码。

## 常规：接入pytest实现单测

pytest是大多数项目都会用到的，不需要每个项目的虚拟环境都装一遍，可以用`uv tool install pytest`全局安装。

为了让单测包成功导入被测文件，需要修改一下项目结构，把python文件放进src文件夹，`__init__.py`可建可不建。然后`pyproject.toml`新增：

```ini
[tool.pytest.ini_options]
pythonpath = "src"
```

相应地，运行GUI程序的命令也变为`uv run src/main.py`。

最后正常执行`pytest --html=coverage/report.html`即可。