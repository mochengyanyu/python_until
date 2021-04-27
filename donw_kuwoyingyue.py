# -*- coding: utf-8 -*-
# @Time : 2021/4/3 0001 09:33
# @Author : zuozhu
# @File : donw_kuwoyingyue

import requests
import json


# search_key_url = r'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn={}&httpsStatus=1';

# get_song_url = r'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1617253572771&httpsStatus=1&reqId={}'


headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

search_headers={
    'Host': 'www.kuwo.cn',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Referer':'http://www.kuwo.cn/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

url = r'http://www.kuwo.cn/';
song_dir = r'F:/kuwo/'
song_count = 0;

def save_song(r_data,song_name):
    global song_count;
    song_count+=1;
    save_file = song_dir+song_name+'.mp3';
    with open(save_file,'wb') as song_file:
        song_file.write(r_data.content);
    print('下载成功:【保存位置为:%s】------%d'%(save_file,song_count));

def down_song(url):
    r_data = requests.request(method='GET',url=url,headers=headers)
    return r_data


def get_song_url(key):
    r = requests.request(method='GET', url=url, headers=headers);
    # 获取kw_token和csrf参数(一定要在请求头上带上这两个参数去请求,kw_token是放在Cookie中的)
    cookies = r.headers['Set-Cookie'].split(';')[0];
    csrf = cookies.split('=')[-1]
    search_headers['Cookie'] = cookies;
    search_headers['csrf'] = csrf;
    for i in range(1, 5):
        search_url = r'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn={}&httpsStatus=1'.format(key, i, 30);
        search_res = requests.request(method='GET', url=search_url, headers=search_headers);
        back_info = search_res.text;
        try:
            back_info_dict = json.loads(back_info);
        except:
            continue;
        reqId = back_info_dict['reqId'];
        songs_info = back_info_dict['data']['list'];
        for song_info in songs_info:
            song_rid = song_info['rid'];
            song_name = song_info['name'];
            if '(' in song_name:
                index_count = song_name.index('(');
                song_name = song_name[0:index_count];
            get_song_url = r'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1617253572771&httpsStatus=1&reqId={}'.format(song_rid, reqId)
            song_info_back = requests.request(method='GET', url=get_song_url, headers=search_headers);
            try:
                song_back_dict = json.loads(song_info_back.text);
            except:
                continue;
            song_url = song_back_dict['url'];
            r_data = down_song(song_url);
            save_song(r_data, song_name);

if __name__ == '__main__':
    key='周杰伦'
    get_song_url(key);

