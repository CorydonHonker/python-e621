# Post Data ex: {url, filename, dir}
from os import remove
from os.path import isfile, exists

import requests

from my_IO import relocate, directory, save_txt_file, save_json_file, open_json_file, chunks
from my_net import dl_file, get_json
from tags_pathing import set_download_path


def check_css():
    css_path = "downloads/Stories/main.css"
    if not isfile(css_path):
        my_css = "img{width:90%;}body{font-size:150%;}" \
                 "body{background-color:#1f3c67;color:white}.center{text-align: center;}" \
                 ".full_bar{text-align: center;width:100%;}td {width:120px}button{width:100%}" \
                 "table{width:100%;}button{height:30px;background-color:darkblue;color:white;}"
        save_txt_file(css_path, my_css)


def dtext_to_span(dtext):  # formats dtext to html <span>
    # translation begin \/
    dtext = dtext.replace('[b]', '<b>').replace('[/b]', '</b>').replace('\n', '<br>').replace('[i]', '<i>'). \
        replace('[/i]', '</i>').replace('[u]', '<u>').replace('[/u]', '</u>').replace('[s]', '<s>'). \
        replace('[/s]', '</s>').replace('[sup]', '<sup>').replace('[/sup]', '</sup>').replace('[sub]', '<sub>'). \
        replace('[/sub]', '</sub>').replace('[spoiler]', '<span class="spoiler">').replace('[/spoiler]', '</span>'). \
        replace('[/color]', '</span>').replace('[quote]', '<span class="quote">"').replace('[/quote]', '</span>'). \
        replace('[code]', '<span class="code">').replace('[/code]', '</span>'). \
        replace('[section]', '<span class="section">').replace('[/section]', '</span>').replace('\"', '"')
    d_list = dtext.split('[color=')  # dealing with color
    if len(d_list) != 1:
        for i in range(1, len(d_list)):
            tmp = d_list[i]
            tmp = tmp.split(']', 1)  # [color, text]
            if len(tmp) == 1:
                continue
            d_list[i] = f'<span style="color:{tmp[0]};">{tmp[1]}'
    dtext = "".join(d_list)
    for level in range(1, 7):  # dealing with headings
        d_list = dtext.split(f'h{level}.')
        if len(d_list) != 1:
            for i in range(1, len(d_list)):
                tmp = d_list[i]
                tmp = tmp.split('<br>', 1)  # [header, text]
                if len(tmp) == 1:
                    continue
                d_list[i] = f'<h{level}>{tmp[0]}</h{level}><br>{tmp[1]}'
        dtext = "".join(d_list)
    d_list = dtext.split('[section')  # dealing with sections
    if len(d_list) != 1:
        for i in range(1, len(d_list)):
            s_type = 'section'
            tmp = d_list[i]
            tmp = tmp.split(']', 1)  # [section data, text]
            if len(tmp) == 1:
                continue
            if tmp[0].find('expanded') != -1:
                s_type = 'section_expanded'
            if tmp[0].find('=') == -1:
                tmp[0] = str()
            else:
                tmp[0] = tmp[0].split('=')[1]
            d_list[i] = f'<span class="{s_type}"><h4>{tmp[0]}</h4><br>{tmp[1]}'
    # End of dtext formatting
    return "".join(d_list)  # sandwich with nav and image


def dtext_series_to_html(dtext_dict):  # expects {file_name: dtext, ...}
    def full_span(dtext_span, img):
        span_head = f'<span id="{img}" class="center"><img src="{img}" alt="{img}"><br>'
        span_tail = '</span>'
        return f'{span_head}{dtext_span}{span_tail}'

    span_group = ''
    separator = '","'
    head_a = '<!DOCTYPE html><head><meta charset="UTF-8"></head>'
    my_css = '<style type="text/css">img{width:90%;}body{font-size:150%;}' \
             'body{background-color:#1f3c67;color:white}.center{text-align: center;}' \
             '.full_bar{text-align: center;width:100%;}td {width:120px}button{width:100%}' \
             'table{width:100%;}button{height:30px;background-color:darkblue;color:white;}</style>'
    head_b = '<html><body>'
    nav_html = '<p class="center"><table><tr><td><button onclick="next(-1)">Left</button></td>' \
               '<td><button onclick="next(1)">Right</button></td></tr></table></p>'
    nav_script = f'<script type="text/javascript">const page_ids = ["{separator.join(dtext_dict)}"];' \
                 'var pos = 0;for(var i = 1;i<page_ids.length;i++){' \
                 'document.getElementById(page_ids[i]).style.visibility = "hidden";};function next(dir=0){' \
                 'document.getElementById(page_ids[pos]).style.visibility = "hidden";' \
                 'pos = (page_ids.length + pos + dir) % page_ids.length;' \
                 'document.getElementById(page_ids[pos]).style.visibility = "visible";};</script>'
    tail = '</body></html>'
    if len(dtext_dict) == 1:  # true if no neighbors
        for file_name, dtext in dtext_dict.items():  # add header and return html
            return f'{head_a}{my_css}{head_b}{full_span(dtext_to_span(dtext), file_name)}{tail}'
    for file_name, dtext in dtext_dict.items():
        span_group += full_span(dtext_to_span(dtext), file_name)
    # add header and return html
    return f'{head_a}{my_css}{head_b}{nav_html}{span_group}{nav_script}{tail}'


