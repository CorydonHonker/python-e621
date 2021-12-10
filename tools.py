#  methods: run search to get tags and tag types.
#  save sorted tags in config/tools/tag_types.json.
#  load config/posts.json scan tags and sort them by type while counting each instance.
#  save sorted & counted tags as config/tools/tag_counts.json
#  use tag_counts.json to generate {type}.txt which lists tags by count descending
#  /////
#  run search to get tags, types, and related tags
#  post: {tag_type:set(tags...), ...}  # all tags per post are saved (maybe scores and favcount too).
#  loop through posts and get list of all tags per tag type.
#  loop through all posts with tag list and add counts of other related tags.
#  save as config/tools/complex_counts.json
#  output *.txt looks like:  #  need a way to filter boring tags from top list and body lists, like "mammal"
#  () tag--------- () next_tag-------- () ...
#  ()\____________/()\________________/() ...
#  () related_tag- () next_related_tag () ...
#  () ...          () ...              () ...
#  //////////////////////////////////////////
#  () tag___________________ () next_tag______________ ()
#  ()\______________________/()\______________________/()
#  () related_tag (tag_type) () next_related_tag (tt)_ ()
from os.path import isfile

import requests

from math import ceil
from my_net import get_json
from my_IO import save_json_file, open_json_file, save_txt_file, directory, name_filter


class ComplexPosts:
    def __init__(self, post_data):
        self.id = post_data['id']
        self.tags = {
            'artist': post_data['tags']['artist'],
            'copyright': post_data['tags']['copyright'],
            'character': post_data['tags']['character'],
            'species': post_data['tags']['species'],
            'general': post_data['tags']['general'],
            'meta': post_data['tags']['meta'],
        }

    def serialize(self):
        return {
            'id': self.id,
            'tags': self.tags,
        }


class ComplexTags:
    def __init__(self, tag):
        self.tag = tag
        self.tags = {
            'artist': dict(),
            'copyright': dict(),
            'character': dict(),
            'species': dict(),
            'general': dict(),
            'meta': dict(),
        }

    def get_super_dict(self):
        s_tag_dict = dict()
        for r_tag_type, r_tag_dict in self.tags.items():
            for r_tag_name, r_count in r_tag_dict.items():
                s_tag_dict.setdefault(f'{r_tag_name} ({r_tag_type})', r_count)
        tmp = sorted(s_tag_dict.items(), key=lambda x: x[1])
        tmp.reverse()
        return dict(tmp[:1000])  # return dict with 1000 items

    def add_tags(self, post_tags):
        for tag_type, tag_list in post_tags.items():
            for tag in tag_list:
                self.tags[tag_type].setdefault(tag, 0)
                self.tags[tag_type][tag] += 1


class TagManager:
    c_tag_path = 'config/tools/complex_tags.json'
    post_save_path = 'config/posts.json'

    def __init__(self):
        directory('config/tools')
        directory('downloads/tools')
        self.c_posts = dict()
        self.every_tag = {
            'artist': set(),
            'copyright': set(),
            'character': set(),
            'species': set(),
            'general': set(),
            'meta': set(),
        }
        self.c_tags = {  # like this? | yes!
            'artist': dict(),
            'copyright': dict(),
            'character': dict(),
            'species': dict(),
            'general': dict(),
            'meta': dict(),
        }

    def save_c_posts(self):
        config_json = dict()
        for post_id, post in self.c_posts.items():
            config_json.setdefault(post_id, post.serialize())
        save_json_file(self.c_tag_path, config_json)
        print(f"{len(config_json)} Posts Saved....")

    def load_c_posts(self):
        config_json = open_json_file(self.c_tag_path)  # returns json dict
        if config_json is not None:
            for post_id, post in config_json.items():
                self.c_posts.setdefault(int(post_id), ComplexPosts(post))
        print(f"{len(self.c_posts)} Posts Loaded....")

    def add_c_post(self, post_data):  # e621 post data
        self.c_posts.setdefault(post_data['id'], ComplexPosts(post_data=post_data))

    def e621_search(self, search_str):  # convert posts to c_posts
        print(f'Start of {search_str} post search...')
        post_api = "https://e621.net/posts.json"  # API shit
        search_params = {'tags': search_str, 'limit': '320', 'page': 1}
        result_count = 320
        with requests.Session() as s:
            while result_count != 0 and search_params['page'] < 750:
                print(f'post page: {search_params["page"]}')  # debug
                result_data = get_json(post_api, search_params, s)  # returns e621 json
                result_count = len(result_data['posts'])  # checks how many posts in result
                for post in result_data['posts']:
                    self.add_c_post(post)  # adds post to Post list
                search_params['page'] += 1  # iterates page number
        # self.save_c_posts()  # save posts to custom json

    def make_c_tags(self):
        print('making c_tags...')
        # self.load_c_posts()
        for post_id, post in self.c_posts.items():
            for tag_type, tag_list in post.tags.items():
                self.every_tag[tag_type].update(tag_list)
        # self.every_tag is filled with tags
        print(f'general size: {len(self.every_tag.get("general"))} | every tag filled...')
        for tag_type, tag_set in self.every_tag.items():
            for tag in tag_set:
                self.c_tags[tag_type].setdefault(tag, ComplexTags(tag))
        # c_tags filled with initialized ComplexTags
        print(f'general size: {len(self.c_tags.get("general"))} | c_tags filled...')
        for post_id, post in self.c_posts.items():
            for tag_type, tag_list in post.tags.items():
                for tag in tag_list:  # adds post tags to every c_tag in the post
                    self.c_tags[tag_type][tag].add_tags(post.tags)
        print(f'general size: {len(self.c_tags.get("general"))} | c_tags filled with filled ComplexTags...')
        # c_tags filled with filled ComplexTags
        # NEXT format txt file
        for tag_type, tag_dict in self.c_tags.items():  # why is collection so messed up?? | simplify it!
            directory(f'downloads/tools/{tag_type}')
            # sort tag_dict?
            for items_idx, (c_tag_name, c_tag_obj) in enumerate(tag_dict.items()):
                print(f'starting {c_tag_name} collection...')
                # add tag_names to first list, skip 2nd line, sort and add tags to end of list.
                name_size = 1
                string_lines = list()
                string_lines.append(c_tag_name)
                string_lines.append('')
                s_dict = c_tag_obj.get_super_dict()
                if len(s_dict) < 24:
                    continue  # too small to save as txt
                else:
                    if list(s_dict.items())[0][1] < 12:  # if first < 4
                        continue
                for s_tag_name, s_tag_count in s_dict.items():
                    string_lines.append(f'{s_tag_count} | {s_tag_name}')
                    if len(string_lines[-1]) > name_size:
                        name_size = len(string_lines[-1])
                # lines and line size collected | format and save text file
                file_name = f'downloads/tools/{tag_type}/{name_filter(c_tag_name)}.txt'
                nl = '\n'
                save_txt_file(file_name, f"{nl.join(string_lines)}\n")
