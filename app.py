# app.py
import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner")
st.write("Upload a document image, convert it to black & white like Adobe Scan, and download it as a PDF.")

uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["jpg", "jpeg", "png"]
)

def process_document(image):
    """
    Convert document image to clean black & white scan.
    """
    # Convert PIL image to OpenCV format
    img = np.array(image)

    # Convert RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize for better processing
    height = 1000
    ratio = height / img.shape[0]
    width = int(img.shape[1] * ratio)
    img = cv2.resize(img, (width, height))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise removal
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold for scanner effect
    scanned = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return scanned

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("✨ Scan Document"):
        with st.spinner("Processing..."):

            scanned = process_document(image)

            st.subheader("Scanned Black & White Image")
            st.image(scanned, clamp=True, use_container_width=True)

            # Convert OpenCV image to PIL
            scanned_pil = Image.fromarray(scanned)

            # Convert to PDF
            pdf_bytes = BytesIO()
            scanned_pil.convert("RGB").save(pdf_bytes, format="PDF")
            pdf_bytes.seek(0)

            st.download_button(
                label="⬇ Download PDF",
                data=pdf_bytes,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )
