import tkinter as tk
from tkinter import ttk
import cv2
from cam import ImageAnalyzer
import guiCam
import threading
import json

class AnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Analyzer")

        # Initialize analyzer
        self.analyzer = ImageAnalyzer()

        # Variables for sliders
        self.exposure_var = tk.IntVar(value=100)
        self.focus_var = tk.IntVar(value=10)
        self.low_h_var = tk.IntVar(value=0)
        self.low_s_var = tk.IntVar(value=0)
        self.low_v_var = tk.IntVar(value=0)
        self.high_h_var = tk.IntVar(value=180)
        self.high_s_var = tk.IntVar(value=255)
        self.high_v_var = tk.IntVar(value=255)

        # Create UI components
        guiCam.create_widgets(self)

        # Start analysis thread
        self.running = True
        self.analysis_thread = threading.Thread(target=self.run_analysis)
        self.analysis_thread.start()


    def update_exposure(self):
        """Update exposure based on the entry value."""
        self.analyzer.set_exposure(self.exposure_var.get())

    def update_focus(self):
        """Update focus based on the entry value."""
        self.analyzer.set_focus(self.focus_var.get())

    def update_hsv(self):
        """Update HSV thresholds based on the entry values."""
        low_hsv = (self.low_h_var.get(), self.low_s_var.get(), self.low_v_var.get())
        high_hsv = (self.high_h_var.get(), self.high_s_var.get(), self.high_v_var.get())
        self.analyzer.set_hsv_thresholds(low_hsv, high_hsv)

    def save_params(self):
        """Save current parameters to a file."""
        params = {
            "exposure": self.exposure_var.get(),
            "focus": self.focus_var.get(),
            "low_hsv": (self.low_h_var.get(), self.low_s_var.get(), self.low_v_var.get()),
            "high_hsv": (self.high_h_var.get(), self.high_s_var.get(), self.high_v_var.get())
        }
        with open("params.json", "w") as f:
            json.dump(params, f)
        print("Parameters saved.")

    def load_params(self):
        """Load parameters from a file."""
        try:
            with open("params.json", "r") as f:
                params = json.load(f)
            self.exposure_var.set(params["exposure"])
            self.focus_var.set(params["focus"])
            self.low_h_var.set(params["low_hsv"][0])
            self.low_s_var.set(params["low_hsv"][1])
            self.low_v_var.set(params["low_hsv"][2])
            self.high_h_var.set(params["high_hsv"][0])
            self.high_s_var.set(params["high_hsv"][1])
            self.high_v_var.set(params["high_hsv"][2])
            print("Parameters loaded.")
        except FileNotFoundError:
            print("No parameters file found.")

    def clear_params(self):
        """Clear all parameter fields."""
        self.exposure_var.set(100)
        self.focus_var.set(10)
        self.low_h_var.set(0)
        self.low_s_var.set(0)
        self.low_v_var.set(0)
        self.high_h_var.set(180)
        self.high_s_var.set(255)
        self.high_v_var.set(255)
        print("Parameters cleared.")

    def open_analysis(self):
        """Open the analysis window."""
        if not self.running:
            self.running = True
            self.analysis_thread = threading.Thread(target=self.run_analysis)
            self.analysis_thread.start()

    def run_analysis(self):
        """Run the analysis in a loop and display results in a separate window."""
        while self.running:
            frame = self.analyzer.analyze_frame()
            cv2.imshow("Analysis", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

    def stop(self):
        """Stop the analysis and release resources."""
        self.running = False
        self.analyzer.release()
        cv2.destroyAllWindows()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyzerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.stop)
    root.mainloop()
