import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import threading
from etc.ext import EXTENSIONS_MAP

class FileForgeOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileForge - Modular File Organizer 📁⚡")
        self.root.geometry("700x520")
        self.root.minsize(650, 480)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    def create_widgets(self):
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill="x", padx=10, pady=5)

        title_lbl = ttk.Label(header_frame, text="FileForge: Modular File Organization Utility", font=("Arial", 12, "bold"))
        title_lbl.pack(anchor="w")
        sub_lbl = ttk.Label(header_frame, text="Organizing files cleanly using separate extension modules (etc/ext.py).", font=("Arial", 9))
        sub_lbl.pack(anchor="w", pady=(2, 0))

        dir_frame = ttk.LabelFrame(self.root, text=" Target Directory ", padding=10)
        dir_frame.pack(fill="x", padx=10, pady=5)

        self.entry_dir = ttk.Entry(dir_frame, font=("Arial", 10))
        self.entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_browse = ttk.Button(dir_frame, text="📁 Browse Folder", command=self.browse_directory)
        self.btn_browse.pack(side="right")

        config_frame = ttk.LabelFrame(self.root, text=" Organization Options ", padding=10)
        config_frame.pack(fill="x", padx=10, pady=5)

        self.var_lowercase = tk.BooleanVar(value=False)
        chk_lowercase = ttk.Checkbutton(config_frame, text="Normalize filenames to lowercase", variable=self.var_lowercase)
        chk_lowercase.pack(anchor="w", pady=2)

        action_frame = ttk.Frame(self.root, padding=10)
        action_frame.pack(fill="x", padx=10, pady=5)

        self.btn_organize = ttk.Button(action_frame, text="🚀 Start Organizing Files", command=self.start_organizing)
        self.btn_organize.pack(side="right", padx=5)

        self.btn_clear = ttk.Button(action_frame, text="Clear Logs", command=lambda: self.log_text.delete(1.0, tk.END))
        self.btn_clear.pack(side="left", padx=5)

        log_frame = ttk.LabelFrame(self.root, text=" Execution Output & History ", padding=8)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4", height=10)
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def browse_directory(self):
        dir_path = filedialog.askdirectory(title="Pilih Folder yang Mau Dirapikan")
        if dir_path:
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, dir_path)
            self.log(f"[INFO] Target folder dipilih: {dir_path}\n")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_organizing(self):
        target_dir = self.entry_dir.get().strip()
        if not target_dir:
            messagebox.showwarning("Warning", "Pilih folder tujuan terlebih dahulu!")
            return
        if not os.path.exists(target_dir):
            messagebox.showerror("Error", "Direktori yang dipilih tidak ditemukan!")
            return

        threading.Thread(target=self.organize_files_worker, args=(target_dir,), daemon=True).start()

    def organize_files_worker(self, target_dir):
        self.log(f"[START] Memulai merapikan folder: {target_dir}\n" + "-"*50)

        try:
            items = os.listdir(target_dir)
            moved_count = 0

            for item in items:
                item_path = os.path.join(target_dir, item)

                if os.path.isdir(item_path):
                    continue

                _, ext = os.path.splitext(item)
                ext = ext.lower()

                category = "Others"
                for cat, exts in EXTENSIONS_MAP.items():
                    if ext in exts:
                        category = cat
                        break

                category_dir = os.path.join(target_dir, category)
                if not os.path.exists(category_dir):
                    os.makedirs(category_dir)

                final_filename = item
                if self.var_lowercase.get():
                    final_filename = item.lower()

                destination_path = os.path.join(category_dir, final_filename)

                if os.path.exists(destination_path):
                    base, extension = os.path.splitext(final_filename)
                    counter = 1
                    while os.path.exists(destination_path):
                        destination_path = os.path.join(category_dir, f"{base}_{counter}{extension}")
                        counter += 1

                shutil.move(item_path, destination_path)
                self.log(f"[MOVE] '{item}' ➔ '{category}/'")
                moved_count += 1

            self.log("-" * 50)
            self.log(f"[DONE] Selesai! Berhasil merapikan {moved_count} file.\n")
            messagebox.showinfo("Sukses", f"Folder berhasil dirapikan!\nTotal file dipindahkan: {moved_count}")

        except Exception as e:
            self.log(f"[ERROR] Terjadi kesalahan: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat merapikan file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileForgeOrganizerApp(root)
    root.mainloop()
