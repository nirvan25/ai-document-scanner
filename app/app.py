import sys
import os

# Allow Streamlit to locate the scanner module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import cv2
import numpy as np
from scanner.scan import DocScanner, create_pdf

st.set_page_config(
    page_title="Nirvan Document Scanner",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Nirvan Document Scanner")

st.markdown(
"""
Upload photos of receipts or documents and convert them into a **clean multi-page scanned PDF**.
"""
)

uploaded_files = st.file_uploader(
    "Upload document images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:

    st.subheader("Uploaded Images")

    images = []
    cols = st.columns(3)

    for i, file in enumerate(uploaded_files):

        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        images.append(img)

        with cols[i % 3]:
            st.image(img, caption=file.name, width="stretch")

    if st.button("Generate PDF"):

        scanner = DocScanner()
        scanned_pages = []

        with st.spinner("Scanning documents..."):

            for img in images:
                scanned = scanner.scan(img)
                scanned_pages.append(scanned)

        os.makedirs("output", exist_ok=True)

        output_path = "output/scanned_document.pdf"

        create_pdf(scanned_pages, output_path)

        st.success("✅ PDF created successfully!")

        with open(output_path, "rb") as f:
            st.download_button(
                label="⬇ Download PDF",
                data=f,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )