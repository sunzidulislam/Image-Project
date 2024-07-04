# Playing Card Detection and Identification

## Introduction

This project involves the detection and identification of playing cards from an image using Python and OpenCV. The system captures images of playing cards, processes them to detect card contours, and matches them to template images to identify the rank and suit of each card.

## Objectives

- Develop a method to detect and identify playing cards from an image.
- Optimize system performance by relying on the similarity between template images and patches in the transformed card image.

## Methodology

### 1. Image Acquisition
- Frames are captured from a webcam using OpenCV (`cv2.VideoCapture`).
- The parameters are initialized, and an initial image is loaded for manipulation.

### 2. Preprocessing
- Apply a Gaussian filter to blur the image.
- Convert the grayscale image into a binary image based on intensity levels using `cv2.threshold`.

### 3. Edge Detection
- Use Canny edge detection to find edges in the image.

### 4. Contour Detection
- Find contours and sort them by contour size.
- Determine which of the contours are cards based on specific criteria (size, shape, etc.).

### 5. Perspective Transformation
- Use the card's perimeter to approximate corner points and find the width and height of the card's bounding rectangle.
- Perform a perspective transformation to get a top-down view of the card.

### 6. Feature Extraction
- Split the card image into rank and suit images.
- Extract the rank and suit by isolating the respective regions.

### 7. Matching
- Match the extracted rank and suit images to the template images.
- Combine the best rank and suit matches to identify the card.

## Input & Output Images
![Inputimage](https://github.com/sunzidulislam/Image-Project/assets/60359567/61a1e306-3414-4cf4-8704-917c38a78b8c) ![Preprocessing](https://github.com/sunzidulislam/Image-Project/assets/60359567/5a4e9333-4270-4acf-9331-5773ea14cfa3) ![Thresholding](https://github.com/sunzidulislam/Image-Project/assets/60359567/18dfc421-f6c6-40d5-8841-9b9446a3cf7d) ![Contour Detection](https://github.com/sunzidulislam/Image-Project/assets/60359567/4ed25a47-39cb-4328-895c-c3341011f3bb) ![Rank Image](https://github.com/sunzidulislam/Image-Project/assets/60359567/28435b4d-17de-42b9-a9b7-ed2de70f3ea2) ![Suit Image](https://github.com/sunzidulislam/Image-Project/assets/60359567/483d9e87-38be-4664-a998-12db7dc3b85f) ![Final Image](https://github.com/sunzidulislam/Image-Project/assets/60359567/cc59651d-de15-44ab-90c3-c35dc6efe716)

## Results

- The system successfully detects and identifies playing cards from images.
- The detected cards and identified features are visually represented on the original images for easy verification and analysis.

## Programming Environment

- **Programming Language:** Python 3.11.3
- **IDE:** Spyder, Visual Studio Code
- **Libraries:** OpenCV

## Conclusion

The card detection and recognition system uses a structured methodology involving multiple steps to ensure accuracy and efficiency. Potential enhancements include integrating advanced noise reduction techniques, adaptive thresholding, and machine learning algorithms.

## References

1. Bradski, G. (2000). The OpenCV Library. Dr. Dobb’s Journal of Software Tools.
2. Bradley, D., & Roth, G. (2007). Adaptive Thresholding Using the Integral Image.
3. Gonzalez, R. C., & Woods, R. E. (2002). Digital Image Processing. Prentice Hall.

## Acknowledgments

Special thanks to Abu Sayeed for his support.
