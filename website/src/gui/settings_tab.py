import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
from typing import Dict, List, Optional
from ..config.constants import COLORS
from ..config.name_lists import NAME_TYPES

class SettingsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name_lists = NAME_TYPES.copy()
        self.custom_lists = self.load_custom_lists()
        self.setup_ui()

    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame cho cài đặt tên
        name_frame = ttk.LabelFrame(main_frame, text="Cài Đặt Tên")
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame cho combobox và nút
        control_frame = ttk.Frame(name_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Chọn loại tên
        ttk.Label(control_frame, text="Loại Tên:").pack(side=tk.LEFT, padx=5)
        self.name_type_var = tk.StringVar(value="vietnamese")
        name_type_combo = ttk.Combobox(
            control_frame,
            textvariable=self.name_type_var,
            values=list(self.name_lists.keys()) + list(self.custom_lists.keys()),
            state="readonly",
            width=20
        )
        name_type_combo.pack(side=tk.LEFT, padx=5)
        
        # Thêm sự kiện khi chọn loại tên
        name_type_combo.bind("<<ComboboxSelected>>", lambda e: self.load_name_list(self.name_type_var.get()))
        
        # Nút thêm danh sách tùy chỉnh
        ttk.Button(
            control_frame,
            text="Thêm Danh Sách Tùy Chỉnh",
            command=self.show_custom_list_dialog
        ).pack(side=tk.LEFT, padx=10)
        
        # Frame cho danh sách tên
        lists_frame = ttk.Frame(main_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tạo grid layout cho các frame tên
        lists_frame.columnconfigure(0, weight=1)
        lists_frame.columnconfigure(1, weight=1)
        lists_frame.columnconfigure(2, weight=1)
        lists_frame.rowconfigure(0, weight=1)
        
        # Họ
        surname_frame = ttk.LabelFrame(lists_frame, text="Họ")
        surname_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.surname_text = scrolledtext.ScrolledText(surname_frame, height=15, wrap=tk.WORD)
        self.surname_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tên đệm
        middle_frame = ttk.LabelFrame(lists_frame, text="Tên Đệm")
        middle_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.middle_text = scrolledtext.ScrolledText(middle_frame, height=15, wrap=tk.WORD)
        self.middle_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tên
        first_frame = ttk.LabelFrame(lists_frame, text="Tên")
        first_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.first_text = scrolledtext.ScrolledText(first_frame, height=15, wrap=tk.WORD)
        self.first_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame cho nút lưu
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Nút lưu
        save_button = ttk.Button(
            button_frame,
            text="Lưu Thay Đổi",
            command=self.save_changes,
            style="Accent.TButton"
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Tạo style cho nút
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        
        # Load danh sách tên ban đầu
        self.load_name_list("vietnamese")

    def load_custom_lists(self) -> Dict:
        """Tải danh sách tên tùy chỉnh từ file"""
        try:
            if os.path.exists("custom_names.json"):
                with open("custom_names.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return {}

    def save_custom_lists(self):
        """Lưu danh sách tên tùy chỉnh vào file"""
        try:
            with open("custom_names.json", "w", encoding="utf-8") as f:
                json.dump(self.custom_lists, f, ensure_ascii=False, indent=2)
        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"Không thể lưu danh sách tùy chỉnh: {str(e)}")

    def show_custom_list_dialog(self):
        """Hiển thị dialog thêm danh sách tùy chỉnh"""
        dialog = tk.Toplevel(self)
        dialog.title("Thêm Danh Sách Tùy Chỉnh")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Tên Danh Sách:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        def add_list():
            name = name_var.get().strip().lower()
            if not name:
                tk.messagebox.showwarning("Cảnh Báo", "Vui lòng nhập tên danh sách")
                return
            if name in self.name_lists or name in self.custom_lists:
                tk.messagebox.showwarning("Cảnh Báo", "Tên danh sách đã tồn tại")
                return
                
            self.custom_lists[name] = {
                "surnames": [],
                "middle_names": [],
                "first_names": []
            }
            self.name_type_var.set(name)
            self.load_name_list(name)
            self.save_custom_lists()
            dialog.destroy()
            
        ttk.Button(dialog, text="Thêm", command=add_list).pack(pady=10)

    def load_name_list(self, name_type: str):
        """Tải danh sách tên vào các text box"""
        lists = self.name_lists.get(name_type) or self.custom_lists.get(name_type)
        if not lists:
            return
            
        # Xóa nội dung cũ
        self.surname_text.delete(1.0, tk.END)
        self.middle_text.delete(1.0, tk.END)
        self.first_text.delete(1.0, tk.END)
        
        # Thêm nội dung mới
        self.surname_text.insert(tk.END, "\n".join(lists["surnames"]))
        self.middle_text.insert(tk.END, "\n".join(lists["middle_names"]))
        self.first_text.insert(tk.END, "\n".join(lists["first_names"]))
        
        # Cuộn lên đầu
        self.surname_text.see("1.0")
        self.middle_text.see("1.0")
        self.first_text.see("1.0")

    def save_changes(self):
        """Lưu thay đổi vào danh sách tên"""
        name_type = self.name_type_var.get()
        if name_type in self.name_lists:
            # Tạo bản sao của danh sách tùy chỉnh
            self.custom_lists[name_type] = {
                "surnames": self.surname_text.get(1.0, tk.END).strip().split("\n"),
                "middle_names": self.middle_text.get(1.0, tk.END).strip().split("\n"),
                "first_names": self.first_text.get(1.0, tk.END).strip().split("\n")
            }
        else:
            # Cập nhật danh sách tùy chỉnh
            self.custom_lists[name_type].update({
                "surnames": self.surname_text.get(1.0, tk.END).strip().split("\n"),
                "middle_names": self.middle_text.get(1.0, tk.END).strip().split("\n"),
                "first_names": self.first_text.get(1.0, tk.END).strip().split("\n")
            })
        
        self.save_custom_lists()
        tk.messagebox.showinfo("Thành Công", "Đã lưu thay đổi")

    def get_name_list(self, name_type: str) -> Dict[str, List[str]]:
        """Lấy danh sách tên theo loại"""
        return self.custom_lists.get(name_type) or self.name_lists.get(name_type) 