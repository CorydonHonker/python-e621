# storing posts, pools, families # stories, path history
from os.path import exists, isfile

import requests

from my_IO import chunks, save_json_file, open_json_file, directory, relocate, save_txt_file
from my_net import get_json, dl_file
from tags_pathing import set_download_path


def main_css():
    my_css = "img {width: 90%;}body {font-size: 150%;}"
    save_txt_file("downloads/Stories/main.css", my_css)


def dtext_to_body(dtext, file_name=None):
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
    dtext = "".join(d_list)
    # head and body
    nav_bar = f'<p class="center">Nav</p>'
    css_style = '<style type="text/css">' \
                'img{width:90%;}body{font-size:150%;}' \
                'body{background-color:#1f3c67;color:white}.center{text-align:center;}' \
                '.full_bar{text-align: center;width:100%;}td{width:120px}button{width:100%}' \
                '</style>'
    head = f'<!DOCTYPE html><head><meta charset="UTF-8"></head>{css_style}' \
           f'<html><body><p class="center">{file_name}</p><br>'
    tail = '</body></html>'
    if file_name is not None:  # add image if path exists
        head += f'<p class="center"><img src="{file_name}" alt="{file_name}"></p><br>'
    return f'{head}{dtext}{tail}'


def dtext_to_html(dtext, img=None):
    def disable_button(path):
        if path is None:
            return 'disabled'
        return ''
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
    dtext = "".join(d_list)
    # head and body
    css_style = ""
    head = '<!DOCTYPE html><head><meta charset="UTF-8"></head><link rel="stylesheet" type="text/css" href="main.css"/>' \
           '<style type="text/css">body{background-color:#1f3c67;color:white}.center{text-align: center;}' \
           '.full_bar{text-align: center;width:100%;}td {width:120px}button{width:100%}</style>' \
           '<html><body><p class="center"><a href="../index.html">Back to Main</a></p><br>'
    tail = '</body></html>'
    if img is not None:  # add image if path exists
        img = img.replace("downloads", "..")
        head += f'<p class="center"><img src="{img}" alt="{img}"></p><br>'
    return f'{head}{dtext}{tail}'


class Post:
    def __init__(self, post_data, custom=False):
        self.new_path = str()
        self.old_path = str()
        if custom:  # from custom json
            self.id = post_data['id']
            self.ext = post_data['ext']
            self.url = post_data['url']
            self.tags = set(post_data['tags'])
            self.rating = post_data['rating']
            self.chars = post_data['chars']
            self.pools = post_data['pools']
            self.copy = post_data['copies']
            self.size = post_data['size']
            # removed pathing to be generated when needed
            self.old_path = post_data['old_path']
            self.story = post_data['story']
            self.family = post_data['family']
        else:  # from raw e621 json
            self.id = post_data['id']
            self.ext = post_data['file']['ext']
            self.url = post_data['file']['url']
            self.tags = set(post_data['tags']['general'] + post_data['tags']['species'] +
                            post_data['tags']['meta'] + post_data['tags']['artist'])
            self.rating = post_data['rating']
            self.pools = len(post_data['pools']) != 0  # if post is managed by pools
            self.chars = len(post_data['tags']['character']) != 0  # set to str later
            self.copy = len(post_data['tags']['copyright']) != 0  # set to str later
            self.size = post_data['file']['size']
            # removed pathing which can be generated from other data
            fam_search = set([post_data['id']] + post_data['relationships']['children'])
            if post_data['relationships']['parent_id'] is not None:
                fam_search.add(post_data['relationships']['parent_id'])
            self.family = len(fam_search) != 1  # if post is saved in FamilyMGR
            if 'story_in_description' in self.tags:
                self.story = post_data['description']
            else:
                self.story = str()
            # handling pathing types
            if self.chars:  # true if character tags exist
                self.chars = 'Char'
            else:
                self.chars = 'No Char'
            if self.copy:  # true if copyright tags exist
                self.copy = 'Copy'
            else:
                self.copy = 'No Copy'

    def serialize(self):
        return {
            'id': self.id,
            'ext': self.ext,
            'url': self.url,
            'tags': list(self.tags),
            'rating': self.rating,
            'chars': self.chars,
            'pools': self.pools,
            'copies': self.copy,
            'size': self.size,
            'old_path': self.old_path,
            'story': self.story,
            'family': self.family,
        }

    def pathing(self):  # run at file downloads
        self.new_path = set_download_path(rating=self.rating, copy=self.copy, p_type='post',
                                          char=self.chars, ext=self.ext, tags=self.tags)

    def story_format(self):
        return dtext_to_html(self.story, f'{self.new_path}{self.id}.{self.ext}')  # Link to image in html

    def download(self, s):
        self.pathing()  # generate pathing
        if self.new_path != self.old_path:  # move file/dir if true
            if exists(self.old_path):  # check for directory
                new_file_path = f'{self.new_path}{self.id}.{self.ext}'
                old_file_path = f'{self.old_path}{self.id}.{self.ext}'
                if isfile(old_file_path):  # check if already downloaded
                    relocate(old_path=old_file_path, new_path=new_file_path)
            if len(self.story) > 0:  # true if story exists
                new_story_path = f'downloads/Stories/{self.new_path.replace("/", "--")}{self.id}.html'
                old_story_path = f'downloads/Stories/{self.old_path.replace("/", "--")}{self.id}.html'
                if isfile(old_story_path):  # check if exists
                    relocate(old_path=old_story_path, new_path=new_story_path)  # renames file
                save_txt_file(new_story_path, self.story_format())  # updates story pathing
            self.old_path = self.new_path
        # Directory stuff End / Downloading start
        file_path = f'{self.new_path}{self.id}.{self.ext}'
        if not isfile(file_path):  # check if already downloaded
            if not exists(self.new_path):  # check for directory
                directory(self.new_path)  # makes directory
            # self method for downloading story.html
            dl_file(file_path=file_path, my_url=self.url, s=s)  # download file


