from os.path import isfile
from basic_definitions import *
import requests


# -----------------
# Session Functions \/
# -----------------


def dl_data(api, req_obj, fun_s):
    global my_sync, posts, pools
    qty_names = ["solo", "duo", "group", "unseen_character", "zero_pictured"]
    gen_names = ["male", "female", "ambiguous_gender", "andromorph", "gynomorph", "herm", "maleherm"]
    # sep
    oldest_id = find_oldest(api, req_obj, fun_s)
    current_id = oldest_id + 1
    while current_id > oldest_id:
        my_data = get_json(api, req_obj, fun_s)
        current_id = my_data['posts'][-1]['id']
        dnp = 'C-DNP'
        for i in my_data['posts']:
            qut = ""
            gen = ""
            for n in qty_names:
                try:
                    i['tags']['general'].index(n)
                    qut = qut + " " + n
                except ValueError:
                    pass
            for n in gen_names:
                try:
                    i['tags']['general'].index(n)
                    gen = gen + " " + n
                except ValueError:
                    pass
            if qut == "":
                qut = " NoQuantities"
            if gen == "":
                gen = " NoGenders"
            gen = gen.lstrip()
            qut = qut.lstrip()
            if dnp not in i['tags']['artist']:
                dnp = 'NC-P'
            # tag stuff /\
            if len(i['pools']) > 0:
                for ii in i['pools']:
                    pools[str(ii)] = {}
            posts[str(i['id'])] = {
                'file': str(i['id']) + '.' + i['file']['ext'],
                'path_options': [
                    tag_scores(i['tags']['general'], i['tags']['species']),
                    len(i['tags']['character']),
                    len(i['tags']['copyright']),
                    i['rating'], dnp,
                    qut, gen],
                'url': i['file']['url']
            }
        req_obj['page'] = 'b' + str(current_id)
        # time stuff \/
        time_difference = time() - my_sync
        my_sync = time()
        print(
            'dl_data',
            '| ID:', abs(oldest_id - current_id),
            "| Time:",  sig_digs(time_difference))
    save_file_data(user_name[user_val] + "-posts.json", posts)
    save_file_data(user_name[user_val] + "-pools.json", pools)
    print('dl_data END')


def dl_pool_index(api, req_obj, fun_s):
    global pools
    json_data = get_file_data(user_name[user_val] + "-pools.json")
    # data get
    chunk_array = list(json_data.keys())
    chunk_array = list(chunks(chunk_array, 75))
    time_data(t_sync=True, count_goal=len(chunk_array))
    for xx in chunk_array:
        req_obj['search[id]'] = ','.join(xx)
        my_data = get_json(api, req_obj, fun_s)
        for ix in my_data:
            json_data[str(ix['id'])]['name'] = ix['name']
            json_data[str(ix['id'])]['posts_ids'] = {}
            for iix in range(0, len(ix['post_ids'])):
                json_data[str(ix['id'])]['posts_ids'][str(ix['post_ids'][iix])] = {
                    'index': iix, 'url': 'blank'}
        # time stuff \/
        display_info = time_data()
        print(
            'dl_pool_index',
            '| total_time:', time_format(display_info[2]),
            '| progress: %', sig_digs(100 * display_info[1]),
            '| est_time:', time_format(display_info[3])
        )
    save_file_data(user_name[user_val] + "-pools.json", json_data)
    print('dl_pool_index END')


def dl_pool_data(api, req_obj, fun_s):
    global pools
    json_data = get_file_data(user_name[user_val] + "-pools.json")
    time_data(t_sync=True, count_goal=len(json_data))
    for xx in json_data:
        copy_per = 0
        char_per = 0
        pool_score = 0
        c_dnp = 'NC-P'
        rating = 's'
        # meta /\
        req_obj['tags'] = 'pool:' + xx
        my_data = get_json(api, req_obj, fun_s)
        for i in my_data['posts']:
            json_data[xx]['posts_ids'][str(i['id'])]['url'] = i['file']['url']
            json_data[xx]['posts_ids'][str(i['id'])]['ext'] = i['file']['ext']
            # meta \/
            pool_score += tag_scores(i['tags']['general'], i['tags']['species'])
            copy_per += len(i['tags']['copyright'])
            char_per += len(i['tags']['character'])
            if 'conditional_dnp' in i['tags']['artist']:
                c_dnp = 'C-DNP'
            if not i['rating'] == 's':
                if not rating == 'e':
                    rating = i['rating']
        json_data[xx]['path_options'] = [
            copy_per,
            char_per,
            pool_score,
            c_dnp,
            rating
        ]
        # time shit \/
        display_info = time_data()
        print(
            'dl_pool_data',
            '| total_time:', time_format(display_info[2]),
            '| progress: %', sig_digs(100 * display_info[1]),
            '| est_time:', time_format(display_info[3]))
    save_file_data(user_name[user_val] + "-pools.json", json_data)
    print('dl_pool_data END')


