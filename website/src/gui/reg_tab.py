import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from typing import Callable, Optional, Dict, List
from ..config.constants import COLORS

class RegTab(ttk.Frame):
    def __init__(self, parent, on_start: Callable, on_stop: Callable):
        super().__init__(parent)
        self.on_start = on_start
        self.on_stop = on_stop
        self.running = False
        self.threads = []
        self.name_list = None  # Khởi tạo name_list
        self.setup_ui()

    def setup_ui(self):
        # Top frame for controls
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Thread count selection
        ttk.Label(control_frame, text="Số Luồng:").pack(side=tk.LEFT, padx=5)
        self.thread_spinbox = ttk.Spinbox(control_frame, from_=1, to=50, width=5)
        self.thread_spinbox.set("1")
        self.thread_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Proxy selection
        ttk.Label(control_frame, text="Nguồn Proxy:").pack(side=tk.LEFT, padx=5)
        self.proxy_var = tk.StringVar(value="file")
        ttk.Radiobutton(control_frame, text="File", variable=self.proxy_var, value="file").pack(side=tk.LEFT)
        ttk.Radiobutton(control_frame, text="Miễn Phí", variable=self.proxy_var, value="free").pack(side=tk.LEFT)
        
        # Start/Stop buttons
        self.start_button = ttk.Button(
            control_frame,
            text="Bắt Đầu",
            command=self.start_registration,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ttk.Button(
            control_frame,
            text="Dừng",
            command=self.stop_registration,
            state=tk.DISABLED,
            style="Accent.TButton"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(status_frame, text="Trạng Thái:").pack(side=tk.LEFT, padx=5)
        self.status_label = ttk.Label(status_frame, text="Sẵn Sàng")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(status_frame, text="Đăng Ký Thành Công:").pack(side=tk.LEFT, padx=20)
        self.count_label = ttk.Label(status_frame, text="0", foreground=COLORS["success"])
        self.count_label.pack(side=tk.LEFT, padx=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(self, text="Nhật Ký Hoạt Động")
        log_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=5,
            font=("Segoe UI", 10)
        )
        self.log_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Table frame
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ("thread", "name", "email", "status", "log")
        self.reg_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Treeview"
        )
        
        # Define headings
        self.reg_table.heading("thread", text="Luồng")
        self.reg_table.heading("name", text="Tên")
        self.reg_table.heading("email", text="Email")
        self.reg_table.heading("status", text="Trạng Thái")
        self.reg_table.heading("log", text="Nhật Ký")
        
        # Define columns width
        self.reg_table.column("thread", width=50)
        self.reg_table.column("name", width=200)
        self.reg_table.column("email", width=250)
        self.reg_table.column("status", width=100)
        self.reg_table.column("log", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.reg_table.yview)
        self.reg_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.reg_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def add_log(self, message: str, level: str = "info"):
        """Thêm thông báo vào khung log với màu sắc tương ứng"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Xác định màu sắc dựa trên cấp độ log
        if level == "success":
            color = COLORS["success"]
        elif level == "warning":
            color = COLORS["warning"]
        elif level == "error":
            color = COLORS["error"]
        else:  # info
            color = COLORS["fg"]
        
        # Thêm log vào khung văn bản
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.tag_configure("timestamp", foreground=COLORS["accent"])
        self.log_text.tag_configure(level, foreground=color)
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.see(tk.END)  # Cuộn xuống dòng mới nhất

    def start_registration(self):
        try:
            thread_count = int(self.thread_spinbox.get())
            if thread_count < 1:
                self.add_log("Số luồng phải ít nhất là 1", "error")
                return
        except ValueError:
            self.add_log("Số luồng không hợp lệ", "error")
            return
        
        # Xóa log cũ
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)
        
        # Thêm log bắt đầu
        self.add_log(f"Bắt đầu quá trình đăng ký với {thread_count} luồng")
        
        # Clear table
        for item in self.reg_table.get_children():
            self.reg_table.delete(item)
        
        # Update UI
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Đang chạy")
        
        # Start registration
        self.on_start(thread_count, self.proxy_var.get())

    def stop_registration(self):
        self.running = False
        self.status_label.config(text="Đang dừng...")
        self.add_log("Đang dừng tất cả các luồng...", "warning")
        
        # Stop registration
        self.on_stop()
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Đã dừng")
        self.add_log("Đã dừng tất cả các luồng", "warning")

    def update_registration_status(self, thread_id: int, uid: str, name: str, email: str, status: str, log: str):
        """Cập nhật trạng thái đăng ký trong bảng"""
        items = self.reg_table.get_children()
        item_id = items[thread_id - 1] if thread_id <= len(items) else None
        
        if not item_id:
            return
            
        self.reg_table.item(item_id, values=(thread_id, name, email, status, log))

    def update_success_count(self, count: int):
        """Cập nhật số lượng đăng ký thành công"""
        self.count_label.config(text=str(count))

    def update_name_list(self, name_list: Dict[str, List[str]]):
        """Cập nhật danh sách tên từ tab cài đặt"""
        if not name_list:
            return
            
        self.name_list = name_list
        self.add_log(f"Đã cập nhật danh sách tên: {name_list['surnames'][0]}...", "success") 