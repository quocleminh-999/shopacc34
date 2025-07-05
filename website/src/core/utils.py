import random
import string
import re
from typing import Optional, Callable

def random_vietnamese_surname() -> str:
    """Tạo họ tiếng Việt ngẫu nhiên"""
    vietnamese_surnames = [
        "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan",
        "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương",
        "Lý", "Tạ", "Cao", "Mai", "Hà", "Đoàn", "Lâm", "Trương",
        "Văn", "Đinh", "Đinh", "Kiều"
    ]
    return random.choice(vietnamese_surnames)

def random_vietnamese_name() -> str:
    """Tạo tên tiếng Việt ngẫu nhiên"""
    middle_names = [
        "Thị", "Văn", "Hữu", "Đức", "Ngọc", "Thanh", "Trọng", 
        "Phúc", "Anh", "Quang", "Minh", "Hoàng", "Duy", "Xuân"
    ]
    first_names = [
        "An", "Bình", "Châu", "Dương", "Giang", "Hà", "Hải",
        "Hùng", "Hương", "Hồng", "Khanh", "Khánh", "Lan", "Linh",
        "Long", "Minh", "My", "Nam", "Ngọc", "Nhung", "Phong",
        "Quân", "Quỳnh", "Sơn", "Tâm", "Tân", "Thảo", "Thành",
        "Thắng", "Thu", "Thúy", "Trang", "Trinh", "Trung", "Tuấn", 
        "Vân", "Vi", "Vy", "Yến"
    ]
    middle_name = random.choice(middle_names)
    first_name = random.choice(first_names)
    return f"{middle_name} {first_name}"

def convert_vietnamese_to_ascii(text: str) -> str:
    """Chuyển đổi tiếng Việt có dấu thành không dấu"""
    text = text.lower()
    text = text.replace("đ", "d")
    text = text.replace("ă", "a").replace("â", "a").replace("ấ", "a").replace("ầ", "a").replace("ẩ", "a").replace("ẫ", "a").replace("ậ", "a")
    text = text.replace("ê", "e").replace("ế", "e").replace("ề","e").replace("ể", "e").replace("ễ", "e").replace("ệ", "e")
    text = text.replace("ô", "o").replace("ố", "o").replace("ồ", "o").replace("ổ", "o").replace("ỗ", "o").replace("ộ", "o")
    text = text.replace("ơ", "o").replace("ớ", "o").replace("ờ", "o").replace("ở", "o").replace("ỡ", "o").replace("ợ", "o")
    text = text.replace("ư", "u").replace("ứ", "u").replace("ừ", "u").replace("ử", "u").replace("ữ", "u").replace("ự", "u")
    text = text.replace("á", "a").replace("à", "a").replace("ả", "a").replace("ã", "a").replace("ạ", "a")
    text = text.replace("é", "e").replace("è", "e").replace("ẻ", "e").replace("ẽ", "e").replace("ẹ", "e")
    text = text.replace("í", "i").replace("ì", "i").replace("ỉ", "i").replace("ĩ", "i").replace("ị", "i")
    text = text.replace("ó", "o").replace("ò", "o").replace("ỏ", "o").replace("õ", "o").replace("ọ", "o")
    text = text.replace("ú", "u").replace("ù", "u").replace("ủ", "u").replace("ũ", "u").replace("ụ", "u")
    text = text.replace("ý", "y").replace("ỳ", "y").replace("ỷ", "y").replace("ỹ", "y").replace("ỵ", "y")
    text = text.replace(" ", "")
    return text

def generate_random_password(length: int = 15) -> str:
    """Tạo mật khẩu ngẫu nhiên"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_email(name: str) -> str:
    """Tạo email ngẫu nhiên từ tên"""
    random_chars = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
    return f"{name}_{random_chars}@gmail.com"

def log_message(message: str, level: str = "info", callback: Optional[Callable] = None) -> None:
    """Ghi log với callback tùy chọn"""
    if callback:
        callback(message, level)
    else:
        print(f"[{level.upper()}] {message}") 