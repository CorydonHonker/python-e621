from time import time, sleep

dl_timer = time()
header = {'user-agent': 'e6_dl-byCM/1.0.1'}


def dl_sync():
    global dl_timer
    tmp = dl_timer
    dl_timer = time()
    tmp = dl_timer - tmp
    if tmp < 0.5:
        sleep(tmp)


def get_json(api, req_obj, s):
    global header
    dl_sync()
    r = s.get(api, timeout=10, headers=header, params=req_obj)
    r.raise_for_status()
    return r.json()


def dl_file(file_path, my_url, s):
    if my_url is None or my_url == "":
        print(f'{my_url} url:', file_path)
        return False
    global header
    dl_sync()
    r = s.get(my_url, stream=True, timeout=10, headers=header)
    if r.status_code == 404:
        print("404")
    else:
        r.raise_for_status()
    with open(file_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
