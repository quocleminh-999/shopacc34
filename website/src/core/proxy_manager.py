import os
import time
import requests
from typing import Optional, Dict, List, Callable
from .utils import log_message
from ..config.constants import PROXY_FILE, PROXY_LIVE_FILE

class ProxyManager:
    def __init__(self):
        self.proxy_list: List[Dict] = []
        self.current_proxy_index = 0

    def load_proxies(self, callback: Optional[Callable] = None) -> bool:
        """Tải proxy từ file"""
        try:
            with open(PROXY_FILE, 'r') as f:
                for line in f:
                    if line.strip():
                        proxy_parts = line.strip().split(':')
                        if len(proxy_parts) == 2:
                            proxy = {
                                'http': f'http://{proxy_parts[0]}:{proxy_parts[1]}',
                                'https': f'http://{proxy_parts[0]}:{proxy_parts[1]}'
                            }
                            self.proxy_list.append(proxy)   
                        elif len(proxy_parts) == 4:
                            proxy = {
                                'http': f'http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}',
                                'https': f'http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}'
                            }
                            self.proxy_list.append(proxy)
            if self.proxy_list:
                log_message("Đã tải proxy từ file thành công", "success", callback)
                return True
            else:
                log_message("Không tìm thấy proxy hợp lệ trong file", "error", callback)
                return False
        except Exception as e:
            log_message(f"Lỗi load proxy: {str(e)}", "error", callback)
            return False

    def check_proxy(self, proxy: Dict, callback: Optional[Callable] = None) -> bool:
        """Kiểm tra proxy có hoạt động không"""
        try:
            test_url = 'https://api.ipify.org?format=json'
            response = requests.get(test_url, proxies=proxy, timeout=10)
            if response.status_code == 200:
                proxy_display = proxy['http'].split('://')[-1]
                proxy_display = proxy_display.split('@')[-1]
                log_message(f"Proxy live: {proxy_display}", "info", callback)
                return True
                
            proxy_display = proxy['http'].split('://')[-1].split('@')[-1]
            log_message(f"Proxy die: {proxy_display}", "error", callback)
            if proxy in self.proxy_list:
                self.proxy_list.remove(proxy)
            self.remove_proxy_from_file(proxy)
            return False
            
        except:
            proxy_display = proxy['http'].split('://')[-1].split('@')[-1]
            log_message(f"Proxy die: {proxy_display}", "error", callback)
            if proxy in self.proxy_list:
                self.proxy_list.remove(proxy)
            self.remove_proxy_from_file(proxy)
            return False

    def remove_proxy_from_file(self, proxy_to_remove: Dict) -> bool:
        """Xóa proxy die khỏi file"""
        try:
            with open(PROXY_FILE, 'r') as f:
                proxies = f.readlines()
            proxy_str = proxy_to_remove['http'].split('://')[-1].split('@')[-1]
            good_proxies = []
            for proxy_line in proxies:
                proxy_line = proxy_line.strip()
                if proxy_line:
                    if len(proxy_line.split(':')) == 2:
                        if proxy_line != proxy_str:
                            good_proxies.append(proxy_line + '\n')
                    elif len(proxy_line.split(':')) == 4:
                        proxy_parts = proxy_line.split(':')
                        proxy_compare = f"{proxy_parts[0]}:{proxy_parts[1]}"
                        if proxy_compare != proxy_str:
                            good_proxies.append(proxy_line + '\n')
            with open(PROXY_FILE, 'w') as f:
                f.writelines(good_proxies)
            return True
        except Exception as e:
            log_message(f"Lỗi khi xóa proxy: {str(e)}", "error")
            return False

    def get_next_proxy(self, callback: Optional[Callable] = None) -> Optional[Dict]:
        """Lấy proxy tiếp theo"""
        while True:
            if not self.proxy_list:
                log_message("Đã hết proxy trong file proxy.txt!", "error", callback)
                return None
                
            if self.current_proxy_index >= len(self.proxy_list):
                self.current_proxy_index = 0
                
            proxy = self.proxy_list[self.current_proxy_index]
            self.current_proxy_index += 1
            return proxy

    def get_proxyscrape(self, callback: Optional[Callable] = None) -> bool:
        """Lấy proxy miễn phí từ proxyscrape"""
        try:
            log_message("Đang lấy Proxy Free...", "info", callback)
            url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=text"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                proxies = response.text.strip().split('\n')
                total_proxies = len(proxies)
                with open(PROXY_FILE, 'w') as f:
                    for proxy in proxies:
                        proxy = proxy.strip()
                        if proxy:
                            f.write(proxy + '\n')
                log_message(f"Đã lưu {total_proxies} proxy vào file proxy.txt", "success", callback)
                return True
            else:
                log_message("Không thể kết nối tới API Proxy Free!", "error", callback)
                return False
        except Exception as e:
            log_message(f"Lỗi khi lấy proxy free: {str(e)}", "error", callback)
            return False 