class Post:
    story = str()

    def __init__(self, post_data, deserialize=False):
        if deserialize:
            self.old_path = post_data['old_path']
            self.id = post_data['id']
            self.url = post_data['url']
            self.tags = set(post_data['tags'])
            self.rating = post_data['rating']
            self.chars_b = post_data['chars']
            self.pools_b = post_data['pools']
            self.copy_b = post_data['copies']
            self.size = post_data['size']
            self.story = post_data['story']
            self.family = set(post_data['family'])
            self.ext = post_data['ext']
            self.fam_b = len(self.family) != 1
        else:
            self.old_path = None
            self.id = post_data['id']
            self.ext = post_data['file']['ext']
            self.url = post_data['file']['url']
            self.tags = set(post_data['tags']['general'] + post_data['tags']['species'] +
                            post_data['tags']['meta'] + post_data['tags']['artist'])
            self.rating = post_data['rating']
            self.pools_b = len(post_data['pools']) != 0  # if post is managed by pools
            self.chars_b = len(post_data['tags']['character']) != 0  # set to str later
            self.copy_b = len(post_data['tags']['copyright']) != 0  # set to str later
            self.size = post_data['file']['size']  # size in bytes
            # \/ Complex data \/
            self.family = set([post_data['id']] + post_data['relationships']['children'])
            if post_data['relationships']['parent_id'] is not None:  # avoids adding None to set
                self.family.add(post_data['relationships']['parent_id'])
            self.fam_b = len(self.family) != 1  # has family members other than itself
            if 'story_in_description' in self.tags:
                self.story = post_data['description']

    def serialize(self):
        return {
            'old_path': self.old_path,
            'id': self.id,
            'ext': self.ext,
            'url': self.url,
            'tags': list(self.tags),
            'rating': self.rating,
            'chars': self.chars_b,
            'pools': self.pools_b,
            'copies': self.copy_b,
            'size': self.size,
            'story': self.story,
            'family': list(self.family),
        }

    def adopted(self):  # remove any downloaded instance when managed by family
        file_path = f'{self.old_path}{self.id}.{self.ext}'
        story_path = f'{self.old_path}{self.id}.html'
        if isfile(file_path):
            print(f'adopted {file_path}')
            remove(file_path)
        if isfile(story_path):
            print(f'adopted {story_path}')
            remove(story_path)

    def get_dl_dir(self):
        return set_download_path(rating=self.rating, copy=self.copy_b, p_type='post',
                                 char=self.chars_b, ext=self.ext, tags=self.tags)

    def save_story(self, story_path=''):
        if not exists(story_path):  # check directory
            directory(story_path)  # make directory
        save_txt_file(f"{story_path}{self.id}.html", dtext_series_to_html({f'{self.id}.{self.ext}': self.story}))

    def download(self, s):
        new_path = self.get_dl_dir()
        if self.old_path is None:  # old_path default is None
            self.old_path = new_path
        if new_path != self.old_path:
            if exists(self.old_path):  # check for directory
                new_file_path = f'{new_path}{self.id}.{self.ext}'
                old_file_path = f'{self.old_path}{self.id}.{self.ext}'
                if isfile(old_file_path):  # check if already downloaded
                    relocate(old_path=old_file_path, new_path=new_file_path)
        # story stuff
        if len(self.story) > 0:  # Story stuff
            new_html_path = f'{new_path}{self.id}.html'
            old_html_path = f'{self.old_path}{self.id}.html'
            if new_html_path != old_html_path:
                if isfile(old_html_path):  # check if old file exists
                    # move to avoid deleting and instead override
                    relocate(old_path=old_html_path, new_path=new_html_path)
            self.save_story(new_path)
        # downloading start
        self.old_path = new_path
        file_path = f'{self.old_path}{self.id}.{self.ext}'
        if not isfile(file_path):  # check if already downloaded
            if not exists(self.old_path):  # dir check
                directory(self.old_path)  # makes directory
            dl_file(file_path=file_path, my_url=self.url, s=s)  # download file


