import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Optional
from ..config.constants import COLORS
from .reg_tab import RegTab
from .settings_tab import SettingsTab
from ..core.proxy_manager import ProxyManager
from ..core.facebook_reg import FacebookRegister
from ..core.utils import (
    random_vietnamese_surname,
    random_vietnamese_name,
    generate_random_password,
    generate_random_email,
    convert_vietnamese_to_ascii
)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Thiết lập cửa sổ chính
        self.title("Facebook Registration Tool")
        self.geometry("1366x768")
        self.configure(bg=COLORS["bg"])
        
        # Khởi tạo các thành phần
        self.proxy_manager = ProxyManager()
        self.facebook_register = FacebookRegister(self.proxy_manager)
        self.registration_threads = []
        self.success_count = 0
        
        # Thiết lập giao diện
        self.setup_ui()
        
        # Tải proxy ban đầu
        self.load_initial_proxies()

    def setup_ui(self):
        # Tạo notebook để chứa các tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tạo tab đăng ký
        self.reg_tab = RegTab(self.notebook, self.start_registration, self.stop_registration)
        self.notebook.add(self.reg_tab, text="Đăng Ký")
        
        # Tạo tab cài đặt
        self.settings_tab = SettingsTab(self.notebook)
        self.notebook.add(self.settings_tab, text="Cài Đặt Tên")
        
        # Cập nhật danh sách tên khi chuyển tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Khởi tạo danh sách tên ban đầu
        name_type = self.settings_tab.name_type_var.get()
        name_list = self.settings_tab.get_name_list(name_type)
        self.reg_tab.update_name_list(name_list)

    def load_initial_proxies(self):
        """Tải proxy ban đầu từ file"""
        if self.proxy_manager.load_proxies(self.reg_tab.add_log):
            self.reg_tab.add_log("Đã tải proxy thành công", "success")
        else:
            self.reg_tab.add_log("Không thể tải proxy từ file", "error")

    def start_registration(self, thread_count: int, proxy_source: str):
        """Bắt đầu quá trình đăng ký"""
        # Xử lý nguồn proxy
        if proxy_source == "free":
            if not self.proxy_manager.get_proxyscrape(self.reg_tab.add_log):
                return
            if not self.proxy_manager.load_proxies(self.reg_tab.add_log):
                return

        # Tạo các luồng đăng ký
        for i in range(thread_count):
            thread = threading.Thread(
                target=self.registration_worker,
                args=(i + 1,),
                daemon=True
            )
            self.registration_threads.append(thread)
            thread.start()
            
            # Thêm dòng mới vào bảng
            self.reg_tab.reg_table.insert("", "end", values=(i + 1, "", "", "", "Đang chờ", ""))

    def stop_registration(self):
        """Dừng quá trình đăng ký"""
        self.reg_tab.running = False
        self.registration_threads.clear()

    def registration_worker(self, thread_id: int):
        """Xử lý đăng ký trong một luồng"""
        while self.reg_tab.running:
            try:
                # Lấy danh sách tên hiện tại
                name_type = self.settings_tab.name_type_var.get()
                name_list = self.settings_tab.get_name_list(name_type)
                
                # Tạo thông tin người dùng ngẫu nhiên
                import random
                ho = random.choice(name_list["surnames"])
                ten = random.choice(name_list["first_names"])
                
                # Thêm tên đệm nếu có
                if name_list["middle_names"]:
                    ten_dem = random.choice(name_list["middle_names"])
                    name = f"{ho} {ten_dem} {ten}"
                else:
                    name = f"{ho} {ten}"
                    
                email = generate_random_email(convert_vietnamese_to_ascii(name))
                password = generate_random_password()
                
                # Cập nhật trạng thái
                self.reg_tab.update_registration_status(
                    thread_id, "", name, email, "Đang đăng ký", "Đang tạo tài khoản..."
                )
                
                # Thực hiện đăng ký
                if self.facebook_register.register(ho, ten, email, password, self.reg_tab.add_log):
                    self.success_count += 1
                    self.reg_tab.update_success_count(self.success_count)
                    self.reg_tab.update_registration_status(
                        thread_id, self.facebook_register.dem, name, email, "Thành công", "Đăng ký thành công"
                    )
                else:
                    self.reg_tab.update_registration_status(
                        thread_id, "", name, email, "Thất bại", "Đăng ký thất bại"
                    )
                
                # Đợi một chút trước khi thử lại
                time.sleep(2)
                
            except Exception as e:
                self.reg_tab.add_log(f"Lỗi trong luồng {thread_id}: {str(e)}", "error")
                self.reg_tab.update_registration_status(
                    thread_id, "", "", "", "Lỗi", str(e)
                )
                time.sleep(5)  # Đợi lâu hơn nếu có lỗi

    def on_tab_changed(self, event):
        """Xử lý sự kiện khi chuyển tab"""
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        
        if tab_name == "Đăng Ký":
            # Cập nhật danh sách tên trong tab đăng ký
            name_type = self.settings_tab.name_type_var.get()
            name_list = self.settings_tab.get_name_list(name_type)
            self.reg_tab.update_name_list(name_list)

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main() 