def dl_pool_files(fun_s):
    dl_folder = '[dl_pools]/'
    json_data = get_file_data(user_name[user_val] + "-pools.json")
    json_data = pool_paths(json_data)
    time_data(t_sync=True, count_goal=len(json_data))
    for x in json_data:
        for ix in json_data[x]['posts_ids']:
            if json_data[x]['posts_ids'][ix]['url'] != 'blank':
                dl_url = json_data[x]['posts_ids'][ix]['url']
                my_path = (
                        dl_folder
                        + json_data[x]['path_options'] + '/' +
                        json_data[x]['name']
                )
                my_path = os_path_correct(my_path)
                my_file_name = (
                        str(json_data[x]['posts_ids'][ix]['index']) +
                        '-' + ix + '.' +
                        json_data[x]['posts_ids'][ix]['ext']
                )
                if not (isfile(my_path + '/' + my_file_name)) and dl_url is not None:
                    fill_dir(my_path)
                    dl_file(my_file_name, my_path, dl_url, fun_s)
        display_info = time_data()
        print(
            'dl_pool_files',
            '| total_time:', time_format(display_info[2]),
            '| progress: %', sig_digs(100 * display_info[1]),
            '| est_time:', time_format(display_info[3]))
    print('dl_pool_files END')


def dl_post_files(fun_s):
    dl_folder = '[dl_posts]/'
    json_data = get_file_data(user_name[user_val] + "-posts.json")
    tag_score_data(user_val, pool=False)
    json_data = post_paths(json_data)
    time_data(t_sync=True, count_goal=len(json_data))
    for x in json_data:
        if json_data[x]['url'] is not None:
            dl_url = json_data[x]['url']
            my_path = (
                    dl_folder +
                    json_data[x]['path_options']
            )
            my_file_name = json_data[x]['file']
            if not (isfile(my_path + '/' + my_file_name)):
                fill_dir(my_path)
                dl_file(my_file_name, my_path, dl_url, fun_s)
        display_info = time_data()
        print(
            'dl_post_files',
            '| total_time:', time_format(display_info[2]),
            '| progress: %', sig_digs(100 * display_info[1]),
            '| est_time:', time_format(display_info[3]))
    print('dl_post_files END')


# final function

def dl_manager(
        users=None,
        new_session=False, get_data=True,
        dl_pools=False, dl_posts=True,
        get_pools=False, get_posts=True):
    if users is None:
        users = [0, 1]
    global user_val, post_params
    user_val = users[0]
    with requests.Session() as s:
        if new_session:
            for u in users:
                user_val = u
                post_params = {'tags': 'fav:' + user_name[user_val], 'limit': '320'}
                print('Begin: ' + user_name[user_val] + "'s Session")
                # session \/
                if get_data:
                    dl_data(post_api, post_params, s)
                if get_pools:
                    dl_pool_index(pool_api, pool_params, s)
                    dl_pool_data(post_api, pool_params, s)
        if len(users) > 1:
            if get_pools:
                user_name.append(merge_data(users, False))
            if get_posts:
                user_name.append(merge_data(users))
            user_val = -1
            tag_score_data(-1, pool=False)
            tag_score_data(-1, pool=True)
        if dl_pools:
            # pool_paths()
            dl_pool_files(s)
        if dl_posts:
            # post_paths()
            dl_post_files(s)


dl_manager(
    users=None,
    new_session=False, get_data=True,
    dl_pools=False, dl_posts=True,
    get_pools=True, get_posts=True)
post_test = False
if post_test:
    with requests.Session() as s2:
        check_post_tags(1451637, s2)
        print("_______")
        check_post_tags(2572913, s2)
    tag_score_data(0, pool=False)
    tag_score_data(0, pool=True)
