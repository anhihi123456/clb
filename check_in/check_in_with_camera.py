import os
import subprocess
import platform
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFont

class ModernEventCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MINH CHỨNG SỰ KIỆN - CAMERA PRO")
        self.root.geometry("820x760")
        self.root.configure(bg="#0f172a") # Slate 900
        self.root.resizable(False, False)

        # Cấu hình thư mục lưu
        self.save_dir = "MinhChung_SuKien"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # Khởi tạo Camera DirectShow cho Windows
        if platform.system() == "Windows":
            self.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.video_capture = cv2.VideoCapture(0)

        self.current_frame = None
        self.setup_ui()
        self.check_camera_permission()
        self.update_camera_stream()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # 1. Header Bar
        header = tk.Frame(self.root, bg="#1e293b", height=70) # Slate 800
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header, 
            text="HỆ THỐNG GHI NHẬN MINH CHỨNG SỰ KIỆN", 
            font=("Segoe UI", 15, "bold"), 
            fg="#38bdf8", # Sky 400
            bg="#1e293b"
        )
        title_lbl.pack(side="left", padx=25, pady=10)

        # Trạng thái Camera LED
        self.status_container = tk.Frame(header, bg="#1e293b")
        self.status_container.pack(side="right", padx=25)

        self.status_dot = tk.Canvas(self.status_container, width=12, height=12, bg="#1e293b", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 6))
        self.dot_item = self.status_dot.create_oval(2, 2, 10, 10, fill="#22c55e", outline="") # Green

        self.status_lbl = tk.Label(
            self.status_container, 
            text="LIVE", 
            font=("Segoe UI", 9, "bold"), 
            fg="#22c55e", 
            bg="#1e293b"
        )
        self.status_lbl.pack(side="left")

        # 2. Main Content Card
        main_card = tk.Frame(self.root, bg="#0f172a")
        main_card.pack(fill="both", expand=True, padx=25, pady=15)

        # Input Box
        input_container = tk.Frame(main_card, bg="#1e293b", padx=15, pady=12)
        input_container.pack(fill="x", pady=(0, 15))

        lbl_input = tk.Label(
            input_container, 
            text="TÊN SỰ KIỆN / HOẠT ĐỘNG", 
            font=("Segoe UI", 9, "bold"), 
            fg="#94a3b8", 
            bg="#1e293b"
        )
        lbl_input.pack(anchor="w", pady=(0, 5))

        self.entry_event = tk.Entry(
            input_container, 
            font=("Segoe UI", 11), 
            bg="#0f172a", 
            fg="#f8fafc", 
            insertbackground="#38bdf8",
            relief="flat", 
            highlightthickness=1, 
            highlightbackground="#334155", 
            highlightcolor="#38bdf8"
        )
        self.entry_event.insert(0, "Họp Chi Đoàn / Hội Nghị Sinh Viên")
        self.entry_event.pack(fill="x", ipady=8)

        # Khung hiển thị Camera Preview
        preview_border = tk.Frame(main_card, bg="#1e293b", padx=4, pady=4)
        preview_border.pack(fill="both", expand=True)

        self.preview_lbl = tk.Label(preview_border, bg="#020617")
        self.preview_lbl.pack(fill="both", expand=True)

        # 3. Footer Action Controls
        footer = tk.Frame(self.root, bg="#0f172a", pady=15)
        footer.pack(fill="x", side="bottom", padx=25)

        self.btn_capture = tk.Button(
            footer, 
            text="📸  CHỤP & LƯU MINH CHỨNG", 
            font=("Segoe UI", 11, "bold"), 
            bg="#0284c7", # Sky 600
            fg="#ffffff", 
            activebackground="#0369a1", 
            activeforeground="#ffffff",
            relief="flat", 
            cursor="hand2", 
            command=self.capture_photo,
            pady=10
        )
        self.btn_capture.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_open = tk.Button(
            footer, 
            text="📁  MỞ THƯ MỤC", 
            font=("Segoe UI", 11, "bold"), 
            bg="#334155", # Slate 700
            fg="#f8fafc", 
            activebackground="#475569", 
            activeforeground="#ffffff",
            relief="flat", 
            cursor="hand2", 
            command=self.open_storage_folder,
            pady=10, 
            width=18
        )
        self.btn_open.pack(side="right")

    def check_camera_permission(self):
        if not self.video_capture.isOpened():
            self.status_dot.itemconfig(self.dot_item, fill="#ef4444")
            self.status_lbl.configure(text="OFFLINE", fg="#ef4444")
            messagebox.showerror(
                "Lỗi Camera",
                "Không thể truy cập camera!\n\n"
                "1. Kiểm tra camera có bị phần mềm khác (Teams, Meet, Zoom) chiếm dụng không.\n"
                "2. Mở Windows Settings > Privacy & security > Camera để cấp quyền cho Desktop Apps."
            )

    def update_camera_stream(self):
        if self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.flip(frame, 1)
                self.current_frame = frame.copy()

                cv2_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(cv2_rgb)
                pil_img = pil_img.resize((762, 450), Image.Resampling.LANCZOS)

                imgtk = ImageTk.PhotoImage(image=pil_img)
                self.preview_lbl.imgtk = imgtk
                self.preview_lbl.configure(image=imgtk)

        self.root.after(16, self.update_camera_stream)

    def capture_photo(self):
        if self.current_frame is None:
            messagebox.showwarning("Cảnh báo", "Chưa nhận diện được khung hình camera!")
            return

        event_name = self.entry_event.get().strip()
        if not event_name:
            messagebox.showwarning("Nhắc nhở", "Vui lòng nhập tên sự kiện trước khi chụp!")
            return

        # Chuyển OpenCV frame sang PIL Image để vẽ text tiếng Việt có dấu chuẩn đẹp
        rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        draw = ImageDraw.Draw(image, "RGBA")
        width, height = image.size

        # Load font Unicode chuẩn của hệ điều hành
        try:
            if platform.system() == "Windows":
                font = ImageFont.truetype("arial.ttf", 22)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Thông tin watermark
        timestamp_str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        text_line1 = f"SỰ KIỆN: {event_name.upper()}"
        text_line2 = f"THỜI GIAN: {timestamp_str}"

        # Vẽ dải nền tối mờ (Dark overlay banner) ở góc dưới để text luôn rõ nét
        banner_height = 80
        draw.rectangle(
            [(0, height - banner_height), (width, height)], 
            fill=(15, 23, 42, 210) # Slate 900 với độ trong suốt alpha
        )

        # Vẽ dải màu nhấn (Sky blue stripe)
        draw.rectangle([(0, height - banner_height), (6, height)], fill=(56, 189, 248, 255))

        # Vẽ text tiếng Việt đầy đủ dấu
        draw.text((25, height - banner_height + 12), text_line1, fill=(255, 255, 255), font=font)
        draw.text((25, height - banner_height + 45), text_line2, fill=(148, 163, 184), font=font)

        # Lưu ảnh JPG chất lượng cao
        save_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"minh_chung_{save_time}.jpg"
        file_path = os.path.join(self.save_dir, file_name)

        image.convert("RGB").save(file_path, "JPEG", quality=95)

        ans = messagebox.askyesno(
            "Đã Lưu Ảnh", 
            f"Ảnh minh chứng đã lưu thành công:\n{file_name}\n\nBạn có muốn mở thư mục ảnh ngay không?"
        )
        if ans:
            self.open_storage_folder()

    def open_storage_folder(self):
        path = os.path.abspath(self.save_dir)
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def on_close(self):
        if self.video_capture.isOpened():
            self.video_capture.release()
        self.root.destroy()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = ModernEventCameraApp(app_root)
    app_root.mainloop()