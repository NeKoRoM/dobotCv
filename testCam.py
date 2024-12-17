from cam import ImageAnalyzer
import tkinter as tk
from tkinter import ttk
import cv2
import threading

class AnalyzerGUI:
    def __init__(self, root):
        """
        Initialize the GUI for controlling the ImageAnalyzer.

        Parameters:
        - root: tk.Tk, the main tkinter root object.
        """
        self.root = root
        self.root.title("Image Analyzer")

        # Initialize analyzer
        self.analyzer = ImageAnalyzer()

        # Variables for sliders
        self.exposure_var = tk.IntVar(value=100)
        self.low_h_var = tk.IntVar(value=0)
        self.low_s_var = tk.IntVar(value=0)
        self.low_v_var = tk.IntVar(value=0)
        self.high_h_var = tk.IntVar(value=180)
        self.high_s_var = tk.IntVar(value=255)
        self.high_v_var = tk.IntVar(value=255)

        # Create UI components
        self.create_widgets()

        # Start analysis thread
        self.running = True
        self.analysis_thread = threading.Thread(target=self.run_analysis)
        self.analysis_thread.start()

    def create_widgets(self):
        """Create GUI components."""
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Exposure slider
        ttk.Label(frame, text="Exposure").grid(row=0, column=0, sticky="w")
        exposure_slider = ttk.Scale(frame, from_=10, to=1000, orient="horizontal", variable=self.exposure_var, command=self.update_exposure)
        exposure_slider.grid(row=0, column=1, padx=5, pady=5)

        # HSV sliders
        ttk.Label(frame, text="Low H").grid(row=1, column=0, sticky="w")
        ttk.Scale(frame, from_=0, to=180, orient="horizontal", variable=self.low_h_var, command=self.update_hsv).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Low S").grid(row=2, column=0, sticky="w")
        ttk.Scale(frame, from_=0, to=255, orient="horizontal", variable=self.low_s_var, command=self.update_hsv).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Low V").grid(row=3, column=0, sticky="w")
        ttk.Scale(frame, from_=0, to=255, orient="horizontal", variable=self.low_v_var, command=self.update_hsv).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="High H").grid(row=4, column=0, sticky="w")
        ttk.Scale(frame, from_=0, to=180, orient="horizontal", variable=self.high_h_var, command=self.update_hsv).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(frame, text="High S").grid(row=5, column=0, sticky="w")
        ttk.Scale(frame, from_=0, to=255, orient="horizontal", variable=self.high_s_var, command=self.update_hsv).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="High V").grid(row=6, column=0, sticky="w")
        ttk.Scale(frame, from_=0, to=255, orient="horizontal", variable=self.high_v_var, command=self.update_hsv).grid(row=6, column=1, padx=5, pady=5)

    def update_exposure(self, _):
        """Update exposure based on the slider value."""
        self.analyzer.set_exposure(self.exposure_var.get())

    def update_hsv(self, _):
        """Update HSV thresholds based on the slider values."""
        low_hsv = (self.low_h_var.get(), self.low_s_var.get(), self.low_v_var.get())
        high_hsv = (self.high_h_var.get(), self.high_s_var.get(), self.high_v_var.get())
        self.analyzer.set_hsv_thresholds(low_hsv, high_hsv)

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
