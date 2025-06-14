import threading
import queue
import requests
import os

# Path to the proxy file
PROXY_FILE = r'C:\Users\hp\Desktop\crawler\crawler\spiders\pro.txt'

# Create a queue and a list for valid proxies
q = queue.Queue()
valid_proxies = []

# Ensure the proxy file exists, if not, scrape proxies and save to file
def ensure_proxies_file():
    if not os.path.isfile(PROXY_FILE):
        print(f"File {PROXY_FILE} not found, scraping proxies...")
        proxies = scrape_proxies()
        if proxies:
            with open(PROXY_FILE, 'w', encoding='utf-8-sig') as f:
                for proxy in proxies:
                    f.write(proxy + "\n")
        return proxies
    else:
        with open(PROXY_FILE, 'r', encoding='utf-8-sig') as f:
            return [line.strip() for line in f if line.strip()]

def scrape_proxies():
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    
    for row in soup.find('table', {'id': 'proxylisttable'}).find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) > 0:
            proxy = f"http://{columns[0].text}:{columns[1].text}"
            proxies.append(proxy)
    
    return proxies

# Ensure the proxies file is available
proxies = ensure_proxies_file()
for p in proxies:
    q.put(p)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            # Ensure the proxy format is correct
            res = requests.get("https://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=5)
            if res.status_code == 200:
                print(f"Valid proxy: {proxy}")
                valid_proxies.append(proxy)  # Store the valid proxy
        except requests.RequestException:
            # Handle exceptions and continue
            pass
        finally:
            q.task_done()

# Start 10 threads to check proxies
threads = []
for _ in range(10):
    thread = threading.Thread(target=check_proxies)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print(f"Valid proxies: {valid_proxies}")
 