import sys
import os

# allow Streamlit to find scanner module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import cv2
import numpy as np
from scanner.scan import DocScanner, create_pdf

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Nirvan Document Scanner",
    page_icon="📄",
    layout="wide"
)

# -------------------------
# HEADER
# -------------------------

st.title("📄 Nirvan Document Scanner")

st.markdown(
"""
Convert photos of receipts or documents into a **clean multi-page scanned PDF**.

Upload multiple images → generate a scanned PDF → download instantly.
"""
)

st.divider()

# -------------------------
# FILE UPLOADER
# -------------------------

uploaded_files = st.file_uploader(
    "Upload document images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

scanner = DocScanner()

# -------------------------
# IMAGE PREVIEW
# -------------------------

if uploaded_files:

    st.subheader("📸 Uploaded Images")

    images = []

    cols = st.columns(3)

    for i, file in enumerate(uploaded_files):

        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        images.append(img)

        with cols[i % 3]:
            st.image(img, caption=file.name, width="stretch")

    st.divider()

    # -------------------------
    # GENERATE PDF BUTTON
    # -------------------------

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        if st.button("📄 Generate Scanned PDF", use_container_width=True):

            scanned_pages = []

            with st.spinner("Scanning documents..."):

                for img in images:
                    scanned = scanner.scan(img)
                    scanned_pages.append(scanned)

            os.makedirs("output", exist_ok=True)

            output_path = "output/scanned_document.pdf"

            create_pdf(scanned_pages, output_path)

            st.success("✅ PDF generated successfully!")

            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇ Download PDF",
                    data=f,
                    file_name="scanned_document.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

# -------------------------
# FOOTER
# -------------------------

st.divider()

st.markdown(
"""

Created by **Nirvan Chhajed**
"""
)