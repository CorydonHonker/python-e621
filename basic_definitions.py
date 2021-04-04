from json import dumps, loads
from time import time, sleep
from gtags import gtag_dictionary
from stags import stag_dictionary
from os.path import exists
import os

meta_file_directory = "json_data"
file_type_src = '-sources.json'
file_type_meta = '-meta.json'
user_val = -1
user_name = [] # add names here
post_params = {'tags': 'fav:' + user_name[user_val], 'limit': '320'}
post_api = "https://e621.net/posts.json"
pool_api = "https://e621.net/pools.json"
pool_params = {'search[id]': ''}
header = {'user-agent': 'e6py-byCM/0.9a'}
meta = {'dates': {}, 'artists': {}, 'characters': {}, 'copyright': {}}
meta_tag = {'posts': {}, 'gtag': {}, 'stag': {}}
pool_meta_base = {'A+': 54, 'A': 48, 'B+': 42, 'B': 36, 'C+': 30, 'C': 24, 'D+': 18, 'D': 12, 'F': 6}
post_meta_base = {'A+': 87, 'A': 76, 'B+': 65, 'B': 54, 'C+': 43, 'C': 32, 'D+': 21, 'D': 10, 'F': 0}
posts = {}
pools = {}
source_list = {}
file_types = ('.png', '.jpg', '.webm', '.mp4', '.gif')
my_sync = time()
dl_timer = time()
tempo = [
    0,  # sync_difference
    0,  # % progress
    0,  # total time
    0,  # estimated remaining time
    1,  # counter
    1,  # count goal
]


# math \/

def generic_averages(my_list, out_method=None):
    if out_method == 'mean':
        return int(sum_array(my_list) / len(my_list))
    if out_method == 'median':
        my_list = sorted(my_list)
        return my_list[int(len(my_list) / 2)]
    if out_method == 'range':
        my_list = sorted(my_list)
        return my_list[-1] - my_list[0]
    if out_method == 'min_max':
        my_list = sorted(my_list)
        return [my_list[-1], my_list[0]]
    if out_method == 'sum':
        return sum_array(my_list)
    return out_method


def sum_array(my_list):
    new_sum = 0
    for x in my_list:
        new_sum += x
    return new_sum


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def sig_digs(value, post_decimal=2):
    if post_decimal < 0:
        post_decimal = 0
    digit_list = [x for x in str(value)]
    decimal = -1
    left_digit = -1
    tmp = "."
    if tmp in digit_list:
        decimal = digit_list.index(tmp)
        digit_list.pop(decimal)
        for idx in range(0, len(digit_list)):
            if not digit_list[idx] == "0":
                left_digit = idx
                break
    if decimal < left_digit:
        while digit_list[0] == "0":
            digit_list.pop(0)
    while len(digit_list) - 1 > post_decimal:
        digit_list.pop(-1)
    if decimal < left_digit:
        tmp = decimal - left_digit - 1
        digit_list.insert(1, ".")
        digit_list.append("*10^" + str(tmp))
    elif decimal > len(digit_list):
        tmp = decimal - len(digit_list)
        digit_list.append("*10^" + str(tmp))
    elif -1 < decimal < len(digit_list):
        digit_list.insert(decimal, ".")
    return ''.join(digit_list)


# tags \/


def tag_score_data(u_val, pool=False):
    file_var = "-posts.json"
    index_var = 0
    my_scores = []
    if pool:
        file_var = "-pools.json"
        index_var = 2
    json_data = get_file_data(user_name[u_val] + file_var)
    for o in json_data:
        my_scores.append(json_data[o]['path_options'][index_var])
        if pool:
            my_scores[-1] = int(my_scores[-1] / len(json_data[o]['posts_ids']))
            if my_scores[-1] > 4000:
                print(o)
    print(
        '| User:', user_name[u_val] + file_var,
        '| Mean:', generic_averages(my_scores, 'mean'),
        '| Median:', generic_averages(my_scores, 'median'),
        '| Grade Size:', int(generic_averages(my_scores, 'range') / 10),
        '| Min Max:', generic_averages(my_scores, 'min_max')
    )


def tag_scores(my_gtags, my_stags):
    tmp_sum = 0
    for x in my_gtags:
        if x in gtag_dictionary:
            tmp_sum += gtag_dictionary[x]
    for x in my_stags:
        if x in stag_dictionary:
            tmp_sum += stag_dictionary[x]
    return tmp_sum


# requests / os stuff \/


def get_file_data(file_name):
    try:
        f = open(meta_file_directory + '/' + file_name, 'r', encoding="utf8")
        tmp = loads(f.read())
        f.close()
        return tmp
    except IOError:
        print('File Not Found')
        return None


def save_file_data(file_name, my_data):
    f = open(meta_file_directory + '/' + file_name, "w", encoding="utf8")
    f.write(dumps(my_data, ensure_ascii=bool(0)))
    f.close()


def save_raw_data(file_name, my_data):
    f = open(meta_file_directory + '/' + file_name, "w", encoding="utf8")
    f.write(my_data)
    f.close()