class Pool:
    def __init__(self, pool_data, custom=False):
        self.new_path = str()
        self.old_path = str()
        if custom:  # custom pool json
            self.id = pool_data['id']
            self.name = pool_data['name']
            self.rating = pool_data['rating']
            self.char = pool_data['char']
            self.copy = pool_data['copy']
            self.tags = set(pool_data['tags'])
            self.old_path = pool_data['old_path']
            self.size = pool_data['size']
            self.posts = dict()
            for post_id in pool_data['posts']:
                self.posts.setdefault(post_id, self.PoolPost(pool_data['posts'][post_id], custom=True))
        else:  # raw e621 pool json
            self.id = pool_data['id']
            self.name = pool_data['name']
            self.rating = 's'
            self.char = 'No Char'
            self.copy = 'No Copy'
            self.size = 0
            self.tags = set()
            self.posts = dict()
            for post_id in pool_data['post_ids']:
                self.posts.setdefault(post_id, self.PoolPost(post_id, temp=True))

    def serialize(self):
        # run pathing stuff?
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
        def __init__(self, post_data, custom=False, temp=False):
            if custom:  # from custom json
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
                    self.story = str()
                else:
                    self.id = post_data['id']
                    self.ext = post_data['file']['ext']
                    self.url = post_data['file']['url']
                    self.size = post_data['file']['size']
                    tmp_tags = set(post_data['tags']['general'] + post_data['tags']['species'] +
                                   post_data['tags']['meta'] + post_data['tags']['artist'])
                    if 'story_in_description' in tmp_tags:
                        self.story = post_data['description']
                    else:
                        self.story = str()

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
        if self.char == 'No Char':
            if len(new_char) > 0:
                self.char = 'Char'

    def copy_check(self, new_copy):
        if self.char == 'No Copy':
            if len(new_copy) > 0:
                self.char = 'Copy'

    def add_post(self, post_data):  # raw e621 post json
        self.posts[post_data['id']] = self.PoolPost(post_data)
        self.size += post_data['file']['size']
        self.tags.update(post_data['tags']['general'] + post_data['tags']['species'] +
                         post_data['tags']['meta'] + post_data['tags']['artist'])
        self.char_check(post_data['tags']['character'])
        self.copy_check(post_data['tags']['copyright'])
        self.rating_check(post_data['rating'])

    def pathing(self):  # run at file downloads
        self.new_path = set_download_path(rating=self.rating, copy=self.copy, p_type='pool',
                                          char=self.char, ext=None, tags=self.tags, name=self.name)

    def download(self, s):
        self.pathing()  # generate pathing
        if self.new_path != self.old_path:  # move file/dir
            if exists(self.old_path):  # check for directory
                relocate(old_path=self.old_path, new_path=self.new_path)
            self.old_path = self.new_path
        # post relocate stuff ## downloads/story/id.html links to file path/ sorted by path in story_main.html
        if len(self.posts) != 0 and self.new_path != "":  # false if missing data
            for post_id in self.posts:
                file_path = f'{self.new_path}{post_id}.{self.posts[post_id].ext}'
                if not isfile(file_path):  # check if already downloaded
                    if not exists(self.new_path):  # check directory
                        directory(self.new_path)  # make directory
                    dl_file(file_path=file_path, my_url=self.posts[post_id].url, s=s)


