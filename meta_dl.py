from basic_definitions import *
import requests


def dl_meta(api, req_obj, fun_s):
    global my_sync, meta
    p_goal = quick_fav_count(user_val, fun_s)
    p_count = 0
    time_data(t_sync=True, count_goal=p_goal)
    # sep
    oldest_id = find_oldest(api, req_obj, fun_s)
    current_id = oldest_id + 1
    while current_id > oldest_id:
        my_data = get_json(api, req_obj, fun_s)
        current_id = my_data['posts'][-1]['id']
        for i in my_data['posts']:
            p_count += 1
            for src in i['sources']:
                source_list.setdefault(src, 0)
                source_list[src] += 1
            cut_date = e6_date_cutter(i['created_at'])
            meta['dates'].setdefault(cut_date, [])
            meta['dates'][cut_date].append(i['id'])
            for tag in i['tags']['artist']:
                meta['artists'].setdefault(tag, [])
                meta['artists'][tag].append(i['id'])
            for tag in i['tags']['character']:
                meta['characters'].setdefault(tag, [])
                meta['characters'][tag].append(i['id'])
            for tag in i['tags']['copyright']:
                meta['copyright'].setdefault(tag, [])
                meta['copyright'][tag].append(i['id'])
        req_obj['page'] = 'b' + str(current_id)
        # time stuff \/
        display_info = time_data(counter=p_count)
        print(
            'dl_data',
            '| Posts', p_count, '/', p_goal,
            '| total_time:', time_format(display_info[2]),
            '| progress: %', sig_digs(100 * display_info[1]),
            '| est_time:', time_format(display_info[3])
        )
    save_file_data(user_name[user_val] + "-meta.json", meta)
    save_file_data(user_name[user_val] + "-sources.json", source_list)
    print('dl_data END')


def downloader(u):
    global user_val, post_params
    with requests.Session() as s:
        user_val = u
        post_params = {'tags': 'fav:' + user_name[user_val], 'limit': '320'}
        dl_meta(post_api, post_params, s)
