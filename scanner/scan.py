import cv2
import numpy as np
import os
from fpdf import FPDF


class DocScanner:

    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect


    def four_point_transform(self, image, pts):

        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = int(max(widthA, widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = int(max(heightA, heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped


    def detect_document(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)

        edged = cv2.Canny(gray, 75, 200)

        contours, _ = cv2.findContours(
            edged.copy(),
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for c in contours:

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                return approx.reshape(4,2)

        return None


    def scan(self, image):

        corners = self.detect_document(image)

        if corners is not None:
            warped = self.four_point_transform(image, corners)
        else:
            warped = image

        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

        scanned = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            21,
            15
        )

        return scanned


def create_pdf(images, output_path):

    pdf = FPDF()
    temp_files = []

    for i, img in enumerate(images):

        temp = f"temp_{i}.png"

        cv2.imwrite(temp, img)
        temp_files.append(temp)

        pdf.add_page()
        pdf.image(temp, x=0, y=0, w=210)

    pdf.output(output_path)

    for file in temp_files:
        os.remove(file)

    print(f"PDF created: {output_path}")