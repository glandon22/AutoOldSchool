import requests

s = requests.Session()
# all cookies received will be stored in the session object

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://account.runescape.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
}
step1 = s.get('https://account.jagex.com/en-GB/login/registration-start', headers=headers)
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "locale": "en-GB",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

payload = {
    "data":{
        "email":"sdfsdfsf@sdfsdfsdfsfd222.com",
        "dob":"1982-03-03T00:00:00.000Z"
    }
}
print(s.cookies)
step2 = s.post('https://account.jagex.com/login/api/registrations/regular/continue', headers=headers, data=payload)
print(step2.request.headers)
print(step2.status_code)