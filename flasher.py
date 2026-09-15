import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import shutil
import threading
import platform

class AndroidFlasherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB & Fastboot Flasher Utility ⚡")
        self.root.geometry("650x700")
        self.root.minsize(600, 600)

        # Cek tools di system
        self.adb_path = shutil.which("adb")
        self.fastboot_path = shutil.which("fastboot")

        self.setup_styles()
        self.create_widgets()
        self.check_dependencies()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    def create_widgets(self):
        # 1. FRAME STATUS DEPENDENCY
        status_frame = ttk.LabelFrame(self.root, text=" System Status ", padding=8)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.lbl_dep = ttk.Label(status_frame, text="Checking system...", font=("Arial", 9))
        self.lbl_dep.pack(anchor="w")

        # 2. FRAME DEVICE CHECKER (REFRESH DEVICES)
        device_frame = ttk.LabelFrame(self.root, text=" Device Connection Checker ", padding=8)
        device_frame.pack(fill="x", padx=10, pady=5)

        self.btn_ref_adb = ttk.Button(device_frame, text="🔄 Check ADB Devices", command=lambda: self.run_command(["adb", "devices"]))
        self.btn_ref_adb.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_ref_fastboot = ttk.Button(device_frame, text="🔄 Check Fastboot Devices", command=lambda: self.run_command(["fastboot", "devices"]))
        self.btn_ref_fastboot.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # 3. FRAME FILE SELECTOR (Untuk file .img / .zip / dll)
        file_frame = ttk.LabelFrame(self.root, text=" File Selector (Recovery / Zip / File) ", padding=8)
        file_frame.pack(fill="x", padx=10, pady=5)

        self.entry_file = ttk.Entry(file_frame, font=("Arial", 10))
        self.entry_file.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_browse = ttk.Button(file_frame, text="📁 Browse File", command=self.browse_file)
        self.btn_browse.pack(side="right")

        # 4. FRAME ADB PUSH MANAGER (FITUR BARU)
        push_frame = ttk.LabelFrame(self.root, text=" ADB Push Options ", padding=8)
        push_frame.pack(fill="x", padx=10, pady=5)

        lbl_dest = ttk.Label(push_frame, text="Target Folder:", font=("Arial", 9))
        lbl_dest.pack(side="left", padx=(0, 5))

        # Dropdown pilihan direktori tujuan di HP
        self.dest_var = tk.StringVar(value="/sdcard/")
        dest_options = [
            "/sdcard/", 
            "/sdcard/Download/", 
            "/sdcard/Documents/", 
            "/data/local/tmp/", 
            "/storage/emulated/0/"
        ]
        self.combo_dest = ttk.Combobox(push_frame, textvariable=self.dest_var, values=dest_options, font=("Arial", 9))
        self.combo_dest.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_push = ttk.Button(push_frame, text="📤 ADB Push File", command=self.adb_push_file)
        self.btn_push.pack(side="right")

        # 5. FRAME KONTROL ADB & FASTBOOT ACTIONS
        action_frame = ttk.LabelFrame(self.root, text=" Actions Control Panel ", padding=10)
        action_frame.pack(fill="x", padx=10, pady=5)

        # Baris 1: ADB Reboots
        lbl_adb = ttk.Label(action_frame, text="ADB State:", font=("Arial", 9, "bold"))
        lbl_adb.grid(row=0, column=0, sticky="w", pady=5)

        self.btn_reboot_bl = ttk.Button(action_frame, text="Reboot to Bootloader", command=lambda: self.run_command(["adb", "reboot", "bootloader"]))
        self.btn_reboot_bl.grid(row=0, column=1, padx=5, sticky="ew")

        self.btn_reboot_rec = ttk.Button(action_frame, text="Reboot to Recovery", command=lambda: self.run_command(["adb", "reboot", "recovery"]))
        self.btn_reboot_rec.grid(row=0, column=2, padx=5, sticky="ew")

        # Baris 2: Fastboot Commands
        lbl_fastboot = ttk.Label(action_frame, text="Fastboot State:", font=("Arial", 9, "bold"))
        lbl_fastboot.grid(row=1, column=0, sticky="w", pady=5)

        self.btn_flash = ttk.Button(action_frame, text="Fastboot Flash Recovery", command=self.fastboot_flash)
        self.btn_flash.grid(row=1, column=1, padx=5, sticky="ew")

        self.btn_boot = ttk.Button(action_frame, text="Fastboot Boot Image", command=self.fastboot_boot)
        self.btn_boot.grid(row=1, column=2, padx=5, sticky="ew")

        action_frame.columnconfigure(1, weight=1)
        action_frame.columnconfigure(2, weight=1)

        # 6. FRAME LOG / TERMINAL OUTPUT
        log_frame = ttk.LabelFrame(self.root, text=" Execution Output / Logs ", padding=8)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4", height=10)
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        self.btn_clear = ttk.Button(self.root, text="Clear Logs", command=lambda: self.log_text.delete(1.0, tk.END))
        self.btn_clear.pack(anchor="e", padx=10, pady=5)

    def check_dependencies(self):
        missing = []
        if not self.adb_path: missing.append("ADB")
        if not self.fastboot_path: missing.append("Fastboot")

        if missing:
            self.lbl_dep.config(text=f"❌ Missing tools: {', '.join(missing)}. Pastikan sudah terinstall di system PATH.", foreground="red")
        else:
            self.lbl_dep.config(text=f"✅ OS: {platform.system()} | ADB & Fastboot Ready!", foreground="green")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Pilih File",
            filetypes=[("All Files", "*.*"), ("Image Files", "*.img"), ("Zip Files", "*.zip")]
        )
        if file_path:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file_path)
            self.log(f"[INFO] File dipilih: {file_path}\n")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def run_command(self, cmd_list):
        def target():
            self.log(f"$ {' '.join(cmd_list)}")
            try:
                process = subprocess.Popen(
                    cmd_list,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                for line in process.stdout:
                    self.log(line.strip())
                process.wait()
                self.log("[DONE] Eksekusi selesai.\n" + "-"*40)
            except Exception as e:
                self.log(f"[ERROR] Gagal menjalankan perintah: {e}\n" + "-"*40)

        threading.Thread(target=target, daemon=True).start()

    def adb_push_file(self):
        file_path = self.entry_file.get().strip()
        target_dir = self.dest_var.get().strip()

        if not file_path:
            messagebox.showwarning("Warning", "Pilih file yang mau di-push terlebih dahulu lewat tombol Browse!")
            return
        if not target_dir:
            messagebox.showwarning("Warning", "Tentukan direktori tujuan penyimpanan di HP!")
            return

        # Perintah: adb push <file_lokal> <target_dir_hp>
        self.run_command(["adb", "push", file_path, target_dir])

    def fastboot_flash(self):
        img_path = self.entry_file.get().strip()
        if not img_path:
            messagebox.showwarning("Warning", "Pilih file .img recovery terlebih dahulu!")
            return
        self.run_command(["fastboot", "flash", "recovery", img_path])

    def fastboot_boot(self):
        img_path = self.entry_file.get().strip()
        if not img_path:
            messagebox.showwarning("Warning", "Pilih file .img image terlebih dahulu!")
            return
        self.run_command(["fastboot", "boot", img_path])

if __name__ == "__main__":
    root = tk.Tk()
    app = AndroidFlasherApp(root)
    root.mainloop()