class Pool:
    def __init__(self, pool_data, deserialize=False):
        if deserialize:
            self.id = pool_data['id']
            self.name = pool_data['name']
            self.rating = pool_data['rating']
            self.char = pool_data['char']
            self.copy = pool_data['copy']
            self.tags = set(pool_data['tags'])
            self.old_path = pool_data['old_path']
            self.size = pool_data['size']
            self.posts = dict()
            for post_id, post_data in pool_data['posts'].items():
                self.posts.setdefault(post_id, self.PoolPost(post_data, deserialize=True))
        else:  # raw e621 pool json
            self.old_path = None
            self.id = pool_data['id']
            self.name = pool_data['name']
            self.rating = 's'
            self.char = False
            self.copy = False
            self.size = 0
            self.tags = set()
            self.posts = dict()
            for post_id in pool_data['post_ids']:
                self.posts.setdefault(post_id, self.PoolPost(post_id, temp=True))

    def serialize(self):
        serial_posts = dict()
        for post_id in self.posts:
            serial_posts.setdefault(post_id, self.posts[post_id].serialize())
        return {
            'id': self.id,
            'name': self.name,
            'tags': list(self.tags),
            'rating': self.rating,
            'copy': self.copy,
            'char': self.char,
            'old_path': self.old_path,
            'size': self.size,
            'posts': serial_posts,
        }

    class PoolPost:
        story = str()

        def __init__(self, post_data, temp=False, deserialize=False):
            if deserialize:  # from custom json
                self.id = post_data['id']
                self.ext = post_data['ext']
                self.url = post_data['url']
                self.size = post_data['size']
                self.story = post_data['story']
            else:  # from raw e621 json
                if temp:  # for when getting pool name
                    self.id = post_data
                    self.ext = str()
                    self.url = str()
                    self.size = 0
                else:
                    self.id = post_data['id']
                    self.ext = post_data['file']['ext']
                    self.url = post_data['file']['url']
                    self.size = post_data['file']['size']
                    tmp_tags = set(post_data['tags']['general'] + post_data['tags']['species'] +
                                   post_data['tags']['meta'] + post_data['tags']['artist'])
                    if 'story_in_description' in tmp_tags:
                        self.story = post_data['description']

        def serialize(self):
            return {
                'id': self.id,
                'ext': self.ext,
                'url': self.url,
                'size': self.size,
                'story': self.story,
            }

    def rating_check(self, new_rating):
        if self.rating != 'e':
            if new_rating != 's':
                self.rating = new_rating

    def char_check(self, new_char):
        if not self.char:  # if no Char (default)
            if len(new_char) > 0:
                self.char = True

    def copy_check(self, new_copy):
        if not self.char:  # if no Char (default)
            if len(new_copy) > 0:
                self.char = True

    def add_post(self, post_data):  # raw e621 post json
        self.posts[post_data['id']] = self.PoolPost(post_data)
        self.size += post_data['file']['size']
        self.tags.update(post_data['tags']['general'] + post_data['tags']['species'] +
                         post_data['tags']['meta'] + post_data['tags']['artist'])
        self.char_check(post_data['tags']['character'])
        self.copy_check(post_data['tags']['copyright'])
        self.rating_check(post_data['rating'])

    def pathing(self):  # run at file downloads
        return set_download_path(rating=self.rating, copy=self.copy, p_type='pool',
                                 char=self.char, ext=None, tags=self.tags, name=self.name)

    def save_stories(self, story_path=None):
        if story_path is None:
            return print("Story path is None")
        story_dict = dict()
        for post_id, post_data in self.posts.items():
            if len(post_data.story) > 0:
                story_dict.setdefault(f'{post_id}.{post_data.ext}', post_data.story)
        if len(story_dict) > 0:
            if not exists(story_path):  # check directory
                directory(story_path)  # make directory
            save_txt_file(f'{story_path}stories.html', dtext_series_to_html(dtext_dict=story_dict))

    def download(self, s):
        new_dir_path = self.pathing()  # generate pathing
        if self.old_path is None:
            self.old_path = new_dir_path
        if new_dir_path != self.old_path:  # move file/dir
            if exists(self.old_path):  # check for directory
                relocate(old_path=self.old_path, new_path=new_dir_path)
            self.old_path = new_dir_path
        self.save_stories(story_path=new_dir_path)
        # post relocate stuff ## downloads/story/id.html links to file path/ sorted by path in story_main.html
        if len(self.posts) != 0 and new_dir_path != "":  # false if missing data
            for post_id in self.posts:
                file_path = f'{new_dir_path}{post_id}.{self.posts[post_id].ext}'
                if not isfile(file_path):  # check if already downloaded
                    if not exists(new_dir_path):  # check directory
                        directory(new_dir_path)  # make directory
                    dl_file(file_path=file_path, my_url=self.posts[post_id].url, s=s)


