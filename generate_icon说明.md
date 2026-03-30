# generate_icon.py 使用说明

## 概述
- `generate_icon.py` 是一个使用 Pillow（PIL）的简单脚本，用于生成带有随机配色与图形的 ICO 图标文件（包含多种尺寸）。默认在当前工作目录生成一个随机命名的 .ico 文件。

## 功能要点
- 生成带透明通道的正方形图像并保存为多尺寸的 ICO（16、32、48、64、128、256）。
- 随机选择背景形状：圆形、圆角矩形或方形。
- 在中心绘制一个内圈与固定文字 `AI+`，并根据背景色自动选择对比文字颜色（黑或白）。
- 可选地绘制一个小强调色圆点以增加变化。

## 依赖
- Python 3.x
- Pillow 库

安装 Pillow：
```bash
pip install pillow
```

注意：脚本中默认字体为 `arial.ttf`，若在当前环境中找不到该文件，脚本会回退到 Pillow 的默认位图字体，显示效果会不同。可将字体文件放在脚本可访问的位置并修改 `font_name` 变量。

## 命令行使用
在命令行运行脚本：

```bash
python generate_icon.py
```

可用参数：
- `--count, -n <N>`: 生成 N 个随机图标（默认 1）。
- `--seed <INT>`: 指定随机种子以复现相同结果（可选）。

示例：生成 5 个图标：
```bash
python generate_icon.py --count 5
```

示例：使用固定随机种子（可复现）：
```bash
python generate_icon.py --count 3 --seed 42
```

脚本在运行时会在当前工作目录生成文件名形如 `icon_<timestamp>_<hex>.ico`，并在每次生成后打印路径。

## 作为模块调用
脚本提供了可重用的函数签名，可在其它 Python 代码中直接调用：

```python
from generate_icon import make_icon

# 生成单个指定文件名的图标（可选 seed）
make_icon('my_icon.ico', seed=12345)
```

参数说明：
- `out_path`: 输出文件路径（例如 `'icon.ico'`）。
- `seed`: 可选整数，设置随机数种子以使生成结果可复现。

## 内部实现细节（便于扩展）
- 图像大小固定为 256x256，随后保存为 ICO 并包含多种目标尺寸（16–256）。
- 背景颜色随机，文本颜色根据背景亮度计算（简单亮度公式）。
- 文本固定为 `AI+`，字体大小会自适应以适配内圈宽度。

如果你想自定义：
- 更改文本内容：修改 `text = 'AI+'`。
- 更改字体或字体路径：修改 `font_name` 与 `font_size` 的初始值。
- 更改可选形状或添加更多装饰：编辑 `shape` 的选择或绘图逻辑。

## 常见问题与排查
- 报错 `ModuleNotFoundError: No module named 'PIL'`：未安装 Pillow，参见上方安装命令。
- 输出图标显示字体不正确或过小：将合适的 TTF 字体（如 `arial.ttf`）放到可访问位置，或修改 `font_name` 为系统上存在的字体路径。
- 在不同平台上 `arial.ttf` 可能不存在：在 Linux 下常用 `DejaVuSans.ttf`，可替换为该字体路径以获得更好兼容性。

## 许可与免责声明
- 该脚本为简单工具示例，如需用于生产环境，请自行审查与测试。脚本不携带额外许可证声明，请按项目需要补充 LICENSE。

---

如果需要，我可以：
- 将 `AI+` 改为可通过命令行传入的参数；
- 添加输出文件名模板选项（如 `--out-dir` 或 `--pattern`）；
- 或者把脚本打包为可直接运行的 exe（Windows）。
