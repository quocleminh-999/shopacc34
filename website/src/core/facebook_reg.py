import time
import json
import re
import random
import os
import requests
from bs4 import BeautifulSoup
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from nacl.public import SealedBox, PublicKey
from typing import Optional, Dict, Callable
from .utils import log_message
from .proxy_manager import ProxyManager
from ..config.constants import FACEBOOK_REG_URL, FACEBOOK_AJAX_REG_URL, FACEBOOK_CONFIRM_URL, SUCCESS_FILE, MAX_RETRIES

class FacebookRegister:
    def __init__(self, proxy_manager: ProxyManager):
        self.proxy_manager = proxy_manager
        self.session = requests.Session()
        self.dem = 0

    def get_random_headers(self) -> Dict:
        """Tạo headers ngẫu nhiên"""
        user_agents = [
            # Chrome
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        ]

        sec_ch_ua_list = [
            '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            '"Google Chrome";v="130", "Chromium";v="130", "Not_A Brand";v="23"',
            '"Google Chrome";v="129", "Chromium";v="129", "Not_A Brand";v="22"',
            '"Google Chrome";v="128", "Chromium";v="128", "Not_A Brand";v="21"',
            '"Google Chrome";v="127", "Chromium";v="127", "Not_A Brand";v="20"',
        ]

        headers = {
            'sec-ch-ua': random.choice(sec_ch_ua_list),
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': random.choice(user_agents),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.facebook.com/',
        }

        return headers

    def check_live_fb(self, uid: str, proxy: Optional[Dict] = None) -> str:
        """Kiểm tra tài khoản Facebook có hoạt động không"""
        url = f"https://graph2.facebook.com/v3.3/{uid}/picture?redirect=0"
        try:
            response = requests.get(url, timeout=30, proxies=proxy)
            check_data = response.json()
            if not check_data.get('data', {}).get('height') or not check_data.get('data', {}).get('width'):
                return 'DIE'
            return 'LIVE'
        except:
            return 'DIE'

    def encrypt_password(self, public_key_data: Dict, password: str) -> str:
        """Mã hóa mật khẩu"""
        try:
            vn_time = str(int(time.time()))
            key_id = int(public_key_data['keyId'])
            public_key = bytes.fromhex(public_key_data['publicKey'])
            if len(public_key) != 32:
                raise ValueError('Public key is not valid')
            password_bytes = password.encode('utf-8')
            timestamp_bytes = vn_time.encode('utf-8')
            key = os.urandom(32)
            aes_gcm = AESGCM(key)
            encrypted_data = aes_gcm.encrypt(bytes(12), password_bytes, timestamp_bytes)
            sealed_box = SealedBox(PublicKey(public_key))
            sealed_key = sealed_box.encrypt(key)
            t = bytearray(48 + 2 + len(sealed_key) + len(encrypted_data))
            u = 0
            t[u] = 1
            u += 1
            t[u] = key_id
            u += 1
            t[u:u+2] = len(sealed_key).to_bytes(2, 'little')
            u += 2
            t[u:u+len(sealed_key)] = sealed_key
            u += len(sealed_key)
            t[u:u+16] = encrypted_data[-16:]
            u += 16
            t[u:] = encrypted_data[:-16]
            hashed_password = base64.b64encode(t).decode('utf-8')
            return f"#PWD_BROWSER:5:{vn_time}:{hashed_password}"
        except:
            return None

    def register(self, ho: str, ten: str, phone: str, password: str, callback: Optional[Callable] = None) -> bool:
        """Đăng ký tài khoản Facebook"""
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                proxy = self.proxy_manager.get_next_proxy(callback)
                if not proxy:
                    log_message("Không còn proxy khả dụng!", "error", callback)
                    return False

                if not self.proxy_manager.check_proxy(proxy, callback):
                    continue

                self.session = requests.Session()
                self.session.proxies = proxy
                headers = self.get_random_headers()

                # Lấy public key
                response_get = self.session.get(FACEBOOK_REG_URL, headers=headers)
                public_key_pattern = r'"publicKey":"([a-zA-Z0-9]+)"'
                key_id_pattern = r'"keyId":(\d+)'
                public_key_match = re.search(public_key_pattern, response_get.text)
                key_id_match = re.search(key_id_pattern, response_get.text)
                public_key_data = {
                    'publicKey': public_key_match.group(1),
                    'keyId': int(key_id_match.group(1)) 
                }

                # Mã hóa mật khẩu
                password_encrypt = self.encrypt_password(public_key_data, password)
                if not password_encrypt:
                    log_message("Đăng ký thất bại.", "error", callback)
                    retry_count += 1
                    continue

                # Lấy cookies
                cookies = response_get.cookies
                for cookie in cookies:
                    if cookie.name == 'datr':
                        datr = cookie.value
                    elif cookie.name == 'fr':
                        fr = cookie.value
                    elif cookie.name == 'sb':
                        sb = cookie.value

                # Lấy form data
                response_get = self.session.get(FACEBOOK_REG_URL, headers=headers)
                soup = BeautifulSoup(response_get.text, 'html.parser')
                hidden_inputs = soup.find_all('input', type='hidden')
                form_data = {}
                for input_field in hidden_inputs:
                   name = input_field.get('name')
                   value = input_field.get('value', '')
                   form_data[name] = value

                # Chuẩn bị data đăng ký
                data = {
                    'jazoest': form_data.get('jazoest'),
                    'lsd': form_data.get('lsd'),
                    'lastname': ho,
                    'firstname': ten, 
                    'birthday_day': str(random.randint(1, 31)),
                    'birthday_month': str(random.randint(1, 12)),
                    'birthday_year': str(random.randint(1988, 2006)),
                    'birthday_age': '',
                    'did_use_age': 'false',
                    'sex': str(random.randint(1, 2)),
                    'preferred_pronoun': '',
                    'custom_gender': '',
                    'reg_email__': phone,
                    'reg_email_confirmation__': '',
                    'reg_passwd__': password_encrypt,
                    'referrer': '',
                    'asked_to_login': '0',
                    'use_custom_gender': '',
                    'terms': 'on',
                    'ns': '0',
                    'ri': form_data.get('ri'),
                    'action_dialog_shown': '',
                    'invid': '',
                    'a': '',
                    'oi': '',
                    'locale': form_data.get('locale'),
                    'app_bundle': '',
                    'app_data': '',
                    'reg_data': '',
                    'app_id': '',
                    'fbpage_id': '',
                    'reg_oid': '',
                    'reg_instance': form_data.get('reg_instance'),
                    'openid_token': '',
                    'uo_ip': '',
                    'guid': '',
                    'key': '',
                    're': '',
                    'mid': '',
                    'fid': '',
                    'reg_dropoff_id': '',
                    'reg_dropoff_code': '',
                    'ignore': 'captcha|reg_email_confirmation__',
                    'captcha_persist_data': form_data.get('captcha_persist_data'),
                    'captcha_response': '',
                    '__user': '0',
                    '__a': '1',
                    '__req': '6',
                    '__hs': '20084.BP:DEFAULT.2.0.0.0.0',
                    'dpr': '1',
                    '__ccg': 'EXCELLENT',
                    '__rev': '1019085267',
                    '__s': 'lxucyo:t0561u:xdnp5s',
                    '__hsi': '7453027861273714271',
                    '__dyn': '7xe6EsK36Q5E5ObwKBWg5S1Dxu13wqovzEdEc8uw9-3K0lW4o3Bw5VCwjE3awdu0FE2awpUO0n24o5-0me1Fw5uwbO0KU3mwaS0zE5W08HwSyE1582ZwrU1Xo1UU3jwea',
                    '__csr': '',
                    '__spin_r': form_data.get('__spin_r'),
                    '__spin_b': 'trunk',
                    '__spin_t': form_data.get('__spin_t')
                }

                # Cập nhật headers
                headers.update({
                    'x-asbd-id': '129477',
                    'x-fb-lsd': form_data.get('lsd'),
                    'content-type': 'application/x-www-form-urlencoded',
                    'referer': FACEBOOK_REG_URL
                })

                # Gửi request đăng ký
                response_post = self.session.post(FACEBOOK_AJAX_REG_URL, headers=headers, data=data)

                if "registration_succeeded" in response_post.text:
                    json_text = response_post.text.replace("for (;;);", "")
                    response_data = json.loads(json_text)
                    if response_data["payload"].get("registration_succeeded") == True:
                        # Xác nhận email
                        ConfirmeMail = self.session.post(url=FACEBOOK_CONFIRM_URL, headers=headers)
                        match = re.search(r'"LSD",\[\],\{"token":"(.*?)"\}', ConfirmeMail.text)
                        if match:
                            lsdUpdate = match.group(1)
                        match = re.search(r'"rev":(\d+)', ConfirmeMail.text)
                        if match:
                            rev = int(match.group(1))

                        # Lấy cookies
                        cookies = response_post.cookies
                        all_cookies = []
                        for cookie in cookies:
                            all_cookies.append(f"{cookie.name}={cookie.value}")
                        cookie_string = '; '.join(all_cookies)

                        # Lấy user ID
                        start = cookie_string.find('c_user=') + 7
                        end = cookie_string.find(';', start)
                        c_user = cookie_string[start:end]

                        # Kiểm tra tài khoản
                        check_live = self.check_live_fb(c_user, proxy)
                        if check_live == 'DIE':
                            log_message("Đăng ký thất bại.", "error", callback)
                            retry_count += 1
                            continue

                        # Lưu tài khoản
                        with open(SUCCESS_FILE, 'a') as f:
                            f.write(f"{c_user}|{password}|{cookie_string}\n")
                        self.dem += 1
                        success_msg = f"[{self.dem}][{c_user}][{ho} {ten}][success.txt]"
                        log_message(success_msg, "success", callback)
                        return True
                    else:
                        log_message("Đăng ký thất bại.", "error", callback)
                        retry_count += 1
                        continue
                else:
                    log_message("Đăng ký thất bại.", "error", callback)
                    retry_count += 1
                    continue

            except Exception as e:
                log_message(f"Đăng ký thất bại: {str(e)}", "error", callback)
                retry_count += 1
                continue

        log_message("Đăng ký thất bại sau nhiều lần thử.", "error", callback)
        return False 