class Family:
    def __init__(self, family_data=None, custom=False, new=False):
        self.new_path = str()
        self.old_path = str()
        self.posts = dict()
        self.size = 0
        self.tags = set()
        self.rating = 's'
        self.char = 'No Char'
        self.copy = 'No Copy'
        self.ext = 'jpg'
        if custom:  # custom data
            self.ids = set(family_data['ids'])
            self.rating = family_data['rating']
            self.char = family_data['char']
            self.copy = family_data['copy']
            self.ext = family_data['ext']
            self.old_path = family_data['old_path']
            self.size = family_data['size']
            self.tags = set(family_data['tags'])
            self.posts = dict()
            for post_id in family_data['posts']:
                self.posts.setdefault(post_id, self.FamPost(family_data['posts'][post_id], custom=True))
        else:  # raw e621 post data; First post
            if new:
                fam_search = set([family_data['id']] + family_data['relationships']['children'])
                if family_data['relationships']['parent_id'] is not None:
                    fam_search.add(family_data['relationships']['parent_id'])
                self.ids = fam_search  # ids
                self.check_add(family_data)
            else:
                self.ids = set(family_data)  # ids

    def serialize(self):
        serial_posts = dict()
        for post_id in self.posts:
            serial_posts.setdefault(post_id, self.posts[post_id].serialize())
        return {
            'ids': list(self.ids),
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
        def __init__(self, post_data, custom=False):
            if custom:  # from custom json
                self.id = post_data['id']
                self.ext = post_data['ext']
                self.url = post_data['url']
                self.size = post_data['size']
                self.story = post_data['story']
            else:  # from raw e621 json
                self.id = post_data['id']
                self.ext = post_data['file']['ext']
                self.url = post_data['file']['url']
                self.size = post_data['file']['size']
                tmp_tags = set(post_data['tags']['general'] + post_data['tags']['species'] +
                               post_data['tags']['meta'] + post_data['tags']['artist'])
                if 'story_in_description' in tmp_tags:
                    self.story = post_data['description']
                else:
                    self.story = str()

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
        if self.char == 'No Char':
            if len(new_char) > 0:
                self.char = 'Char'

    def copy_check(self, new_copy):
        if self.char == 'No Copy':
            if len(new_copy) > 0:
                self.char = 'Copy'

    def ext_check(self, new_ext):  # check if not png or jpg
        if new_ext != 'jpg' and new_ext != 'png':
            self.ext = new_ext

    def check_add(self, post_data):  # adds posts if possible
        fam_search = set([post_data['id']] + post_data['relationships']['children'])
        if post_data['relationships']['parent_id'] is not None:
            fam_search.add(post_data['relationships']['parent_id'])
        if len(fam_search) == 1:
            return False  # 'Orphan'
        if not self.ids.isdisjoint(fam_search):
            self.posts.setdefault(post_data['id'], self.FamPost(post_data))
            self.ids.update(fam_search)
            self.size += post_data['file']['size']
            self.tags.update(post_data['tags']['general'] + post_data['tags']['species'] +
                             post_data['tags']['meta'] + post_data['tags']['artist'])
            self.char_check(post_data['tags']['character'])
            self.copy_check(post_data['tags']['copyright'])
            self.rating_check(post_data['rating'])
            self.ext_check(post_data['file']['ext'])
            return False  # 'Family'
        return True  # 'New or Another Family'

    def pathing(self):  # run at file downloads
        new_uid = list(self.ids)
        new_uid.sort(key=int)  # lowest ID is highest parent in family tree
        p_type = 'family'
        if len(self.posts) == 1:
            p_type = 'post'
        self.new_path = set_download_path(rating=self.rating, copy=self.copy, p_type=p_type,
                                          char=self.char, ext=self.ext, tags=self.tags, name=new_uid[0])
        if self.new_path != self.old_path:  # move file/dir
            if exists(self.old_path):  # check for directory
                pass  # FIX LATER
                # relocate(old_path=self.old_path, new_path=self.new_path)
            self.old_path = self.new_path


class DownloadMGR:
    custom_post_path = "custom/posts.json"
    custom_pool_path = "custom/pools.json"
    custom_fam_path = "custom/families.json"
    download_story_path = "downloads/Stories"
    abort = False

    def __init__(self):
        self.posts = dict()
        self.pools = dict()
        self.pool_tmp = set()
        self.families = list()
        self.tmp_fam = Family({0})  # for checking when self.families is 0
        directory("custom")

    class Metrics:
        kb_reference = 1_024
        mb_reference = kb_reference * kb_reference
        gb_reference = mb_reference * kb_reference

        def __init__(self, data):
            self.counter = 0
            self.total = len(data)
            self.size_count = 0
            self.size_total = 0
            if type(data) is list:
                for obj in data:
                    self.size_total += obj.size
            else:
                for thing_id in data:
                    self.size_total += data[thing_id].size

        def size_format(self, file_size):
            if file_size < self.gb_reference:
                if file_size < self.mb_reference:
                    return f'{round(file_size / self.kb_reference, 2)}Kb'
                else:
                    return f'{round(file_size / self.mb_reference, 2)}Mb'
            else:
                return f'{round(file_size / self.gb_reference, 2)}Gb'

        def display_count(self, name='Count', percent=False):
            if percent:
                print(f'{name}: {round(self.counter * 100 / self.total, 2)}%')
            else:
                print(f'{name}: {self.counter}/{self.total}')

        def display_size(self, name='Count', percent=False):
            if percent:
                print(f'{name}: {round(self.size_count * 100 / self.size_total, 2)}%')
            else:
                print(f'{name}: {self.size_format(self.size_count)}/{self.size_format(self.size_total)}')

        def iter(self, add=1, size=0):
            self.counter += add
            self.size_count += size

    def save_posts(self):  # exports custom POST json
        custom_json = dict()
        for post_id in self.posts:
            custom_json.setdefault(post_id, self.posts[post_id].serialize())
        save_json_file(self.custom_post_path, custom_json)
        print(f"{len(self.posts)} Posts Saved....")

    def save_pools(self):  # exports custom POOL json
        custom_json = dict()
        for pool_id in self.pools:
            custom_json.setdefault(pool_id, self.pools[pool_id].serialize())
        save_json_file(self.custom_pool_path, custom_json)
        print(f"{len(self.pools)} Pools Saved....")

    def save_families(self):  # exports custom FAMILY json
        custom_json = list()
        for family in self.families:  # families don't have IDs
            custom_json.append(family.serialize())
        save_json_file(self.custom_fam_path, custom_json)
        print(f"{len(self.families)} Families Saved....")

    def load_posts(self):  # loads custom POST json
        custom_json = open_json_file(self.custom_post_path)  # returns json dict
        if custom_json is not None:
            for post_id in custom_json:
                self.posts.setdefault(int(post_id), Post(custom_json[post_id], custom=True))
            print(f"{len(self.posts)} Posts Loaded....")

    def load_pools(self):  # loads custom POOL json
        custom_json = open_json_file(self.custom_pool_path)  # returns json dict
        if custom_json is not None:
            for pool_id in custom_json:
                self.pools.setdefault(int(pool_id), Pool(custom_json[pool_id], custom=True))
            print(f"{len(self.pools)} Pools Loaded....")

    def load_families(self):  # loads custom FAMILY json
        custom_json = open_json_file(self.custom_fam_path)  # returns json list
        if custom_json is not None:
            for family_data in custom_json:
                self.families.append(Family(family_data, custom=True))
        print(f"{len(self.families)} Families Loaded....")

    def stop(self):
        self.abort = True

    def add_post(self, post_data):  # adds post to post, pool, and family lists
        if post_data['file']['url'] is not None:  # catches default blacklist and misc errors
            self.posts[post_data['id']] = Post(post_data)  # overrides existing data for post id if it exists
            # Pool & Family stuff
            if len(post_data['pools']) > 0:  # True if post has pools
                self.pool_tmp.update(post_data['pools'])
            else:  # no pool-families
                if len(self.families) == 0:  # run tmp_fam check while no real families exist
                    if self.tmp_fam.check_add(post_data):  # True if unresolved, also adds post to itself if possible
                        self.families.append(Family(post_data, new=True))  # add new Family
                        self.posts[post_data['id']].family = True  # prevents double downloads
                else:
                    add_fam = True
                    for family in self.families:  # loop because families don't have ids
                        add_fam = family.check_add(post_data)  # True if unresolved, adds post to itself if possible
                        if not add_fam:  # true when post is added to family
                            break
                    if add_fam:  # true when no existing family is related
                        self.families.append(Family(post_data, new=True))  # add new Family
                        self.posts[post_data['id']].family = True  # prevents double downloads

    def post_search(self, search_str, fast_pools=True):
        # load posts & families
        self.load_posts()
        self.load_families()
        # Begin search requests
        post_api = "https://e621.net/posts.json"  # API shit
        search_params = {'tags': search_str, 'limit': '320', 'page': 1}
        result_count = 320
        with requests.Session() as s:
            while result_count != 0 and search_params['page'] < 750:
                print(f'post page: {search_params["page"]}', end='\r')  # debug
                result_data = get_json(post_api, search_params, s)  # returns e621 json
                result_count = len(result_data['posts'])  # checks how many posts in result
                for post in result_data['posts']:
                    self.add_post(post)  # adds post to post, pool, and family lists
                search_params['page'] += 1  # iterates page number
        # save posts & families to custom json
        self.save_families()
        self.save_posts()
        # load pools data
        self.load_pools()
        if fast_pools:  # difference_update removes unwanted elements
            if len(self.pool_tmp) != 0:  # catches empty
                if len(self.pools) != 0:
                    self.pool_tmp.difference_update(set(self.pools.keys()))
        # Begin pool requests
        pool_api = "https://e621.net/pools.json"
        chunk_list = list(chunks(list(self.pool_tmp), 70))  # limit is ~70 for e621
        print(f'Chunked {len(self.pool_tmp)} pools...')  # debug
        pool_params = {'search[id]': list(), 'limit': '320'}
        with requests.Session() as s:
            for id_list in chunk_list:
                pool_params['search[id]'] = ",".join(map(str, id_list))  # stringify pool ids
                my_data = get_json(pool_api, pool_params, s)  # returns e621 json
                for pool in my_data:
                    self.pools[pool['id']] = Pool(pool)  # overrides/adds pool in pool dict; No posts yet
        # save raw pool data?
        # download PoolPost data
        with requests.Session() as s:
            update_count = 0  # for periodic saving
            for pool_id in self.pools:
                print(f'Pool progress: {update_count}/{len(self.pools)}')
                if fast_pools:
                    if self.pools[pool_id].size != 0:
                        continue
                search_params['page'] = 1
                search_params['tags'] = f'pool:{pool_id}'
                result_count = 320
                while result_count != 0 and search_params['page'] != 750:
                    my_data = get_json(post_api, search_params, s)  # returns e621 json
                    result_count = len(my_data['posts'])
                    for post in my_data['posts']:
                        self.pools[pool_id].add_post(post)  # add posts to pool
                    search_params['page'] += 1  # iterates to next page
                update_count += 1  # saves every ~60 pool searches
                if update_count % 100 == 0:
                    self.save_pools()  # save pool to custom json
        # save pool to custom json
        self.save_pools()
        print('End of post search...')

    def download_all(self):
        if not exists(self.download_story_path):  # check directory
            directory(self.download_story_path)  # make directory
        self.load_posts()  # load posts for download
        with requests.Session() as s:
            clean_list = list()
            for post_id in self.posts:  # clean out posts managed by pools and families
                if self.posts[post_id].pools:  # True if managed by pool
                    clean_list.append(post_id)
                else:
                    if self.posts[post_id].family:  # true if not managed by family
                        clean_list.append(post_id)
            for post_id in clean_list:  # removing posts
                self.posts.pop(post_id)
            m_mgr = self.Metrics(data=self.posts)  # get cleaned data # METRICS
            for post_id in self.posts:
                m_mgr.iter(1, self.posts[post_id].size)  # METRICS
                self.posts[post_id].download(s=s)  # download stuff
                m_mgr.display_count('Posts')  # METRICS
        self.save_posts()
        print('Finished Post Downloads....')
        self.load_pools()  # load pools for download
        with requests.session() as s:
            m_mgr = self.Metrics(data=self.pools)  # METRICS
            for pool_id in self.pools:
                m_mgr.iter(1, self.pools[pool_id].size)  # METRICS
                self.pools[pool_id].pathing()  # generate pathing
                if len(self.pools[pool_id].posts) == 0 or self.pools[pool_id].new_path == "":  # true if missing data
                    continue
                for post_id in self.pools[pool_id].posts:
                    file_path = f'{self.pools[pool_id].new_path}{post_id}.{self.pools[pool_id].posts[post_id].ext}'
                    if not isfile(file_path):  # check if already downloaded
                        if not exists(self.pools[pool_id].new_path):  # check directory
                            directory(self.pools[pool_id].new_path)  # make directory
                        dl_file(file_path=file_path, my_url=self.pools[pool_id].posts[post_id].url, s=s)
                m_mgr.display_count('Pools')  # METRICS
        self.save_pools()  # save pathing
        print('Finished Pools Downloads....')
        self.load_families()  # load families for download
        with requests.session() as s:
            m_mgr = self.Metrics(data=self.families)
            for family in self.families:
                m_mgr.iter(1, family.size)  # METRICS
                family.pathing()  # generate pathing
                if len(family.posts) == 0 or family.new_path == "":
                    continue  # true if missing data
                for post_id in family.posts:
                    file_path = f'{family.new_path}{post_id}.{family.posts[post_id].ext}'
                    if not isfile(file_path):  # check if already downloaded
                        if not exists(family.new_path):  # check directory
                            directory(family.new_path)  # make directory
                        dl_file(file_path=file_path, my_url=family.posts[post_id].url, s=s)
                m_mgr.display_count('Families')  # METRICS
        self.save_families()
        print('Finished Families Downloads....')


class CleanSets:
    def __init__(self):
        self.ids = set()

    def search(self, search_str):
        post_api = "https://e621.net/posts.json"  # API shit
        search_params = {'tags': search_str, 'limit': '320', 'page': 1}
        result_count = 320
        with requests.Session() as s:
            while result_count != 0 and search_params['page'] < 750:
                print(f'{search_str} page: {search_params["page"]}')  # debug
                result_data = get_json(post_api, search_params, s)  # returns e621 json
                result_count = len(result_data['posts'])  # checks how many posts in result
                for post in result_data['posts']:
                    self.ids.add(str(post['id']))  # adds post to post, pool, and family lists
                search_params['page'] += 1  # iterates page number

    def clean(self):
        print(len(self.ids), 'ids')
        chunk_list = chunks(list(self.ids), 9990)
        super_str = str()
        for chunk in chunk_list:
            print(len(chunk), 'chunk size')
            super_str += f'\n\r|=================|\n\r{" ".join(chunk)}'
        save_txt_file('custom/clean_sets.txt', super_str)
