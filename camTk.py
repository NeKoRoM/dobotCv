import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
import time
from save import CameraSettings
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CameraProcessor:
    def __init__(self, root):
        self.root = root
        self.picam2 = None
        self.image = None
        self.output_image = None
        self.prev_focus = 5
        self.prev_exposure = 100
        self.prev_time = time.time()
        self.image_label = None
        self.output_image_label = None

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Camera Interface")

        self.camera_frame = ttk.LabelFrame(self.root, text="Camera")
        self.camera_frame.grid(row=0, column=0, padx=10, pady=10)

        self.camera1_frame = ttk.LabelFrame(self.root, text="Camera1")
        self.camera1_frame.grid(row=0, column=1, padx=10, pady=10)

        self.focus_scale = ttk.Scale(self.camera_frame, from_=0, to=25, orient=tk.HORIZONTAL, command=self._on_trackbar)
        self.focus_scale.set(self.prev_focus)
        self.focus_scale.grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.camera_frame, text="Focus").grid(row=0, column=1, padx=5, pady=5)

        self.exposure_scale = ttk.Scale(self.camera_frame, from_=0, to=100000, orient=tk.HORIZONTAL, command=self._on_trackbar_exp)
        self.exposure_scale.set(self.prev_exposure)
        self.exposure_scale.grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.camera_frame, text="Exposure").grid(row=1, column=1, padx=5, pady=5)

        self.lov_h_scale = ttk.Scale(self.camera1_frame, from_=0, to=180, orient=tk.HORIZONTAL, command=self._on_trackbar_lovH)
        self.lov_h_scale.grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.camera1_frame, text="Low H").grid(row=0, column=1, padx=5, pady=5)

        self.lov_s_scale = ttk.Scale(self.camera1_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self._on_trackbar_lovS)
        self.lov_s_scale.grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.camera1_frame, text="Low S").grid(row=1, column=1, padx=5, pady=5)

        self.lov_v_scale = ttk.Scale(self.camera1_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self._on_trackbar_lovV)
        self.lov_v_scale.grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(self.camera1_frame, text="Low V").grid(row=2, column=1, padx=5, pady=5)

        self.high_h_scale = ttk.Scale(self.camera1_frame, from_=0, to=180, orient=tk.HORIZONTAL, command=self._on_trackbar_highH)
        self.high_h_scale.grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(self.camera1_frame, text="High H").grid(row=3, column=1, padx=5, pady=5)

        self.high_s_scale = ttk.Scale(self.camera1_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self._on_trackbar_highS)
        self.high_s_scale.grid(row=4, column=0, padx=5, pady=5)
        ttk.Label(self.camera1_frame, text="High S").grid(row=4, column=1, padx=5, pady=5)

        self.high_v_scale = ttk.Scale(self.camera1_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self._on_trackbar_highV)
        self.high_v_scale.grid(row=5, column=0, padx=5, pady=5)
        ttk.Label(self.camera1_frame, text="High V").grid(row=5, column=1, padx=5, pady=5)

        self.image_label = ttk.Label(self.camera1_frame)
        self.image_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.output_image_label = ttk.Label(self.camera_frame)
        self.output_image_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.start_button = ttk.Button(self.root, text="Start Camera", command=self.start_camera)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop Camera", command=self.close_camera)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)

    def close_camera(self):
        if self.picam2:
            self.picam2.close()
        cv2.destroyAllWindows()

    def start_camera(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        self.picam2.start()
        time.sleep(2)
        self.run()

    def get_settings(self):
        hsv_lower = [
            self.lov_h_scale.get(),
            self.lov_s_scale.get(),
            self.lov_v_scale.get()
        ]
        hsv_upper = [
            self.high_h_scale.get(),
            self.high_s_scale.get(),
            self.high_v_scale.get()
        ]

        params = CameraSettings(
            name="Camera1",
            exposure=self.exposure_scale.get(),
            focus=self.focus_scale.get(),
            hsv_lower=hsv_lower,
            hsv_upper=hsv_upper
        )
        return params

    def set_settings(self, camera_settings):
        self.focus_scale.set(camera_settings.focus)
        self.exposure_scale.set(camera_settings.exposure)
        self.lov_h_scale.set(camera_settings.hsv_lower[0])
        self.lov_s_scale.set(camera_settings.hsv_lower[1])
        self.lov_v_scale.set(camera_settings.hsv_lower[2])
        self.high_h_scale.set(camera_settings.hsv_upper[0])
        self.high_s_scale.set(camera_settings.hsv_upper[1])
        self.high_v_scale.set(camera_settings.hsv_upper[2])

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

    def update_image_label(self, image, label):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image)
        label.config(image=image_tk)
        label.image = image_tk

    def process_frame(self):
        im = self.picam2.capture_array()

        low_black = np.array([
            self.lov_h_scale.get(),
            self.lov_s_scale.get(),
            self.lov_v_scale.get()
        ], np.uint8)

        high_black = np.array([
            self.high_h_scale.get(),
            self.high_s_scale.get(),
            self.high_v_scale.get()
        ], np.uint8)

        img_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        self.image = cv2.inRange(img_hsv, low_black, high_black)

        _, binary = cv2.threshold(self.image, 200, 255, cv2.THRESH_BINARY)
        binary = cv2.bitwise_not(binary)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.output_image = im

        min_area = 1000

        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area < min_area:
                continue

            if hierarchy[0][i][2] != -1 and hierarchy[0][i][3] != -1:
                parent_idx = hierarchy[0][i][3]
                parent_contour = contours[parent_idx]

                previosly_child_idx = hierarchy[0][i][2]  # first child
                next_child = hierarchy[0][previosly_child_idx][0]  # second child
                bigest_child_idx = previosly_child_idx

                while hierarchy[0][previosly_child_idx][0] != -1:
                    if cv2.contourArea(contours[bigest_child_idx]) <= cv2.contourArea(contours[next_child]):
                        bigest_child_idx = next_child
                    previosly_child_idx = hierarchy[0][next_child][0]
                    next_child = hierarchy[0][previosly_child_idx][0]

                child_contour = contours[bigest_child_idx]

                self.findPt(contour, parent_contour, self.output_image, (255, 255, 0))
                self.findPt(child_contour, contour, self.output_image, (255, 0, 255))

                cv2.drawContours(self.output_image, [contour], -1, (0, 255, 0), 1)
                cv2.drawContours(self.output_image, [child_contour], -1, (255, 255, 0), 1)
                cv2.drawContours(self.output_image, [parent_contour], -1, (0, 0, 255), 1)

        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        cv2.putText(self.output_image, f"{fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        self.update_image_label(self.image, self.image_label)
        self.update_image_label(self.output_image, self.output_image_label)

    def run(self):
        self.process_frame()

        focus_track = self.focus_scale.get()
        if focus_track != self.prev_focus:
            self.prev_focus = focus_track
            self.picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": focus_track})

        exp_track = self.exposure_scale.get()
        if exp_track != self.prev_exposure:
            self.prev_exposure = exp_track
            self.picam2.set_controls({"ExposureTime": exp_track * 10})

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.close_camera()
        else:
            self.root.after(10, self.run)

if __name__ == "__main__":
    root = tk.Tk()
    processor = CameraProcessor(root)
    root.mainloop()