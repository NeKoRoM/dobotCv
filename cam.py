import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls

class ImageAnalyzer:
    def __init__(self, exposure=100, low_hsv=(0, 0, 0), high_hsv=(180, 255, 255)):
        """
        Initialize the ImageAnalyzer class.

        Parameters:
        - exposure: int, exposure time for the camera.
        - low_hsv: tuple, lower HSV threshold for filtering.
        - high_hsv: tuple, upper HSV threshold for filtering.
        """
        self.exposure = exposure
        self.low_hsv = np.array(low_hsv, np.uint8)
        self.high_hsv = np.array(high_hsv, np.uint8)
        
        # Initialize camera
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        self.picam2.start()

    def set_exposure(self, exposure):
        """Set the exposure time."""
        self.exposure = exposure
        self.picam2.set_controls({"ExposureTime": self.exposure})

    def set_hsv_thresholds(self, low_hsv, high_hsv):
        """Set the HSV thresholds for filtering."""
        self.low_hsv = np.array(low_hsv, np.uint8)
        self.high_hsv = np.array(high_hsv, np.uint8)

    def find_contours(self, binary_image):
        """
        Find contours in a binary image using OpenCV.

        Parameters:
        - binary_image: numpy.ndarray, binary image to find contours in.

        Returns:
        - contours: list, detected contours.
        - hierarchy: numpy.ndarray, contour hierarchy.
        """
        contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    def analyze_frame(self):
        """
        Capture a frame from the camera and perform contour analysis.

        Returns:
        - output_image: numpy.ndarray, annotated frame.
        - fps: float, frames per second of processing.
        """
        frame = self.picam2.capture_array()

        # Convert to HSV and apply thresholding
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        binary_mask = cv2.inRange(img_hsv, self.low_hsv, self.high_hsv)

        # Find contours
        contours, hierarchy = self.find_contours(binary_mask)
        output_image = frame.copy()
        min_area = 1000

        if hierarchy is not None:
            for i, contour in enumerate(contours):
                if cv2.contourArea(contour) < min_area:
                    continue

                if hierarchy[0][i][2] != -1 and hierarchy[0][i][3] != -1:
                    parent_idx = hierarchy[0][i][3]
                    parent_contour = contours[parent_idx]
                    child_idx = hierarchy[0][i][2]
                    child_contour = contours[child_idx]

                    self.draw_analysis(output_image, contour, parent_contour, child_contour)

        return output_image

    def draw_analysis(self, output_image, contour, parent_contour, child_contour):
        """
        Draw contours and measurements on the image.

        Parameters:
        - output_image: numpy.ndarray, image to draw on.
        - contour: numpy.ndarray, main contour.
        - parent_contour: numpy.ndarray, parent contour.
        - child_contour: numpy.ndarray, child contour.
        """
        cv2.drawContours(output_image, [contour], -1, (0, 255, 0), 1)  # Green
        cv2.drawContours(output_image, [parent_contour], -1, (0, 0, 255), 1)  # Red
        cv2.drawContours(output_image, [child_contour], -1, (255, 255, 0), 1)  # Blue

    def release(self):
        """Release the camera resources."""
        self.picam2.close()

# Example usage in a separate file:
# from image_analyzer import ImageAnalyzer
# analyzer = ImageAnalyzer(exposure=500, low_hsv=(0, 100, 100), high_hsv=(180, 255, 255))
# while True:
#     frame = analyzer.analyze_frame()
#     cv2.imshow("Analysis", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# analyzer.release()
# cv2.destroyAllWindows()
