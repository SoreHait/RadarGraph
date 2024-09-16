# Author: SoreHait

from PIL import Image, ImageDraw, ImageFont
from math import sin, cos, radians

# Constants Here
# should be more than 2, goes counterclockwise
AXES_TAGS = ['爆发', '底力', '技巧', '抽奖', '键盘', '狗屎', '-100号']
# correspond to AXES_TAGS, length should be same
AXES_VALUES = [2, 4, 10, 5, 0, 100, 100]
# initial angle of the first axis
INIT_ANGLE = 90
# value over this will go over boundary
BOUNDARY_VALUE = 10
# font path
FONT = 'NotoSansSC-Regular.ttf'
# inner bound color, '#RRGGBBAA'
INNER_BOUND_COLOR = '#FF8C9ED9'
# fill color, '#RRGGBBAA'
FILL_COLOR = '#FF8C9E7F'
# True = white background
BACKGROUND = True

assert len(AXES_TAGS) > 2
assert len(AXES_TAGS) == len(AXES_VALUES)

def ptoc(dist: float, angle: float) -> tuple[int, int]:
    x = round(dist * cos(radians(angle))) + 1000
    y = -round(dist * sin(radians(angle))) + 1000
    return x, y

def get_anchor(angle: float) -> str:
    angle %= 360
    if 0 <= angle < 22.5:
        return 'lm'
    elif 22.5 <= angle < 67.5:
        return 'lb'
    elif 67.5 <= angle < 112.5:
        return 'mb'
    elif 112.5 <= angle < 157.5:
        return 'rb'
    elif 157.5 <= angle < 202.5:
        return 'rm'
    elif 202.5 <= angle < 247.5:
        return 'rt'
    elif 247.5 <= angle < 292.5:
        return 'mt'
    elif 292.5 <= angle < 337.5:
        return 'lt'
    elif 337.5 <= angle < 360:
        return 'lm'

base = Image.new('RGBA', (2000, 2000))
base_draw = ImageDraw.Draw(base)

# draw axes
axes_segments = []
for idx in range(len(AXES_TAGS)):
    angle = idx * 360 / len(AXES_TAGS) + INIT_ANGLE
    segment = []
    for dist in range(15, 695, 25):
        segment.append(ptoc(dist, angle))
        if len(segment) >= 2:
            axes_segments.append(segment)
            segment = []
    if segment:
        segment.append(ptoc(695, angle))
        axes_segments.append(segment)
for segment in axes_segments:
    base_draw.line(segment, '#0000007F', 10)

# draw boundary
bound_coords = [ptoc(700, idx * 360 / len(AXES_TAGS) + INIT_ANGLE) for idx in range(len(AXES_TAGS))]
base_draw.polygon(bound_coords, outline='black', width=15)

# write axes text
axes_tag_coords = [ptoc(750, idx * 360 / len(AXES_TAGS) + INIT_ANGLE) for idx in range(len(AXES_TAGS))]
axes_tag_anchors = [get_anchor(idx * 360 / len(AXES_TAGS) + INIT_ANGLE) for idx in range(len(AXES_TAGS))]
font = ImageFont.truetype(FONT, 100)
for text, coord, anchor in zip(AXES_TAGS, axes_tag_coords, axes_tag_anchors):
    base_draw.text(coord, text, 'black', font, anchor)

# overlay
overlay = Image.new('RGBA', (2000, 2000))
overlay_draw = ImageDraw.Draw(overlay)
inner_bound_coords = [ptoc(AXES_VALUES[idx] / BOUNDARY_VALUE * 700, idx * 360 / len(AXES_TAGS) + INIT_ANGLE) for idx in range(len(AXES_TAGS))]
overlay_draw.polygon(inner_bound_coords, FILL_COLOR, INNER_BOUND_COLOR, 10)

# overlay the overlay over base
base.alpha_composite(overlay)

if BACKGROUND:
    base = Image.alpha_composite(Image.new('RGBA', (2000, 2000), 'white'), base)
base.save('output.png')
