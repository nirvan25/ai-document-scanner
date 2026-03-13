import cv2
import os
import argparse
from fpdf import FPDF


class DocScanner:

    def scan_image(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            print(f"Error loading image: {image_path}")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Blur to remove noise
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive threshold to create "scanned" effect
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

        temp_file = f"temp_page_{i}.png"

        cv2.imwrite(temp_file, img)

        temp_files.append(temp_file)

        pdf.add_page()

        pdf.image(temp_file, x=0, y=0, w=210)

    pdf.output(output_path)

    # remove temp images
    for file in temp_files:
        os.remove(file)

    print(f"PDF created successfully: {output_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--images",
        nargs="+",
        required=True,
        help="List of images to scan"
    )

    parser.add_argument(
        "--output",
        default="output/scanned_document.pdf",
        help="Output PDF path"
    )

    args = parser.parse_args()

    scanner = DocScanner()

    scanned_pages = []

    for img_path in args.images:

        print(f"Processing: {img_path}")

        page = scanner.scan_image(img_path)

        if page is not None:
            scanned_pages.append(page)

    if scanned_pages:

        os.makedirs("output", exist_ok=True)

        create_pdf(scanned_pages, args.output)

    else:
        print("No valid pages scanned.")