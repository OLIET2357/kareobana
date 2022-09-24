# https://qiita.com/bohemian916/items/67f22ee7aeac103dd205#linebox

import pyocr
import pyocr.builders
import argparse
import cv2
from PIL import Image

import sys
import os

parser = argparse.ArgumentParser(description='tesseract ocr test')
parser.add_argument('image', help='image path')
args = parser.parse_args()

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


res = tool.image_to_string(Image.open(args.image),
                           lang="jpn",
                           builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6))

# draw result
out = cv2.imread(args.image)
for d in res:
    print(d.content)
    print(d.position)
    cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2)

cv2.imshow('image', out)
cv2.waitKey(0)
cv2.destroyAllWindows()
