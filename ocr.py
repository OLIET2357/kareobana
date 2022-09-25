# https://qiita.com/bohemian916/items/67f22ee7aeac103dd205#wordbox

import pyocr
import pyocr.builders
import argparse
import cv2
from PIL import Image

import tensorflow as tf
import numpy as np

import sys
import os

DEBUG_IMAGES_DIR = 'debug_images'

# https://ja.wikipedia.org/wiki/Shift_JIS#%E5%8C%BA%E7%82%B9%E7%95%AA%E5%8F%B7%E3%81%8B%E3%82%89%E3%81%AE%E5%A4%89%E6%8F%9B


def s1(k, t):
    if 1 <= k <= 62:
        return (k+257)//2
    if 63 <= k <= 94:
        return (k+385)//2


def s2(k, t):
    if k % 2 == 1:
        if 1 <= t <= 63:
            return t+63
        if 64 <= t <= 94:
            return t+64
    else:
        return t+158


parser = argparse.ArgumentParser(description='tesseract ocr test')
parser.add_argument('image', help='image path')
parser.add_argument('-d', '--debug', action='store_true',
                    help='save debug images')

args = parser.parse_args()

IMAGE_PATH = args.image
DEBUG = args.debug

if DEBUG:
    os.makedirs(DEBUG_IMAGES_DIR, exist_ok=True)

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR'  # インストールしたTesseract-OCRのpath
TESSDATA_PATH = r'C:\Program Files\Tesseract-OCR\tessdata'  # tessdataのpath

os.environ["PATH"] += os.pathsep + TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH


tools = pyocr.get_available_tools()

if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]


res = tool.image_to_string(Image.open(IMAGE_PATH),
                           lang="jpn",
                           builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6))

# draw result
img = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img_lines = []
for i, d in enumerate(res, 1):
    print(d.content)
    print(d.position)
    pos = d.position
    cv2.rectangle(img_out, pos[0], pos[1], (0, 0, 255), 2)
    img_crop = img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]]
    img_lines.append(img_crop)
    if DEBUG:
        cv2.imwrite(os.path.join(DEBUG_IMAGES_DIR,
                    'line_%d.png' % i), img_crop)

model = tf.keras.models.load_model(
    r"D:\Downloads\cp932_chars\test.files\hex_100\saved_model")

for l, img_line in enumerate(img_lines, 1):
    h, w = img_line.shape
    _, img_th = cv2.threshold(img_line, -1, 255, cv2.THRESH_OTSU)
    img_boxes = []
    start = 0
    for x in range(w+1):
        if x == w or np.count_nonzero(img_th[:, x] == 0) == 0 or x-start >= h:
            end = x
            if end-start <= 1:
                start = x
                continue
            img_box = img_line[:, start:end]
            img_boxes.append(img_box)
            start = x

    for c, img_box in enumerate(img_boxes, 1):
        if DEBUG:
            cv2.imwrite(os.path.join(DEBUG_IMAGES_DIR,
                                     'char_%d_%d.png' % (l, c)), img_box)

        img = cv2.copyMakeBorder(
            img_box, 0, 0, 0, img_box.shape[0]-img_box.shape[1], cv2.BORDER_CONSTANT, value=255)
        # cv2.imshow(str(c), img)
        img = cv2.bitwise_not(img)
        img = cv2.resize(img, (28, 28))

        X = (img.astype(np.float32)/255).reshape(1, 1, 28, 28)
        y = model(Input=X)
        # kuten = np.argmax(y)
        ss = []
        for h in np.argsort(y[0][0])[-10:]:
            if h < 0x100:
                bs = [h]
            else:
                bs = [h//0x100, h % 0x100]
            s = bytearray(bs).decode('cp932')
            ss.append(s)
        print(ss)

    #     print(s, end='')
    # print()

# cv2.waitKey(0)
# cv2.destroyAllWindows()

if DEBUG:
    cv2.imwrite(os.path.join(DEBUG_IMAGES_DIR, 'line_boxes.png'),  img_out)

# cv2.imshow('image', img_out)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# model = tf.keras.models.load_model(
#     r"D:\Downloads\cnn\saved_model_kuten_1000\saved_model.pb")

# y = model(Input=X)
