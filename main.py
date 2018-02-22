import dlib
from PIL import Image
import argparse

from imutils import face_utils
import numpy as np

import moviepy.editor as mpy


class DealWithIt(object):

    MAX_WIDTH = 500

    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68.dat')
        self.deal_text_img = Image.open("helpers-img/text.png")
        self.glass_img = Image.open("helpers-img/deals.png")
        self.img = None
        self.img_width = None
        self.img_height = None

    def set_image_path(self, path):
        self.img = Image.open(path)

    def set_width_and_height(self):
        self.img_width, self.img_height = self.img
        print("Width of image is: {0}".format(self.img_width))
        print("Height of image is: {0}".format(self.img_height))

    def scale_img(self):
        if self.img_width > 500:
            scaled_height = int(self.MAX_WIDTH * self.img_width / self.img_height)
            print("Scaled height is: {0}".format(scaled_height))
            self.img.thumbnail((self.MAX_WIDTH, scaled_height))

    def convert_to_greyscale(self):
        img_grey = self.img.convert("L")
        return np.array(img_grey)


parser = argparse.ArgumentParser()
parser.add_argument("-image", required=True, help="path to input image")
parser.add_argument("-output", required=True, help="name of output gif")
args = parser.parse_args()


dets = detector(grey_img_arr)

faces = []

if len(dets) > 0:
    print("Find {} faces".format(len(dets)))
    print("Rectangles of faces {}".format(dets))
    for i, d in enumerate(dets):
        face = {}

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

        current_deal = current_deal.rotate(angle, expand=True)
        current_deal = current_deal.transpose(Image.FLIP_TOP_BOTTOM)

        face['glass_image'] = current_deal
        left_eye_x = left_eye[0, 0] - deal_galses_width // 4
        lefy_eye_y = left_eye[0, 1] - deal_galses_width // 6
        face['final_pos'] = (left_eye_x, lefy_eye_y)
        faces.append(face)
else:
    print("No faces found")
    exit()

# during time of gif
duration = 4

def make_frame(t):
    draw_image = img.convert("RGBA")

    if t == 0:
        return np.asarray(draw_image)

    for face in faces:
        if t <= duration - 2:
            current_x = int(face['final_pos'][0])
            current_y = int(face['final_pos'][1] * t / (duration - 2))
            draw_image.paste(face['glass_image'], (current_x, current_y), face['glass_image'])
        else:
            draw_image.paste(face['glass_image'], face['final_pos'], face['glass_image'])
            draw_image.paste(DEAL_TEXT_IMG, (75, draw_image.height - 100), DEAL_TEXT_IMG)

    return np.asarray(draw_image)


animation = mpy.VideoClip(make_frame, duration=duration)
animation.write_gif("deal.gif", fps=4)