class Family:
    def __init__(self, family_data=None, deserialize=False):
        self.old_path = None
        self.posts = dict()
        self.size = 0
        self.tags = set()
        self.char = False
        self.copy = False
        self.ext = 'jpg'  # for checking against animated ext
        self.ids = set(family_data)  # for tracking posts which are not stored
        self.rating = 's'
        if deserialize:
            self.ids = set(family_data['ids'])
            self.rating = family_data['rating']
            self.char = family_data['char']
            self.copy = family_data['copy']
            self.ext = family_data['ext']
            self.old_path = family_data['old_path']
            self.size = family_data['size']
            self.tags = set(family_data['tags'])
            self.posts = dict()
            for post_id, post_data in family_data['posts'].items():
                self.posts.setdefault(post_id, self.FamPost(post_data, deserialize=True))

    def serialize(self):
        serial_posts = dict()
        for post_id, post_data in self.posts.items():
            serial_posts.setdefault(post_id, post_data.serialize())
        return {
            'ids': list(self.posts.keys()),
            'rating': self.rating,
            'char': self.char,
            'copy': self.copy,
            'ext': self.ext,
            'old_path': self.old_path,
            'size': self.size,
            'tags': list(self.tags),
            'posts': serial_posts,
        }

    class FamPost:
        def __init__(self, post_data, deserialize=False):
            if deserialize:
                self.id = post_data['id']
                self.ext = post_data['ext']
                self.url = post_data['url']
                self.size = post_data['size']
                self.story = post_data['story']
            else:  # adopt from Post
                self.id = post_data.id
                self.ext = post_data.ext
                self.url = post_data.url
                self.size = post_data.size
                self.story = post_data.story

        def serialize(self):
            return {
                'id': self.id,
                'ext': self.ext,
                'url': self.url,
                'size': self.size,
                'story': self.story,
            }

    def ext_check(self, new_ext):  # check if not png or jpg
        if new_ext != 'jpg' and new_ext != 'png':
            self.ext = new_ext

    def rating_check(self, new_rating):
        if self.rating != 'e':
            if new_rating != 's':
                self.rating = new_rating

    def char_check(self, new_char):
        if not self.char:  # if no Char (default)
            if new_char:
                self.char = True

    def copy_check(self, new_copy):
        if not self.char:  # if no Char (default)
            if new_copy:
                self.char = True

    def adopt(self, post_data):  # need to check if Post has a download and delete it
        self.posts.setdefault(post_data.id, self.FamPost(post_data))
        self.size += post_data.size
        self.tags.update(post_data.tags)
        self.char_check(post_data.chars_b)
        self.copy_check(post_data.copy_b)
        self.rating_check(post_data.rating)

    def get_new_path(self):
        head_id = list(self.posts)
        head_id.sort(key=int)
        head_id = head_id[0]  # lowest ID is highest parent in family tree
        return set_download_path(rating=self.rating, copy=self.copy, p_type='family',
                                 char=self.char, ext=self.ext, tags=self.tags, name=head_id)

    def save_stories(self, story_path=None):
        if story_path is None:
            return print("Story path is None")
        story_dict = dict()
        for post_id, post_data in self.posts.items():
            if len(post_data.story) > 0:
                story_dict.setdefault(f'{post_id}.{post_data.ext}', post_data.story)
        if len(story_dict) > 0:
            if not exists(story_path):  # check directory
                directory(story_path)  # make directory
            save_txt_file(f'{story_path}stories.html', dtext_series_to_html(dtext_dict=story_dict))

    def download(self, s):  # possible duplicate, if Post becomes family, delete old Post file in Adopt!
        new_dir_path = self.get_new_path()  # generate pathing
        if self.old_path is None:
            self.old_path = new_dir_path
        if new_dir_path != self.old_path:  # move file/dir
            if exists(self.old_path):  # check for directory
                relocate(old_path=self.old_path, new_path=new_dir_path)
            self.old_path = new_dir_path
        self.save_stories(story_path=new_dir_path)
        # post relocate stuff ## downloads/story/id.html links to file path/ sorted by path in story_main.html
        if len(self.posts) != 0 and new_dir_path != "":  # false if missing data
            for post_id in self.posts:
                file_path = f'{new_dir_path}{post_id}.{self.posts[post_id].ext}'
                if not isfile(file_path):  # check if already downloaded
                    if not exists(new_dir_path):  # check directory
                        directory(new_dir_path)  # make directory
                    dl_file(file_path=file_path, my_url=self.posts[post_id].url, s=s)


