import dlib
from PIL import Image
import argparse

from imutils import face_utils
import numpy as np

import moviepy.editor as mpy

parser = argparse.ArgumentParser()
parser.add_argument("-image", required=True, help="path to input image")
args = parser.parse_args()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68.dat')

MAX_WIDTH = 500
DEAL_TEXT_IMG = Image.open("helpers-img/text.png")
GLASS_IMG = Image.open("helpers-img/deals.png")

img = Image.open(args.image)
img_width, img_height = img.size
print("Width of image is: {0}".format(img_width))
print("Height of image is: {0}".format(img_height))

if img_width > 500:
    scaled_height = int(MAX_WIDTH * img_height / img_width)
    print("Scaled height is: {0}".format(scaled_height))

    img.thumbnail((MAX_WIDTH, scaled_height))
    img.save("images/scaled_img.jpg")

img_scaled = Image.open("images/scaled_img.jpg")
img_grey = img_scaled.convert("L")
img_grey.save("images/greyscale_img.jpg")

grey_img_arr = np.array(img_grey)

dets = detector(grey_img_arr)

if len(dets) > 0:
    print("Find {} faces".format(len(dets)))
    print("Rectangles of faces {}".format(dets))
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            i, d.left(), d.top(), d.right(), d.bottom()))

        deal_galses_width = d.right() - d.left()
        print("Deal glasses width: {}".format(deal_galses_width))

        shape = predictor(grey_img_arr, d)
        shape = face_utils.shape_to_np(shape)

        left_eye = shape[36:42]
        right_eye = shape[42:48]
        print("Left eye {}, right eye".format(left_eye, right_eye))

        left_eye_center = left_eye.mean(axis=0).astype("int")
        right_eye_center = right_eye.mean(axis=0).astype("int")
        print("Center of left eye {}, center of right eye {}".format(left_eye_center, right_eye_center))

        dx = left_eye_center[0] - right_eye_center[0]
        dy = left_eye_center[1] - right_eye_center[1]

        angle = np.rad2deg(np.arctan2(dy, dx))
        print("Angle {}".format(angle))

        # resize glases
        current_deal = GLASS_IMG.resize((deal_galses_width,
                                         int(deal_galses_width * GLASS_IMG.size[1] / GLASS_IMG.size[0]))
                                        , resample=Image.LANCZOS)
        current_deal.show()


else:
    print("No faces found")
    exit()


