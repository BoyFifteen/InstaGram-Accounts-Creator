import requests
import uuid
import time
import random
import string
import json
class InstagramDeepLinkBot:
    def __init__(self, email):
        self.session = requests.Session()
        self.email = email
        self.username = "".join(random.choices(string.ascii_lowercase, k=11))
        self.password = "Dev_2026_Secure!"
        self.guid = str(uuid.uuid4())
        self.mid = None
        self.datr = None
    def log(self, text):
        print(f"[*] {text}")
    def get_headers(self, host="www.instagram.com", referer=None):
        csrf = self.session.cookies.get('csrftoken', '')
        headers = {
            'authority': host,
            'accept': '*/*',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': referer or 'https://www.instagram.com/accounts/emailsignup/',
            'sec-ch-ua': '"Not A(Byte<Empty) ";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'x-csrftoken': csrf,
            'x-ig-app-id': '936619743392459',
            'x-asbd-id': '129477',
            'x-ig-www-claim': '0',
            'x-requested-with': 'XMLHttpRequest'
        }
        return headers
    def prepare(self):
        self.log("Building Device Reputation...")
        r = self.session.get("https://www.instagram.com/", headers={'user-agent': 'Mozilla/5.0'})
        self.mid = self.session.cookies.get('mid')
        
    def run(self):
        self.prepare()
        url_otp = "https://www.instagram.com/api/v1/accounts/send_verify_email/"
        self.session.post(url_otp, headers=self.get_headers(), data={'device_id': self.guid, 'email': self.email})
        self.log(f"OTP sent to {self.email}")
        
        code = input("[?] Enter the code: ")
        url_verify = "https://i.instagram.com/api/v1/accounts/check_confirmation_code/"
        res_verify = self.session.post(url_verify, headers=self.get_headers(host="i.instagram.com"), 
                                     data={'code': code, 'device_id': self.guid, 'email': self.email})
        signup_token = res_verify.json().get('signup_code')
        if signup_token:
            self.log("Signup Token validated successfully.")
            time.sleep(random.randint(3, 6))
            url_final = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/"
            timestamp = int(time.time())
            data_final = {
                'enc_password': f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{self.password}",
                'email': self.email,
                'username': self.username,
                'first_name': 'Tester',
                'month': '5', 'day': '20', 'year': '1995',
                'client_id': self.mid,
                'seamless_login_enabled': '1',
                'tos_version': 'row',
                'force_sign_up_code': signup_token,
                'signup_code': signup_token 
            }
            final_headers = self.get_headers(referer="https://www.instagram.com/accounts/birthday/")
            res_final = self.session.post(url_final, headers=final_headers, data=data_final)
            return res_final.json()
        return "Failed to get signup_token"
bot = InstagramDeepLinkBot("vava27@premipay.io")
print(json.dumps(bot.run(), indent=2))
