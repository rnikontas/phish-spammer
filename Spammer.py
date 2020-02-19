import json
import random
import string
import time
import requests
import concurrent.futures

threads = 15
amount_per_thread = 100


def random_password(length):
    base = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(base) for i in range(length))


url = "https://ibxinformatica.com.br/wp-content/plugins/image-widget/views/owa.php"

data = {'destination': 'https%3A%2F%2Fexchange.vu.lt%2Fowa%2F', 'flags': '4', 'forcedownlevel': 0,
        'username': '1234567', 'password': 'gnfdjigsdn', 'passwordText': '', 'trusted': '4', 'isUtf8': 1}

headers = {'authority': 'ibxinformatica.com.br', 'method': 'POST',
           'path': '/wp-content/plugins/image-widget/views/owa.php', 'scheme': 'https',
           'accept': 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'en-US,en;q=0.9,lt;q=0.8,vi;q=0.7,ja;q=0.6,it;q=0.5,pt;q=0.4,th;q=0.3,fr;q=0.2',
           'cache-control': 'max-age=0', 'content-length': '133', 'content-type': 'application/x-www-form-urlencoded',
           'cookie': 'cookieTest=1; logondata=acc=0&lgn=1234567; PBack=0; PrivateComputer=true',
           'dnt': '1', 'origin': 'https://ibxinformatica.com.br',
           'referer': 'https://ibxinformatica.com.br/wp-content/plugins/image-widget/views/index.htm',
           'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin',
           'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}


def spam(id):
    local_data = data
    local_headers = headers

    start = time.perf_counter()
    for i in range(amount_per_thread):
        user = random.randint(1000000, 2000000)
        password = random_password(random.randint(8, 16))
        #print('Thread ', id, ' Sending ', user, ' username and ', password, 'password.')
        local_data["username"] = user
        local_data["password"] = password
        local_headers["cookie"] = 'cookieTest=1; logondata=acc=0&lgn=' + str(user) + '; PBack=0; PrivateComputer=true'
        session = requests.Session()
        session.get(url)
        result = session.post(url, data=json.dumps(local_data), headers=local_headers)
        if result.status_code == requests.codes.ok:
            time.sleep(0.01)
            # print('All good')
        else:
            print('Thread ', id, ' failed a POST: ', result.status_code)

    end = time.perf_counter()
    print('Thread ', id, ' finished! Took ', (end - start), 's to complete')


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(spam, range(threads))
