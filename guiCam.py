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
