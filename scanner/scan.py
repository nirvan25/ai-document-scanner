import cv2
import numpy as np
import os
import argparse
import matplotlib.pyplot as plt

from matplotlib.patches import Polygon

from scanner import transform
from scanner import imutils
from scanner import polygon_interacter as poly_i


class DocScanner:

    def __init__(self, interactive=False):
        self.interactive = interactive

    def get_contour(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        edged = cv2.Canny(gray, 75, 200)

        contours, _ = cv2.findContours(
            edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for c in contours:

            peri = cv2.arcLength(c, True)

            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                return approx.reshape(4, 2)

        h, w = image.shape[:2]

        return np.array([[0, 0], [w, 0], [w, h], [0, h]])

    def scan(self, image_path):

        os.makedirs("output", exist_ok=True)

        image = cv2.imread(image_path)

        ratio = image.shape[0] / 500.0

        orig = image.copy()

        image = imutils.resize(image, height=500)

        screenCnt = self.get_contour(image)

        warped = transform.four_point_transform(orig, screenCnt * ratio)

        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            21,
            15,
        )

        basename = os.path.basename(image_path)

        output_path = "output/" + basename

        cv2.imwrite(output_path, thresh)

        print("Processed:", basename)


if __name__ == "__main__":

    ap = argparse.ArgumentParser()

    ap.add_argument("--image", required=True)

    args = vars(ap.parse_args())

    scanner = DocScanner()

    scanner.scan(args["image"])