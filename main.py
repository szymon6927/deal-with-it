import dlib
from PIL import Image
import argparse

from imutils import face_utils
import numpy as np

import moviepy.editor as mpy


class DealWithIt(object):

    def __init__(self, image_path, output):
        self.image_path = image_path
        self.output = output
        self.img = None
        self.deal_text_img = Image.open("helpers-img/text.png")
        self.glass_img = Image.open("helpers-img/deals.png")
        self.duration = 4
        self.face_elements = []

    def load_image(self):
        self.img = Image.open(self.image_path)

    def get_width_and_height(self):
        img_width, img_height = self.img.size
        print("Width of image is: {0}".format(img_width))
        print("Height of image is: {0}".format(img_height))
        return [img_width, img_height]

    def scale_img(self):
        """Scale image if width grater than 500"""
        max_width = 500
        img_width, img_height = self.get_width_and_height()
        if img_width > 500:
            scaled_height = int(max_width * img_width / img_height)
            print("Scaled height is: {0}".format(scaled_height))
            self.img.thumbnail((max_width, scaled_height))

    def convert_to_greyscale(self):
        """Return an pixels array of greyscaled image"""
        img_grey = self.img.convert("L")
        return np.array(img_grey)

    def count_glass_width(self, rect):
        """Count meme glass based on face rect"""
        print("Deal glasses width: {}".format(rect.right() - rect.left()))
        return rect.right() - rect.left()

    def find_faces(self):
        detector = dlib.get_frontal_face_detector()
        img_grey = self.convert_to_greyscale()
        rectangles = detector(img_grey, 0)
        if len(rectangles) > 0:
            return rectangles
        else:
            print("No faces find, exiting.")
            exit()

    def face_orientation(self, rect):
        """predictor used to detect orientation in place where current face is"""
        predictor = dlib.shape_predictor('shape_predictor_68.dat')
        img_grey = self.convert_to_greyscale()
        shape = predictor(img_grey, rect)
        shape = face_utils.shape_to_np(shape)
        return shape

    def detect_eye(self, rect):
        """Select outlines of eyes and return angle and position of left and right eye"""
        shape = self.face_orientation(rect)

        left_eye = shape[36:42]
        right_eye = shape[42:48]

        # compute the center of mass for each eye
        left_eye_center = left_eye.mean(axis=0).astype("int")
        right_eye_center = right_eye.mean(axis=0).astype("int")

        # compute the angle between the eye centroids
        dx = left_eye_center[0] - right_eye_center[0]
        dy = left_eye_center[1] - right_eye_center[1]
        angle = np.rad2deg(np.arctan2(dy, dx))
        return [left_eye, right_eye, angle]

    def set_gif_elements(self):
        """Set required element for gif animation, like prepared glasses, eye position"""
        gif_elemets = []
        rects = self.find_faces()

        for rect in rects:
            element = {}  # dict for elements animated on final gif

            glases_width = self.count_glass_width(rect)

            left_eye, right_eye, angle = self.detect_eye(rect)
            # resize glasses to face width
            adjusted_glases = self.glass_img.resize((glases_width,
                                                    int(glases_width * self.glass_img.size[1]/self.glass_img.size[0])),
                                                    resample=Image.LANCZOS)

            # rotate and flip to fit eye centers
            adjusted_glases = adjusted_glases.rotate(angle, expand=True)
            adjusted_glases = adjusted_glases.transpose(Image.FLIP_TOP_BOTTOM)

            # add the scaled image to a list, shift the final position to the
            # left of the leftmost eye
            element['glasses_image'] = adjusted_glases

            left_eye_x = left_eye[0, 0] - glases_width // 5
            left_eye_y = right_eye[0, 1] - glases_width // 5
            element['final_eye_pos'] = (left_eye_x, left_eye_y)

            gif_elemets.append(element)

        self.face_elements = gif_elemets

    def make_frame(self, t):
        draw_img = self.img.convert('RGBA')  # returns copy of original image

        if t == 0:
            return np.asarray(self.img.convert('RGBA'))

        for face in self.face_elements:
            if t <= self.duration - 2:
                current_x = int(face['final_eye_pos'][0])
                current_y = int(face['final_eye_pos'][1] * t / (self.duration - 2))
                draw_img.paste(face['glasses_image'], (current_x, current_y), face['glasses_image'])
            else:
                draw_img.paste(face['glasses_image'], face['final_eye_pos'], face['glasses_image'])
                draw_img.paste(self.deal_text_img, (75, draw_img.height - 75), self.deal_text_img)

        return np.asarray(draw_img)

    def make_gif(self):
        self.load_image()
        self.scale_img()
        self.set_gif_elements()
        animation = mpy.VideoClip(self.make_frame, duration=self.duration)
        animation.to_gif(self.output, fps=4)


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-image", required=True, help="path to input image")
    parser.add_argument("-output", required=True, help="name of output gif")
    return parser.parse_args()


if __name__ == "__main__":
    args = cli_parser()
    meme = DealWithIt(args.image, args.output)
    meme.make_gif()




