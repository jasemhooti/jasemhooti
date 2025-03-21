import requests
from config import XUI_PANEL_URL, XUI_PANEL_USERNAME, XUI_PANEL_PASSWORD

def login_to_xui():
    session = requests.Session()
    login_url = f"{XUI_PANEL_URL}login"  # آدرس صفحه ورود
    login_data = {
        "username": XUI_PANEL_USERNAME,
        "password": XUI_PANEL_PASSWORD
    }
    try:
        response = session.post(login_url, data=login_data)
        response.raise_for_status()  # بررسی وضعیت پاسخ HTTP
        # بررسی کنید که آیا ورود موفقیت آمیز بوده است (مثلاً با بررسی محتوای پاسخ یا کوکی‌ها)
        if "dashboard" in response.text:  # یک نشانه فرضی از ورود موفقیت آمیز
            return session
        else:
            print("خطا در ورود به پنل X-UI.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"خطا در اتصال به پنل X-UI: {e}")
        return None

def create_xui_config(session, user_identifier, package_details):
    if session:
        list_url = f"{XUI_PANEL_URL}server/list"
        try:
            response = session.get(list_url)
            response.raise_for_status()
            # در اینجا باید منطقی برای یافتن یک سرور مناسب و استفاده از آن برای ایجاد کانفیگ اضافه کنید.
            # این ممکن است شامل تجزیه پاسخ JSON یا HTML باشد.
            # به عنوان یک مثال ساده، فرض می‌کنیم اولین سرور موجود را انتخاب می‌کنیم.
            servers_data = response.json().get('data')
            if servers_data and isinstance(servers_data, list) and servers_data[0]:
                server_id = servers_data[0].get('id')
                if server_id:
                    add_url = f"{XUI_PANEL_URL}server/add"
                    add_data = {
                        "server_id": server_id,
                        "remark": f"{user_identifier}_{package_details['name']}",
                        "protocol": "vless",
                        "port": "443",
                        "uuid": "generate",
                        "security": "tls",
                        "sni": "", # بسته به نیاز
                        "allow_insecure": False,
                        "fingerprint": "chrome",
                        "listen": "",
                        "mux": False,
                        "mux_concurrency": 8,
                        "mux_stream": "grpc",
                        "mux_dial": "direct",
                        "path": "/",
                        "host": "",
                        "grpc_service_name": "",
                        "ws_path": "/",
                        "ws_host": "",
                        "allow_passive": True,
                        "tls_1_3": True,
                        "xtls_flow": "",
                        "network": "tcp"
                    }
                    add_response = session.post(add_url, json=add_data)
                    add_response.raise_for_status()
                    if add_response.json().get('success'):
                        # پس از ایجاد، باید لینک یا جزئیات کانفیگ را از پنل دریافت کنید.
                        # این ممکن است نیاز به یک درخواست دیگر به API داشته باشد.
                        # به عنوان یک راه حل موقت، یک لینک فرضی برمی‌گردانیم.
                        return f"vmess://{user_identifier}_{package_details['name']}" # لینک فرضی
                    else:
                        print(f"خطا در ایجاد کانفیگ: {add_response.json()}")
                        return None
                else:
                    print("شناسه سرور معتبر یافت نشد.")
                    return None
            else:
                print("هیچ سروری در پنل X-UI یافت نشد.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"خطا در ارتباط با پنل X-UI: {e}")
            return None
    return None
