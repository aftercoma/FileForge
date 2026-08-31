import os, shutil
from pathlib import Path 


class Ext:
    def __init__(self):
        self.extention_map = {
    "Media": [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".bmp",
        ".svg",
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".mp3",
        ".wav",
        ".flac",
    ],

    "Dokumen": [
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".odt",
        ".ods",
        ".odp",
    ],

    "Arsip": [
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
    ],

    "Kode": [
        ".py",
        ".js",
        ".ts",
        ".html",
        ".css",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".sh",
        ".json",
        ".xml",
        ".class",
        ".lua",
        ".php",
    ],
}
    def manage(self, Target_Dir: Path):
        if not Target_Dir.exists():
            print(f"Target Folder Tidak Ditemukan! {Target_Dir}")
            return 
        print(f"[START] Organize the target [{Target_Dir}]")
        for item in list(Target_Dir.iterdir()):
            print(f"DEBUG [{item}]")
            if item.is_dir():
                continue 
            file_ext = item.suffix.lower()
            moved = False 
            for category, extensions in self.extention_map.items():
                if file_ext in extensions:
                    dest_dir = Target_Dir / category 
                    dest_dir.mkdir(exist_ok=True)
                    shutil.move(
                            str(item),
                            str(dest_dir / item.name)
                            )

                    print(f"[MOVED] {item.name} -> {category}")

                    moved = True
                    break 
            if not moved:
                dest_dir = Target_Dir / "Lainnya"
                dest_dir.mkdir(exist_ok=True)
                shutil.move(
                    str(item),
                    str(dest_dir / item.name)
                )

                print(f"[MOVED] {item.name} -> Lainnya/")

if __name__=="__main__":
    print (r"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ███████╗██╗██╗     ███████╗                           ║
║   ██╔════╝██║██║     ██╔════╝                           ║
║   █████╗  ██║██║     █████╗                             ║
║   ██╔══╝  ██║██║     ██╔══╝                             ║
║   ██║     ██║███████╗███████╗                           ║
║   ╚═╝     ╚═╝╚══════╝╚══════╝                           ║
║                                                          ║
║                    F I L E M A N A G E                  ║
║                                                          ║
║                 Python File Organizer                   ║
║                                                          ║
║              [ Organize • Sort • Clean ]                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝           

           """)
    raw = input(f"({Path.home()})/: ").strip()
    etc = Path.home() / raw
    app = Ext()
    app.manage(etc)
