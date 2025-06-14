import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

PROXY_FILE = r'C:\Users\hp\Desktop\crawler\crawler\spiders\pro.txt'

def load_proxies(filename):
    if not os.path.isfile(filename):
        print(f"File {filename} not found, scraping proxies...")
        proxies = scrape_proxies()
        if proxies:
            with open(filename, 'w', encoding='utf-8-sig') as f:
                for proxy in proxies:
                    f.write(proxy + "\n")
        return proxies

    with open(filename, 'r', encoding='utf-8-sig') as f:
        proxies = [line.strip() for line in f if line.strip()]

    if not proxies:
        print("No proxies found in the file.")
    
    return proxies

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

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def check_proxies(proxies):
    test_url = 'http://books.toscrape.com/'  # Target URL to fetch HTML content
    valid_proxies = []
    for proxy in proxies:
        try:
            session = requests_retry_session()
            res = session.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=10)
            if res.status_code == 200:
                valid_proxies.append(proxy)
                print(f"Proxy: {proxy}, Status code: {res.status_code}")
                break  # Exit loop once a valid proxy is found
            else:
                print(f"Proxy: {proxy}, Status code: {res.status_code}")
        except requests.RequestException as e:
            print(f"Proxy: {proxy}, Error: {e}")
    return valid_proxies

# Load proxies from file and check them
proxies = load_proxies(PROXY_FILE)
valid_proxies = check_proxies(proxies)

# Save valid proxies back to file
with open(PROXY_FILE, 'w', encoding='utf-8-sig') as f:
    for proxy in valid_proxies:
        f.write(proxy + "\n")

print("Valid proxies:")
for proxy in valid_proxies:
    print(f"Proxy: {proxy}")
