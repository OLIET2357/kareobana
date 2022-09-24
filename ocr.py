# https://qiita.com/bohemian916/items/67f22ee7aeac103dd205#wordbox

import pyocr
import pyocr.builders
import argparse
import cv2
from PIL import Image

import sys
import os

DEBUG_IMAGES_DIR = 'debug_images'

os.makedirs(DEBUG_IMAGES_DIR, exist_ok=True)

parser = argparse.ArgumentParser(description='tesseract ocr test')
parser.add_argument('image', help='image path')
parser.add_argument('-d', '--debug', action='store_true',
                    help='save debug images')

args = parser.parse_args()

IMAGE_PATH = args.image
DEBUG = args.debug

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
img = cv2.imread(IMAGE_PATH)
img_out = img.copy()
img_lines = []
for i, d in enumerate(res, 1):
    print(d.content)
    print(d.position)
    pos = d.position
    cv2.rectangle(img_out, pos[0], pos[1], (0, 0, 255), 2)
    img_crop = img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]]
    img_lines.append(img_crop)
    cv2.imwrite(os.path.join(DEBUG_IMAGES_DIR, 'line_%d.png' % i), img_crop)

cv2.imwrite(os.path.join(DEBUG_IMAGES_DIR, 'line_boxes.png'),  img_out)

cv2.imshow('image', img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()
