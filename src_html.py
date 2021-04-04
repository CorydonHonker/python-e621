from basic_definitions import *


web_name = {'furaffinity.net': set(), 'imagebam.com': set(), 'twitter.com': set(), 'refsheet.net': set(),
            'sofurry.com': set(), 'cloudnovel.net': set(), 'animatic.fun': set(), 'f-list.net': set(), 'sta.sh': set(),
            'weebly.com': set(), 'pastebin.com': set(), 'queencomplex.net': set(), 'artstation.com': set(),
            'fiverr.com': set(), 'marmalademum.com': set(),
            'newgrounds.com':set(), 'sealled.space': set(), 'reallyhorrible.art': set(), 'mythologian.net': set(),
            'hentai-foundry.com': set(), 'subscribestar.adult': set(), 'ko-fi.com': set(), 'reddit.com': set(),
            'google.com': set(), 'tumblr.com': set(), 'patreon.com': set(), 'mega.nz': set(), 'furrynetwork.com': set(),
            'weasyl.com': set(), 'pixiv.net': set(), 'trello.com': set(), 'derpibooru.org': set(), 'aryion.com': set(),
            'archiveofourown.org': set(), 'pornhub.com': set(), 'secret.graphics': set(), 'baraag.net': set(),
            'koboldadventure.com': set(), 'deviantart.com': set(), 'furrydakimakura.com': set(), 'rule34.xxx': set(),
            'dropbox.com': set(), 'foxxfire.com': set(), 'zoo.booru': set(), 'itch.io': set(), 'Misc': set()}
# link_part_a = '<a href="url">link text</a>'
doc_head = ('<!DOCTYPE html><head><meta charset="UTF-8"></head>''<style type="text/css">'
            'a:visited{color:#ddc41e}body{background-color:#20041a;color:white}</style>'
            '<html><body><div id="butt"></div></br><div id="dump"></div><script type="text/javascript">'
            'function hide_elm(){x=document.getElementsByClassName("lnk");for(i=0;i<x.length;i++){x[i].hidden=true;}};')
doc_tail = '</script></body></html>'


def find_valid_url(my_link):
    global file_types
    cut_a = 'http'
    cut_b = ')'
    ban_tuple = ('twimg', 'inkbunny', 'org/images', '/status/', '/view/', '/file', 'imgbox.com', 'imgur.com',
                 '/art/', '/submissions/', '/artworks/', '/pictures/', '/posts/', '/photo', 'facebook', '=post',
                 'randomarchive.com', '/img/', 'googleusercontent', '/submission/', 'com/p/', 'discordapp.com',
                 'e621.net', 'sofurryfiles', '/post/', '/t.me/', '/discord.', 'yahoo.com', 'derpiboo.ru',
                 'desuarchive.org', 'vk.com', '/media/')
    if my_link.find(cut_a) < 0:
        return -1
    for f_type in file_types:
        if my_link.find(f_type) > -1:
            return -1
    for f_type in ban_tuple:
        if my_link.find(f_type) > -1:
            return -1
    my_link = my_link.split(cut_a, 1)
    my_link = (cut_a + my_link[-1]).rsplit(cut_b, 1)
    return my_link[0]


def html_a_tag(link, extra):
    global web_name
    new_tag = f'({extra}) <a href="{link}">{link}</a></br>'
    for site in web_name:
        if not link.find(site) == -1:
            web_name[site].add(new_tag)
            return 0
    web_name['Misc'].add(new_tag)


def html_builder(file_name='sources.html'):
    global doc_head, web_name
    for site in web_name:
        bloc = (f"h0=document.createElement('button');p0=document.createElement('div');p0.hidden=true;"
                f"h0.innerHTML='{site} ({len(web_name[site])})';p0.className='lnk';"
                f"p0.innerHTML='{''.join(web_name[site])}';h0.id='{site}_h3';"
                f"p0.id='{site}_p';document.getElementById('butt').appendChild(h0);"
                f"document.getElementById('dump').appendChild(p0);"
                f"document.getElementById('{site}_h3').addEventListener('click',function(){{"
                f"hide_elm();document.getElementById('{site}_p').hidden=false}});")
        doc_head += bloc
    save_raw_data(file_name, doc_head + doc_tail)
    return 0


def src_to_html(u, file_type):
    new_list = get_file_data(user_name[u] + file_type)
    time_data(True, count_goal=len(new_list))
    counter = 0
    for link in new_list:
        valid_url = find_valid_url(link)
        if isinstance(valid_url, str):
            html_a_tag(valid_url, str(new_list[link]))
        counter += 1
        if counter % 1024 == 0:
            display_info = time_data(counter=counter)
            print(
                f'src_to_html | Posts:{counter}/{len(new_list)} | {sig_digs(100 * display_info[1])}% '
                f'| Total:{time_format(display_info[2])} | Remain:{time_format(display_info[3])} '
            )
    html_builder()
