import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import time
def fifo_algorithm(pages, frames):
    memory = []
    page_faults = 0
    steps = []
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        steps.append(memory.copy())
    return page_faults, steps
def lru_algorithm(pages, frames):
    memory = []
    page_faults = 0
    steps = []
    recent_usage = []
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
                recent_usage.append(page)
            else:
                lru_page = recent_usage.pop(0)
                memory.remove(lru_page)
                memory.append(page)
                recent_usage.append(page)
            page_faults += 1
        else:
            recent_usage.remove(page)
            recent_usage.append(page)
        steps.append(memory.copy())
    return page_faults, steps

def optimal_algorithm(pages, frames):
    memory = []
    page_faults = 0
    steps = []
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future = pages[i+1:]
                index_dict = {}
                for mem_page in memory:
                    if mem_page in future:
                        index_dict[mem_page] = future.index(mem_page)
                    else:
                        index_dict[mem_page] = float('inf')
                page_to_replace = max(index_dict, key=index_dict.get)
                memory[memory.index(page_to_replace)] = page
            page_faults += 1
        steps.append(memory.copy())
    return page_faults, steps
class PageReplacementSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Page Replacement Simulator")
        self.root.geometry("1000x700")
        self.current_theme = "dark"
        self.set_theme_colors()
        self.create_menu()
        self.create_widgets()
        self.create_treeview()
        self.create_chart_area()

    def set_theme_colors(self):
        if self.current_theme == "dark":
            self.bg_color = "#2C3E50"
            self.fg_color = "#ECF0F1"
            self.entry_bg = "#34495E"
            self.btn_bg = "#3498DB"
            self.btn_fg = "white"
        else:
            self.bg_color = "#ECF0F1"
            self.fg_color = "#2C3E50"
            self.entry_bg = "white"
            self.btn_bg = "#2980B9"
            self.btn_fg = "white"
        self.root.configure(bg=self.bg_color)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Manual", command=self.show_manual)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Ultimate Page Replacement Simulator\nDeveloped to stand out!"))
        menubar.add_cascade(label="Help", menu=help_menu)

        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Toggle Dark/Light Mode", command=self.toggle_theme)
        menubar.add_cascade(label="Theme", menu=theme_menu)

    def create_widgets(self):
        input_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        input_frame.pack(fill=tk.X)

        # Pages input
        tk.Label(input_frame, text="Pages (space-separated):", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.pages_entry = tk.Entry(input_frame, width=40, font=("Arial", 12), bg=self.entry_bg, fg=self.fg_color)
        self.pages_entry.grid(row=0, column=1, padx=10, pady=5)
        self.pages_entry.insert(0, "7 0 1 2 0 3 4 2 3 0 3 2")

        # Frames input
        tk.Label(input_frame, text="Frames:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.frames_entry = tk.Entry(input_frame, width=5, font=("Arial", 12), bg=self.entry_bg, fg=self.fg_color)
        self.frames_entry.grid(row=0, column=3, padx=10, pady=5)
        self.frames_entry.insert(0, "3")

        # Algorithm dropdown
        tk.Label(input_frame, text="Algorithm:", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.algorithm_choice = ttk.Combobox(input_frame, values=["FIFO", "LRU", "Optimal"], state="readonly", font=("Arial", 12))
        self.algorithm_choice.grid(row=0, column=5, padx=10, pady=5)
        self.algorithm_choice.current(0)

        # Simulate Button
        self.simulate_btn = tk.Button(input_frame, text="Simulate", font=("Arial", 12, "bold"), bg=self.btn_bg, fg=self.btn_fg, command=self.simulate)
        self.simulate_btn.grid(row=0, column=6, padx=10, pady=5)

        # Export Button
        self.export_btn = tk.Button(input_frame, text="Export CSV", font=("Arial", 12, "bold"), bg="#27AE60", fg="white", command=self.export_csv)
        self.export_btn.grid(row=0, column=7, padx=10, pady=5)

        # Total faults label
        self.faults_label = tk.Label(self.root, text="Total Page Faults: 0", bg=self.bg_color, fg=self.fg_color, font=("Arial", 14, "bold"))
        self.faults_label.pack(pady=10)

    def create_treeview(self):
        # Frame for simulation steps table
        table_frame = tk.Frame(self.root, bg=self.bg_color)
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("Step", "Memory Frames"), show="headings", height=8)
        self.tree.heading("Step", text="Step")
        self.tree.heading("Memory Frames", text="Memory Frames")
        self.tree.column("Step", width=80, anchor="center")
        self.tree.column("Memory Frames", width=400, anchor="w")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_chart_area(self):
        # Frame for matplotlib chart
        chart_frame = tk.Frame(self.root, bg=self.bg_color)
        chart_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 3), facecolor=self.bg_color)
        self.ax.set_title("Page Faults", color=self.fg_color)
        self.ax.set_ylabel("Faults", color=self.fg_color)
        self.ax.set_facecolor(self.entry_bg)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def simulate(self):
        try:
            pages = list(map(int, self.pages_entry.get().split()))
            frames = int(self.frames_entry.get())
            algorithm = self.algorithm_choice.get()

            if frames <= 0 or not pages:
                raise ValueError("Invalid input!")

            if algorithm == "FIFO":
                faults, steps = fifo_algorithm(pages, frames)
            elif algorithm == "LRU":
                faults, steps = lru_algorithm(pages, frames)
            elif algorithm == "Optimal":
                faults, steps = optimal_algorithm(pages, frames)
            else:
                raise ValueError("Algorithm not implemented!")

            self.faults_label.config(text=f"Total Page Faults: {faults}")
            self.populate_table(steps)
            self.update_chart(faults)

            # Animate step-by-step execution (optional: can be toggled or slowed down)
            self.animate_steps(steps)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def populate_table(self, steps):
        # Clear previous rows
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Insert new simulation steps
        for i, mem in enumerate(steps):
            self.tree.insert("", "end", values=(i+1, "  ".join(map(str, mem))))

    def update_chart(self, faults):
        self.ax.clear()
        self.ax.bar(["Page Faults"], [faults], color="#E74C3C")
        self.ax.set_title("Page Faults", color=self.fg_color)
        self.ax.set_ylabel("Faults", color=self.fg_color)
        self.ax.set_facecolor(self.entry_bg)
        self.canvas.draw()

    def animate_steps(self, steps):
        # Optional: animate steps in the Treeview (highlight each row briefly)
        for item in self.tree.get_children():
            self.tree.item(item, tags=("normal",))
        self.tree.tag_configure("highlight", background="#F1C40F")
        for item in self.tree.get_children():
            self.tree.item(item, tags=("highlight",))
            self.root.update_idletasks()
            time.sleep(0.3)
            self.tree.item(item, tags=("normal",))
        # End of animation

    def export_csv(self):
        # Export the simulation steps to a CSV file using pandas
        rows = []
        for child in self.tree.get_children():
            step, memory = self.tree.item(child)["values"]
            rows.append({"Step": step, "Memory Frames": memory})
        df = pd.DataFrame(rows)
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export", "Simulation steps exported successfully!")

    def toggle_theme(self):
        # Toggle between dark and light mode
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme_colors()
        # Update widget colors
        self.root.configure(bg=self.bg_color)
        self.faults_label.config(bg=self.bg_color, fg=self.fg_color)
        # Update input frame colors (for simplicity, recreate UI elements or update individually)
        # (In a real app, you would loop through and update each widget's colors)
        messagebox.showinfo("Theme", f"Switched to {self.current_theme} mode. Restart the app to see full effect.")

    def show_manual(self):
        manual_text = (
            "Ultimate Page Replacement Simulator - User Manual:\n\n"
            "1. Enter the page reference string (space-separated numbers).\n"
            "2. Enter the number of available frames.\n"
            "3. Choose an algorithm (FIFO, LRU, Optimal).\n"
            "4. Click 'Simulate' to run the simulation.\n"
            "5. View the simulation steps in the table below.\n"
            "6. See the page fault analysis in the graph area.\n"
            "7. Use 'Export CSV' to save simulation steps for later analysis.\n"
            "8. Toggle Dark/Light Mode from the Theme menu.\n"
        )
        messagebox.showinfo("User Manual", manual_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementSimulatorApp(root)
    root.mainloop()