def get_json(api, req_obj, fun_s):
    global header
    dl_sync()
    r = fun_s.get(api, timeout=10, headers=header, params=req_obj)
    r.raise_for_status()
    return r.json()


def get_html(api, fun_s):
    global header
    dl_sync()
    r = fun_s.get(api, timeout=10, headers=header)
    r.raise_for_status()
    return r.text


def find_oldest(api, req_obj, fun_s):
    req_obj['page'] = 'a1'
    my_data = get_json(api, req_obj, fun_s)
    req_obj.pop('page')
    return my_data['posts'][-1]['id']


def quick_fav_count(u, fun_s):
    users_api = 'https://e621.net/users.json'
    users_params = {'search[name_matches]': user_name[u]}
    user_info = get_json(users_api, users_params, fun_s)
    user_id = str(user_info[0]['id'])
    users_api = 'https://e621.net/users/' + user_id
    user_info = get_html(users_api, fun_s)
    string_cutter_a = '<a href="/favorites?user_id=' + user_id + '">'
    string_cutter_b = '</a>'
    user_info = user_info.splitlines()
    for line in user_info:
        if line.find(string_cutter_a) > 0:
            cut = line.split(string_cutter_a)
            cut = cut[-1].split(string_cutter_b)
            return int(cut[0])
    return 0


def os_path_correct(dir_name):
    r = '_'
    dir_name = dir_name \
        .replace('<', r) \
        .replace('>', r) \
        .replace(':', r) \
        .replace('\\', r) \
        .replace('|', r) \
        .replace('?', r) \
        .replace('*', r) \
        .replace('"', r).rstrip('.')
    return dir_name


def directory(directory_name):
    # Create directory ,it's a directory name which you are going to create.
    # Directory_Name = input("Enter the directory name ")
    # try and catch block use to handle the exceptions.
    try:
        # Create  Directory  MyDirectory
        os.makedirs(directory_name, exist_ok=True)
        # print if directory created successfully...
        print("Directory ", directory_name, " Created ")
    except FileExistsError:
        # print if directory already exists...
        print("Directory ", directory_name, " already exists...")


def dl_file(file_name, file_path, my_url, fun_s):
    global header
    dl_sync()
    r = fun_s.get(my_url, stream=True, timeout=10, headers=header)
    if r.status_code == 404:
        print("404")
    else:
        r.raise_for_status()
    with open(file_path + '/' + file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


def merge_data(users=None, post=True):
    if users is None:
        users = [0, 1]
    u_data = []
    u_name = []
    file_str = "-posts.json"
    if post:
        file_str = "-pools.json"
    for u in users:
        u_data.append(get_file_data(user_name[u] + file_str))
        u_name.append(user_name[u])
    for u_index in range(1, len(u_data)):
        u_data[0].update(u_data[u_index])
    super_name = '-'.join(u_name)
    save_file_data(super_name + file_str, u_data[0])
    return super_name


def fill_dir(my_path):
    if not exists(my_path):
        directory(my_path)


# time \/


def dl_sync():
    global dl_timer
    tmp = time() - dl_timer
    if tmp > 0.5:
        dl_timer = time()
        return 0
    sleep(tmp)
    dl_timer = time()


def time_data(t_sync=False, counter=0, count_goal=1):
    global tempo, my_sync
    if t_sync:
        tempo = [0, 0, 0, 0, counter, count_goal]
    if counter > 1:
        tempo[4] = counter
    else:
        tempo[4] += 1
    tmp = time()
    tempo[0] = tmp - my_sync
    my_sync = time()
    tempo[1] = tempo[4] / tempo[5]
    tempo[2] += tempo[0]
    tempo[3] = (1 - tempo[1]) * tempo[2] / tempo[1]
    return tempo


def time_format(seconds):
    hour = seconds // 3600
    seconds %= 3600
    minute = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hour, minute, seconds)


def e6_date_cutter(date):
    date = date.split('T')
    return date[0]


# pool stuff \/


def pool_eval_copy(copy_val):
    if copy_val > 5:
        return 'CopyWTF'
    if copy_val > 1.9:
        return 'CopyHigh'
    if copy_val > 0.8:
        return 'CopyMean'
    if copy_val > 0:
        return 'CopyLow'
    return 'OpenFree'


def pool_eval_char(char_val):
    if char_val > 9:
        return 'SeaChar'
    if char_val > 6:
        return 'CrowdChar'
    if char_val > 3:
        return 'GroupChar'
    if char_val > 0:
        return 'FewChar'
    return 'CharFree'


def pool_eval_meta(meta_val):
    if meta_val > pool_meta_base['A+']:
        return 'S'
    if meta_val > pool_meta_base['A']:
        return 'A+'
    if meta_val > pool_meta_base['B+']:
        return 'A'
    if meta_val > pool_meta_base['B']:
        return 'B+'
    if meta_val > pool_meta_base['C+']:
        return 'B'
    if meta_val > pool_meta_base['C']:
        return 'C+'
    if meta_val > pool_meta_base['D+']:
        return 'C'
    if meta_val > pool_meta_base['D']:
        return 'D+'
    if meta_val > pool_meta_base['F']:
        return 'D'
    return 'F'


