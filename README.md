# Stack-Sheet-Counter

```markdown
# Sheet Stack Counter App

This Streamlit app allows users to upload an image of sheet stacks and count the number of sheets based on detected lines. The app provides various image editing options to improve line detection accuracy.

## Features

- Upload an image (JPEG, PNG).
- Crop, rotate, resize, and adjust the brightness and contrast of the image.
- Detect and count the number of sheets in the uploaded image.
- Display the processed image with detected lines and midpoints.

## Installation

1. Clone the repository:

```bash
git clone [https://github.com/yourusername/sheet-stack-counter.git]
cd sheet-stack-counter
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7 or higher
- Streamlit
- OpenCV
- NumPy
- Pillow
- streamlit-cropper

## Usage

1. Run the Streamlit app:


streamlit run app.py


2. Open your web browser and navigate to `http://localhost:8501`.

3. Upload an image of sheet stacks using the sidebar.

4. Use the image editing options in the sidebar to adjust the image.

5. The app will display the number of sheets and show the processed image with detected lines and midpoints.

## Image Editing Options

- **Crop**: Crop the image to a square aspect ratio.
- **Rotate**: Rotate the image by a specified angle.
- **Resize**: Resize the image to specified width and height.
- **Brightness**: Adjust the brightness of the image.
- **Contrast**: Adjust the contrast of the image.
- **Circle Radius**: Adjust the radius of the circles drawn on the midpoints of detected lines.

## How It Works

1. **Preprocessing**: The uploaded image is converted to grayscale and Gaussian blur is applied to reduce noise. Canny edge detection is then performed.
2. **Line Detection**: Probabilistic Hough Line Transform is used to detect lines in the edge-detected image.
3. **Line Merging**: Detected lines are merged if they are close enough to each other.
4. **Midpoint Calculation**: Midpoints of the merged lines are calculated.
5. **Sheet Counting**: The number of midpoints is used to determine the number of sheets.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


### Explanation

- **Features**: Describes the main functionalities of the app.
- **Installation**: Provides step-by-step instructions to set up the project.
- **Requirements**: Lists the necessary dependencies.
- **Usage**: Explains how to run the app and use it.
- **Image Editing Options**: Details the available image editing options.
- **How It Works**: Summarizes the workflow of the image processing and sheet counting.
- **License**: States the licensing information.

