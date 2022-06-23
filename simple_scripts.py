from pprint import pprint

import requests
from bs4 import BeautifulSoup
import html5lib


custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}


android_headers = {
"authority": "goo.gl",
"method": "GET",
"path": "/maps/8tmfodFCER2pWruEA",
"scheme": "https",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en,en-US;q=0.9,es-MX;q=0.8,es;q=0.7",
"dnt": "1",
"sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
"sec-ch-ua-mobile": "?1",
"sec-ch-ua-platform": "Android",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36",
}

test_url = "https://goo.gl/maps/8tmfodFCER2pWruEA"

test_response = requests.get(test_url, headers=android_headers, allow_redirects=False)
# pprint(test_response.__dict__)


loc_url = test_response.headers["location"]
# print(f"loc url: {loc_url}")
new_response = requests.get(loc_url, headers=android_headers, allow_redirects=False)
pprint(new_response.__dict__)

test_soup = BeautifulSoup(test_response.text, "html5lib")

# print(test_soup.prettify())