def set_pool_meta(my_data):
    global pool_meta_base
    tmp_list = []
    for i in my_data:
        tmp_list.append(int(my_data[i]['path_options'][2] / len(my_data[i]['posts_ids'])))
    my_unit = int(generic_averages(tmp_list, 'range') / 10)
    my_min = generic_averages(tmp_list, 'min_max')[-1]
    # median ~ C+
    pool_meta_base = {
        'A+': my_min + my_unit * 9,
        'A': my_min + my_unit * 8,
        'B+': my_min + my_unit * 7,
        'B': my_min + my_unit * 6,
        'C+': my_min + my_unit * 5,
        'C': my_min + my_unit * 4,
        'D+': my_min + my_unit * 3,
        'D': my_min + my_unit * 2,
        'F': my_min + my_unit
    }


def pool_path_builder(p_options, pool_size):
    tmp = [
        pool_eval_meta(p_options[2] / pool_size),
        p_options[3] + ' (' + p_options[4] + ')',
        pool_eval_copy(p_options[0] / pool_size),
        pool_eval_char(p_options[1] / pool_size),
    ]
    return '/'.join(tmp)


def pool_paths(my_data):
    # json_data = get_file_data(user_name[user_val] + "-pools.json")
    # set_pool_meta(my_data)
    for i in my_data:
        my_data[i]['path_options'] = pool_path_builder(
            my_data[i]['path_options'], len(my_data[i]['posts_ids']))
    # save_file_data(user_name[user_val] + "-pools.json", my_data)
    print('pool_paths END')
    return my_data


# post stuff \/


def format_post_list(tag_list, post_id, type_key):
    global meta_tag
    for tag_str in tag_list:
        if tag_str in meta_tag[type_key]:
            meta_tag[type_key][tag_str].append(post_id)
        else:
            meta_tag[type_key][tag_str] = [post_id]


def check_post_tags(post_id, s):
    url_base = "https://e621.net/posts.json"
    my_obj = {'tags': 'id:' + str(post_id), 'limit': '1'}
    single_post = get_json(url_base, my_obj, s)
    for gtag in single_post['posts'][0]['tags']['general']:
        if gtag in gtag_dictionary:
            print(gtag, gtag_dictionary[gtag])
    for gtag in single_post['posts'][0]['tags']['species']:
        if gtag in stag_dictionary:
            print(gtag, stag_dictionary[gtag])
    print(
        tag_scores(
            single_post['posts'][0]['tags']['general'],
            single_post['posts'][0]['tags']['species']
        )
    )


def post_eval_copy(copy_val):
    if copy_val > 6:
        return 'CopyWTF'
    if copy_val > 3:
        return 'CopyHigh'
    if copy_val > 1:
        return 'CopyMean'
    if copy_val > 0:
        return 'CopyLow'
    return 'OpenFree'


def post_eval_char(char_val):
    if char_val > 9:
        return 'SeaChar'
    if char_val > 6:
        return 'CrowdChar'
    if char_val > 3:
        return 'GroupChar'
    if char_val > 0:
        return 'FewChar'
    return 'CharFree'


def post_eval_meta(meta_val):
    if meta_val > post_meta_base['A+']:
        return 'S'
    if meta_val > post_meta_base['A']:
        return 'A+'
    if meta_val > post_meta_base['B+']:
        return 'A'
    if meta_val > post_meta_base['B']:
        return 'B+'
    if meta_val > post_meta_base['C+']:
        return 'B'
    if meta_val > post_meta_base['C']:
        return 'C+'
    if meta_val > post_meta_base['D+']:
        return 'C'
    if meta_val > post_meta_base['D']:
        return 'D+'
    if meta_val > post_meta_base['F']:
        return 'D'
    return 'F'


def post_path_builder(p_options):
    tmp = [
        post_eval_meta(p_options[0]),
        p_options[4] + ' (' + p_options[3] + ')',
        post_eval_copy(p_options[2]),
        post_eval_char(p_options[1]),
        p_options[5],
        p_options[6],
    ]
    return '/'.join(tmp)


def set_post_meta(my_data):
    global post_meta_base
    tmp_list = []
    for i in my_data:
        tmp_list.append(int(my_data[i]['path_options'][0]))
    my_unit = int(generic_averages(tmp_list, 'range') / 10)
    my_min = generic_averages(tmp_list, 'min_max')[-1]
    # median ~ C+
    post_meta_base = {
        'A+': my_min + my_unit * 9,
        'A': my_min + my_unit * 8,
        'B+': my_min + my_unit * 7,
        'B': my_min + my_unit * 6,
        'C+': my_min + my_unit * 5,
        'C': my_min + my_unit * 4,
        'D+': my_min + my_unit * 3,
        'D': my_min + my_unit * 2,
        'F': my_min + my_unit
    }


def post_paths(my_data):
    # json_data = get_file_data(user_name[user_val] + "-posts.json")
    # set_post_meta(my_data)
    for i in my_data:
        my_data[i]['path_options'] = post_path_builder(my_data[i]['path_options'])
    # save_file_data(user_name[user_val] + "-posts.json", json_data)
    print('post_paths END')
    return my_data
