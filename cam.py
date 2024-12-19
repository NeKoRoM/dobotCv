import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
import time
from save import CameraSettings

class CameraProcessor:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        self.picam2.start()
        time.sleep(2)

        cv2.namedWindow("Camera")
        cv2.namedWindow("Camera1")
        
        self.prev_focus = cv2.getTrackbarPos("focus", "Camera") if cv2.getTrackbarPos("focus", "Camera") != -1 else 5
        self.prev_exposure = cv2.getTrackbarPos("exposure", "Camera") if cv2.getTrackbarPos("exposure", "Camera") != -1 else 100
        self.prev_time = time.time()


        self._setup_trackbars()

    def get_settings(self):
        """
        Отримання поточних параметрів камери з повзунків.

        :return: Об'єкт CameraSettings із поточними значеннями параметрів камери.
        """
        hsv_lower = [
            cv2.getTrackbarPos("lov_h", "Camera1"),
            cv2.getTrackbarPos("lov_s", "Camera1"),
            cv2.getTrackbarPos("lov_v", "Camera1")
        ]
        hsv_upper = [
            cv2.getTrackbarPos("high_h", "Camera1"),
            cv2.getTrackbarPos("high_s", "Camera1"),
            cv2.getTrackbarPos("high_v", "Camera1")
        ]

        params = CameraSettings(
            name="Camera1",
            exposure=cv2.getTrackbarPos("exposure", "Camera"),
            focus=cv2.getTrackbarPos("focus", "Camera"),
            hsv_lower=hsv_lower,
            hsv_upper=hsv_upper
        )
        return params

    def set_settings(camera_settings):
        """
        Встановлення параметрів камери за допомогою повзунків.

        :param camera_settings: Об'єкт CameraSettings із новими значеннями параметрів.
        """
        cv2.setTrackbarPos("focus", "Camera", camera_settings.focus)
        cv2.setTrackbarPos("exposure", "Camera", camera_settings.exposure)

        cv2.setTrackbarPos("lov_h", "Camera1", camera_settings.hsv_lower[0])
        cv2.setTrackbarPos("lov_s", "Camera1", camera_settings.hsv_lower[1])
        cv2.setTrackbarPos("lov_v", "Camera1", camera_settings.hsv_lower[2])

        cv2.setTrackbarPos("high_h", "Camera1", camera_settings.hsv_upper[0])
        cv2.setTrackbarPos("high_s", "Camera1", camera_settings.hsv_upper[1])
        cv2.setTrackbarPos("high_v", "Camera1", camera_settings.hsv_upper[2])

        
    def _setup_trackbars(self):
        cv2.createTrackbar("focus", "Camera", 5, 25, self._on_trackbar)
        cv2.createTrackbar("exposure", "Camera", 100, 100000, self._on_trackbar_exp)

        cv2.createTrackbar("lov_h", "Camera1", 0, 180, self._on_trackbar_lovH)
        cv2.createTrackbar("lov_s", "Camera1", 0, 255, self._on_trackbar_lovS)
        cv2.createTrackbar("lov_v", "Camera1", 0, 255, self._on_trackbar_lovV)
        cv2.createTrackbar("high_h", "Camera1", 180, 180, self._on_trackbar_highH)
        cv2.createTrackbar("high_s", "Camera1", 255, 255, self._on_trackbar_highS)
        cv2.createTrackbar("high_v", "Camera1", 55, 255, self._on_trackbar_highV)

    @staticmethod
    def _on_trackbar(val):
        pass

    @staticmethod
    def _on_trackbar_exp(val):
        pass

    @staticmethod
    def _on_trackbar_lovH(val):
        pass

    @staticmethod
    def _on_trackbar_lovS(val):
        pass

    @staticmethod
    def _on_trackbar_lovV(val):
        pass

    @staticmethod
    def _on_trackbar_highH(val):
        pass

    @staticmethod
    def _on_trackbar_highS(val):
        pass

    @staticmethod
    def _on_trackbar_highV(val):
        pass

    @staticmethod
    def findPt(contour_main, parent_contour_second, output_image, color=(0, 255, 255)):
        x, y = contour_main[0][0]
        x_parent, y_parent = parent_contour_second[0][0]

        xL, yL = contour_main[0][0]
        x_parentL, y_parentL = parent_contour_second[0][0]

        for pt in contour_main:
            if pt[0][0] > x:
                x, y = pt[0]
            if pt[0][0] < xL:
                xL, yL = pt[0]

        for pt in parent_contour_second:
            if pt[0][0] > x_parent:
                x_parent, y_parent = pt[0]
            if pt[0][0] < x_parentL:
                x_parentL, y_parentL = pt[0]

        cv2.line(output_image, (x, y), (x_parent, y_parent), color, 1)
        cv2.putText(output_image, f"Left width: {x_parentL - xL}px", (xL, yL - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(output_image, (xL, yL), (x_parentL, y_parentL), color, 1)
        cv2.putText(output_image, f"Right width: {x_parent - x}px", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    def process_frame(self):
        im = self.picam2.capture_array()

        low_black = np.array([
            cv2.getTrackbarPos("lov_h", "Camera1"),
            cv2.getTrackbarPos("lov_s", "Camera1"),
            cv2.getTrackbarPos("lov_v", "Camera1")], np.uint8)

        high_black = np.array([
            cv2.getTrackbarPos("high_h", "Camera1"),
            cv2.getTrackbarPos("high_s", "Camera1"),
            cv2.getTrackbarPos("high_v", "Camera1")], np.uint8)

        img_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        image = cv2.inRange(img_hsv, low_black, high_black)

        _, binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
        binary = cv2.bitwise_not(binary)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        output_image = im

        min_area = 1000

        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area < min_area:
                continue

            if hierarchy[0][i][2] != -1 and hierarchy[0][i][3] != -1:
                parent_idx = hierarchy[0][i][3]
                parent_contour = contours[parent_idx]

                previosly_child_idx = hierarchy[0][i][2] # first child
                next_child =  hierarchy[0][previosly_child_idx][0] # second child
                bigest_child_idx = previosly_child_idx

                while hierarchy[0][previosly_child_idx][0] != -1:
                    if cv2.contourArea(contours(bigest_child_idx)) <= cv2.contourArea(contours(next_child)):
                        bigest_child_idx = next_child
                    previosly_child_idx = hierarchy[0][next_child][0]
                    next_child = hierarchy[0][previosly_child_idx][0]
                    
                        


                child_contour = contours[bigest_child_idx]

                self.findPt(contour, parent_contour, output_image, (255, 255, 0))
                self.findPt(child_contour, contour, output_image, (255, 0, 255))

                cv2.drawContours(output_image, [contour], -1, (0, 255, 0), 1)
                cv2.drawContours(output_image, [child_contour], -1, (255, 255, 0), 1)
                cv2.drawContours(output_image, [parent_contour], -1, (0, 0, 255), 1)

        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        cv2.putText(output_image, f"{fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Camera1", image)
        cv2.imshow("Camera", output_image)

    def run(self, continue_flag):
        while continue_flag[0]:
            self.process_frame()

            focus_track = cv2.getTrackbarPos("focus", "Camera")
            if focus_track != self.prev_focus:
                self.prev_focus = focus_track
                self.picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": focus_track})

            exp_track = cv2.getTrackbarPos("exposure", "Camera")
            if exp_track != self.prev_exposure:
                self.prev_exposure = exp_track
                self.picam2.set_controls({"ExposureTime": exp_track * 10})

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.picam2.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    processor = CameraProcessor()
    processor.run()
