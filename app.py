import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance
from io import BytesIO
from streamlit_cropper import st_cropper

def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    for _ in range(5):
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gray, 50, 150)
    return gray, edges

def detect_lines(edges):
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=300)
    return lines

def merge_lines(lines):
    if lines is None:
        return []

    merged_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        merged = False
        for i, (mx1, my1, mx2, my2) in enumerate(merged_lines):
            if abs(y1 - my1) < 10 and abs(y2 - my2) < 10:
                merged_lines[i] = (min(x1, mx1), my1, max(x2, mx2), my2)
                merged = True
                break
        if not merged:
            merged_lines.append((x1, y1, x2, y2))
    return merged_lines

def calculate_midpoints(lines, image_width):
    fixed_x = image_width // 2  # Center of the image horizontally
    midpoints = []
    for x1, y1, x2, y2 in lines:
        mid_y = (y1 + y2) // 2  # Vertical midpoint
        midpoints.append((fixed_x, mid_y))
    return np.array(midpoints)

def count_sheets(image, circle_radius):
    gray, edges = preprocess_image(image)
    
    # Morphological transformations to close gaps
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    lines = detect_lines(edges)
    if lines is None or len(lines) == 0:
        return 0, gray, edges, np.zeros_like(image), image
    
    merged_lines = merge_lines(lines)
    if len(merged_lines) == 0:
        return 0, gray, edges, np.zeros_like(image), image
    
    image_width = image.shape[1]
    midpoints = calculate_midpoints(merged_lines, image_width)
    
    # Draw detected lines and midpoints
    line_img = np.zeros_like(image)
    for x1, y1, x2, y2 in merged_lines:
        cv2.line(line_img, (x1, y1), (x2, y2), (255, 255, 255), 2)
    
    processed_image = np.array(image.copy())
    for (mid_x, mid_y) in midpoints:
        cv2.circle(processed_image, (mid_x, mid_y), circle_radius, (0, 255, 0), 2)
    
    sheet_count = len(midpoints)
    return sheet_count, gray, edges, line_img, processed_image

def main():
    st.set_page_config(page_title="Sheet Stack Counter", layout="wide")
    
    st.title("Sheet Stack Counter App")

    # Sidebar for image editing options
    st.sidebar.title("Image Editing Options")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(BytesIO(uploaded_file.read()))
        
        st.sidebar.write("### Adjustments")
        crop = st.sidebar.checkbox("Crop")
        rotate = st.sidebar.slider("Rotate", -180, 180, 0)
        resize = st.sidebar.checkbox("Resize")
        resize_width = st.sidebar.slider("Width", 10, image.width, image.width)
        resize_height = st.sidebar.slider("Height", 10, image.height, image.height)
        brightness = st.sidebar.slider("Brightness", 0.5, 3.0, 1.0)
        contrast = st.sidebar.slider("Contrast", 0.5, 3.0, 1.0)
        circle_radius = st.sidebar.slider("Circle Radius", 1, 20, 5)
        
        if crop:
            cropped_image = st_cropper(image, aspect_ratio=(1, 1), return_type="image")
        else:
            cropped_image = image

        edited_image = cropped_image.rotate(rotate)
        if resize:
            edited_image = edited_image.resize((resize_width, resize_height))
        enhancer = ImageEnhance.Brightness(edited_image)
        edited_image = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(edited_image)
        edited_image = enhancer.enhance(contrast)
        
        # st.write("## Edited Image")
        
        image = np.array(edited_image.convert('RGB'))
        
        sheet_count, gray, edges, line_img, processed_image = count_sheets(image, circle_radius)
        
        # Create columns
        col1, col2 = st.columns([1, 2])
        st.markdown(f"<h2 style='text-align: center;'>Number of sheets: {sheet_count}</h2>", unsafe_allow_html=True)
        
        with col1:
            st.image(gray, caption="Grayscale Image", use_column_width=True, channels="GRAY",width=300)
            st.image(edited_image,caption="Edited Image", use_column_width=True,width=300)
            st.image(edges, caption="Canny Edges", use_column_width=True, channels="GRAY",width=300)
        with col2:
            # st.image(image, caption="Uploaded Image", use_column_width=True)
            st.image(line_img, caption="Detected Lines", use_column_width=True, channels="GRAY",width=300)
            st.image(processed_image, caption="Contours and Midpoints", use_column_width=True,width=300)
        
    st.sidebar.write("## Info")
    st.sidebar.write("""
        This application allows you to upload an image of sheet stacks and 
        count the number of sheets based on detected lines. 
        Use the options to crop, rotate, resize, and adjust the brightness 
        and contrast of the image to improve line detection accuracy.
    """)

if __name__ == "__main__":
    main()