class GroupManager:
    config = "config"
    post_save_path = f"{config}/posts.json"
    pool_save_path = f"{config}/pools.json"
    fam_save_path = f"{config}/families.json"

    def __init__(self):
        self.posts = dict()
        self.pools = dict()
        self.pool_ids = set()
        self.families = list()  # fix list saving
        self.fam_ids = list()  # list of id set
        directory(self.config)

    class Metrics:
        pass  # do after download loops are finished

    def save_posts(self):
        config_json = dict()
        for post_id, post in self.posts.items():
            config_json.setdefault(post_id, post.serialize())
        save_json_file(self.post_save_path, config_json)
        print(f"{len(config_json)} Posts Saved....")

    def save_pools(self):  # exports custom POOL json
        config_json = dict()
        for pool_id, pool in self.pools.items():
            config_json.setdefault(pool_id, pool.serialize())
        save_json_file(self.pool_save_path, config_json)
        print(f"{len(config_json)} Pools Saved....")

    def save_families(self):  # exports custom FAMILY json
        config_json = list()
        for family in self.families:  # families don't have IDs
            config_json.append(family.serialize())
        save_json_file(self.fam_save_path, config_json)
        print(f"{len(config_json)} Families Saved....")

    def load_posts(self):  # loads custom POST json
        config_json = open_json_file(self.post_save_path)  # returns json dict
        if config_json is not None:
            for post_id in config_json:
                self.posts.setdefault(int(post_id), Post(config_json[post_id], deserialize=True))
        print(f"{len(self.posts)} Posts Loaded....")

    def load_pools(self):  # loads custom POOL json
        config_json = open_json_file(self.pool_save_path)  # returns json dict
        if config_json is not None:
            for pool_id in config_json:
                self.pools.setdefault(int(pool_id), Pool(config_json[pool_id], deserialize=True))
        print(f"{len(self.pools)} Pools Loaded....")

    def check_family(self, family_data):
        for family in self.families:
            if not family.ids.intersection(set(family_data['ids'])) == set():  # if not empty setcustom
                return False  # already exists
        return True  # append new family

    def load_families(self):  # loads custom FAMILY json
        # self.families = list()  # need function to clear/merge duplicates
        config_json = open_json_file(self.fam_save_path)  # returns json list
        if config_json is not None:
            for family_data in config_json:
                if self.check_family(family_data=family_data):
                    self.families.append(Family(family_data, deserialize=True))
        print(f"{len(self.families)} Families Loaded....")

    def add_post(self, post_data):  # adds post to post, pool, and family lists
        if post_data['file']['url'] is not None:  # catches default blacklist and misc errors
            self.posts[post_data['id']] = Post(post_data)  # overrides existing data for post id if it exists
            # pools \/
            if len(post_data['pools']) > 0:  # True if post has pools
                self.pool_ids.update(post_data['pools'])

    def post_search(self, search_str, new_only=True):
        print('Start of post search...')
        self.load_posts()
        post_api = "https://e621.net/posts.json"  # API shit
        search_params = {'tags': search_str, 'limit': '320', 'page': 1}
        result_count = 320
        with requests.Session() as s:
            while result_count != 0 and search_params['page'] < 750:
                print(f'post page: {search_params["page"]}')  # debug
                result_data = get_json(post_api, search_params, s)  # returns e621 json
                result_count = len(result_data['posts'])  # checks how many posts in result
                for post in result_data['posts']:
                    self.add_post(post)  # adds post to Post list
                search_params['page'] += 1  # iterates page number
        self.save_posts()  # save posts to custom json
        # pool stuff \/
        self.load_pools()
        if new_only:  # only gets new pools and ignores old ones
            if len(self.pool_ids) != 0 and len(self.pools) != 0:
                self.pool_ids.difference_update(set(self.pools.keys()))
        pool_api = "https://e621.net/pools.json"
        chunk_list = list(chunks(list(self.pool_ids), 70))  # limit is ~70 for e621
        print(f'Chunked {len(self.pool_ids)} pools...')  # debug
        pool_params = {'search[id]': "", 'limit': '320'}
        with requests.Session() as s:
            for id_list in chunk_list:
                pool_params['search[id]'] = ""
                pool_params['search[id]'] = ",".join(map(str, id_list))  # stringify pool ids
                my_data = get_json(pool_api, pool_params, s)  # returns e621 json
                for pool in my_data:
                    self.pools[pool['id']] = Pool(pool)  # overrides/adds pool in pool dict; No posts yet
        self.save_pools()
        # now get pool posts
        search_params = {'tags': '', 'limit': '320', 'page': 1}
        post_api = "https://e621.net/posts.json"  # API shit
        with requests.Session() as s:
            for update_count, pool_id in enumerate(self.pools):
                if new_only:
                    if self.pools[pool_id].size != 0:
                        continue
                print(f'Pool progress: {update_count}/{len(self.pools)}')
                search_params['page'] = 1
                search_params['tags'] = f'pool:{pool_id}'
                result_count = 320
                while result_count != 0 and search_params['page'] != 750:
                    my_data = get_json(post_api, search_params, s)  # returns e621 json
                    result_count = len(my_data['posts'])  # checks if page is empty
                    for post in my_data['posts']:
                        self.pools[pool_id].add_post(post)  # add posts to pool
                    search_params['page'] += 1  # iterates to next page
                if update_count % 100 == 0:  # for shitty internet
                    self.save_pools()  # save pool to custom json
        self.save_pools()  # save pool to custom json
        print('End of post search...')

    def family_search(self):  # fix this shit!!!
        print('Begin family search')
        self.load_families()
        self.load_posts()
        if len(self.posts) == 0:
            return print('No posts to search through...')
        # loop through posts, exclude those in pools, use self.fam_ids to collect families
        # once done, add posts to family except for families of length 1
        for post_id, post in self.posts.items():  # loops through all posts
            if not post.pools_b and post.fam_b:  # true if not in pool and has family != 1
                for full_fam in self.families:  # checking for preexisting families
                    if not full_fam.ids.intersection(post.family) == set():
                        full_fam.ids.update(post.family)
                        full_fam.adopt(post)
                        post.adopted()
                        break  # next post | skips adding to fam_ids
                else:  # no break
                    for fam_group in self.fam_ids:  # check if id from post.family exists in family from self.fam_ids
                        if not fam_group.intersection(post.family) == set():  # if not empty set
                            fam_group.update(post.family)
                            break  # next post
                    else:  # run if no break
                        self.fam_ids.append(post.family)
        print(self.fam_ids)
        for fam_group in self.fam_ids:
            new_family = Family(family_data=fam_group)
            for post_id in fam_group:
                if post_id in self.posts:  # need to check for single adoptions | one Post families
                    new_family.adopt(self.posts[post_id])
                    self.posts[post_id].adopted()
            self.families.append(new_family)
        self.save_families()
        print('end family search')

    def download(self):
        self.load_posts()
        with requests.Session() as s:
            # remove Posts managed by other groups
            pop_list = set()
            for post_id, post in self.posts.items():
                if post.pools_b or post.fam_b:  # in pool or family != 1
                    pop_list.add(post_id)
            for post_id in pop_list:
                self.posts.pop(post_id)
            # begin post downloads
            for idx, (post_id, post) in enumerate(self.posts.items()):
                print(f'Posts: {idx}/{len(self.posts)} | {post_id}')
                post.download(s=s)
            print('Finished Post downloads...')
            self.load_pools()
            for idx, (pool_id, pool) in enumerate(self.pools.items()):
                print(f'Pools: {idx}/{len(self.pools)} | {pool.name}')
                pool.download(s=s)
            print('Finished Pools downloads...')
            self.load_families()
            for idx, family in enumerate(self.families):
                print(f'Families: {idx}/{len(self.families)} | {len(family.ids)}')
                family.download(s=s)
            # add saves
            print('Finished Families downloads....')
