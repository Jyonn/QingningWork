# coding=utf-8
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

'''
需要导入image库: pip install pillow
'''

_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
# init_chars = _numbers
fontType = os.path.join(os.path.dirname(__file__), '../../newsee/Base/AGALEGA-Regular.otf')  # 要注意修改路径


def create_validate_code(size=(120, 30),
                         chars=init_chars,
                         mode="RGBA",
                         bg_color=(255, 255, 255, 0),
                         fg_color=(0, 0, 255),
                         font_size=18,
                         font_type=fontType,
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance=2):
    """
    :todo: 生成验证码图片
    :param size: 图片的大小(宽,高),默认为(120,30)
    :param chars: 允许的字符集
    :param mode: 图片模式,默认为RGBA
    :param bg_color: 背景颜色,默认为透明#ffffff
    :param fg_color: 前景色,默认为蓝色#0000ff
    :param font_size: 验证字体大小
    :param font_type: 验证字体
    :param length: 验证码字符个数,默认为4个
    :param draw_lines: 是否划干扰线,默认为画
    :param n_line: 干扰线的条数, 格式元祖, 默认为(1,2)
    :param draw_points: 是否画干扰点
    :param point_chance: 干扰点出现概率,范围为[0,100]
    :return: [0]: PIL Image实例
    :return: [1]: 验证码图片中字符串
    """
    width, height = size  # 设置长宽
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)  # 创建画笔
    if draw_lines:  # 如果需要绘制干扰线
        create_lines(draw, n_line, width, height)
    if draw_points:  # 如果需要绘制干扰点
        create_points(draw, point_chance, width, height)

    strs = create_strs(draw, chars, length, font_type, font_size, width, height, fg_color)

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    return strs, img


def create_lines(draw, n_line, width, height):
    """绘制干扰线"""
    line_num = random.randint(n_line[0], n_line[1])  # 干扰线条数
    for i in range(line_num):
        # 起始点
        begin = (random.randint(0, width), random.randint(0, height))
        # 结束点
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=(0, 0, 0))


def create_points(draw, point_chance, width, height):
    """绘制干扰点"""
    chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

    for w in range(width):
        for h in range(height):
            tmp = random.randint(0, 100)
            if tmp > 100 - chance:
                draw.point((w, h), fill=(0, 0, 0))


def create_strs(draw, chars, length, font_type, font_size, width, height, fg_color):
    """绘制验证码字符"""
    c_chars = random.sample(chars, length)
    strs = ' %s ' % ''.join(c_chars)  # 每个字符前后以空格隔开

    font = ImageFont.truetype(font_type, font_size)
    font_width, font_height = font.getsize(strs)

    draw.text(((width - font_width) / 3, (height - font_height) / 3), strs, font=font, fill=fg_color)

    return ''.join(c_chars)
