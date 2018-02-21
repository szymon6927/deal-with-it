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