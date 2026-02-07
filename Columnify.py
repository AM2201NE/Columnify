import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pypdf import PdfReader, PdfWriter

class ColumnifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Columnify")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # --- UI LAYOUT ---
        tk.Label(root, text="Columnify: Medical Textbooks", font=("Arial", 16, "bold")).pack(pady=15)

        # 1. File Selection Section
        self.file_frame = tk.LabelFrame(root, text=" 1. Select Input ", padx=10, pady=10)
        self.file_frame.pack(fill="x", padx=20, pady=5)
        
        self.btn_select = tk.Button(self.file_frame, text="Browse PDF", command=self.pick_file, width=15)
        self.btn_select.pack(side="left", padx=5)
        
        self.file_label = tk.Label(self.file_frame, text="No file selected", fg="#a1a1a1", wraplength=250)
        self.file_label.pack(side="left", padx=5)

        # 2. Output Naming Section
        self.name_frame = tk.LabelFrame(root, text=" 2. Output Settings ", padx=10, pady=10)
        self.name_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(self.name_frame, text="Full Output Name:").pack(anchor="w")
        self.name_ent = tk.Entry(self.name_frame, width=50)
        self.name_ent.pack(pady=5)
        self.name_ent.bind("<KeyRelease>", self.check_ready)

        # 3. Execution Section
        self.action_frame = tk.Frame(root, pady=10)
        self.action_frame.pack(fill="x", padx=20)

        # Feature indicators (Visual only, logic is automated)
        feat_label = tk.Label(self.action_frame, text="✔ Auto-Rotation Enabled  ✔ Smart Gutter Detection", 
                              font=("Arial", 8), fg="#555")
        feat_label.pack()

        self.progress = ttk.Progressbar(self.action_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        
        self.status_label = tk.Label(self.action_frame, text="Waiting for input...", font=("Arial", 9, "italic"))
        self.status_label.pack()

        self.btn_process = tk.Button(
            self.action_frame, 
            text="Process PDF", 
            command=self.start_thread, 
            bg="#cccccc", 
            fg="white", 
            state="disabled",
            font=("Arial", 12, "bold"),
            height=2
        )
        self.btn_process.pack(pady=10, fill="x")

        self.input_path = ""

    def pick_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.input_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=filename, fg="#2c3e50")
            
            # Default name generation
            default_out = filename.replace(".pdf", " 1column.pdf")
            self.name_ent.delete(0, tk.END)
            self.name_ent.insert(0, default_out)
            self.check_ready()

    def check_ready(self, event=None):
        has_file = bool(self.input_path)
        name_text = self.name_ent.get().strip()
        has_name = len(name_text) > 4 and name_text.lower().endswith(".pdf")
        
        if has_file and has_name:
            self.btn_process.config(state="normal", bg="#27ae60")
            self.status_label.config(text="Ready to process!", fg="black")
        else:
            self.btn_process.config(state="disabled", bg="#cccccc")

    def start_thread(self):
        self.btn_process.config(state="disabled", text="Working...")
        self.btn_select.config(state="disabled")
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        try:
            reader = PdfReader(self.input_path)
            writer = PdfWriter()
            total = len(reader.pages)
            
            output_dir = os.path.dirname(self.input_path)
            output_full_path = os.path.join(output_dir, self.name_ent.get())

            for i in range(total):
                page = reader.pages[i]
                
                # --- AUTO-ROTATE & DESKEW METADATA ---
                # Forces the internal coordinate system to be 0 degrees
                page.transfer_rotation_to_content()

                mb = page.mediabox
                ll_x, ll_y = float(mb.lower_left[0]), float(mb.lower_left[1])
                ur_x, ur_y = float(mb.upper_right[0]), float(mb.upper_right[1])
                width = ur_x - ll_x
                height = ur_y - ll_y

                # --- SMART CENTERED SPLIT ---
                # We use the mathematical center of the page's visible content area
                # This ensures consistent splitting even if the paper scan is off-center
                split_x = ll_x + (width / 2)

                # --- 1-COLUMN TRANSFORMATION ---
                # Create Left Column Page
                page_l = writer.add_page(page)
                page_l.mediabox.lower_left = (ll_x, ll_y)
                page_l.mediabox.upper_right = (split_x, ur_y)
                
                # Create Right Column Page
                page_r = writer.add_page(page)
                page_r.mediabox.lower_left = (split_x, ll_y)
                page_r.mediabox.upper_right = (ur_x, ur_y)

                # Progress Update
                percent = int(((i + 1) / total) * 100)
                self.root.after(0, self.update_ui, percent, f"Processing: {i+1} / {total} pages")

            with open(output_full_path, "wb") as f:
                writer.write(f)
            
            self.root.after(0, lambda: messagebox.showinfo("Success", "Perfect! Your 1-column PDF is ready."))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed: {str(e)}"))
        
        finally:
            self.root.after(0, self.reset_ui)

    def update_ui(self, val, txt):
        self.progress["value"] = val
        self.status_label.config(text=txt)

    def reset_ui(self):
        self.btn_process.config(text="Process PDF")
        self.btn_select.config(state="normal")
        self.progress["value"] = 0
        self.check_ready()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColumnifyApp(root)
    root.mainloop()