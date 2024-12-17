import tkinter as tk
from tkinter import ttk
import cv2
from image_analyzer import ImageAnalyzer
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
        self.create_widgets()

        # Start analysis thread
        self.running = True
        self.analysis_thread = threading.Thread(target=self.run_analysis)
        self.analysis_thread.start()

    def create_widgets(self):
        """Create GUI components."""
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Exposure
        ttk.Label(frame, text="Exposure").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.exposure_var, width=5).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Update", command=self.update_exposure).grid(row=0, column=2, padx=5, pady=5)

        # Focus
        ttk.Label(frame, text="Focus").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.focus_var, width=5).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Update", command=self.update_focus).grid(row=1, column=2, padx=5, pady=5)

        # HSV sliders with text entries
        ttk.Label(frame, text="Low H").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.low_h_var, width=5).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Low S").grid(row=3, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.low_s_var, width=5).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Low V").grid(row=4, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.low_v_var, width=5).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(frame, text="High H").grid(row=5, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.high_h_var, width=5).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="High S").grid(row=6, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.high_s_var, width=5).grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(frame, text="High V").grid(row=7, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.high_v_var, width=5).grid(row=7, column=1, padx=5, pady=5)

        # Update HSV button
        ttk.Button(frame, text="Update HSV", command=self.update_hsv).grid(row=8, column=0, columnspan=2, pady=5)

        # Parameter management buttons
        ttk.Button(frame, text="Save Params", command=self.save_params).grid(row=9, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Load Params", command=self.load_params).grid(row=9, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Clear Params", command=self.clear_params).grid(row=9, column=2, padx=5, pady=5)

        # Open/Close buttons
        ttk.Button(frame, text="Open Analysis", command=self.open_analysis).grid(row=10, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Close Analysis", command=self.stop).grid(row=10, column=1, padx=5, pady=5)

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
