# -*- coding: utf-8 -*-
# @Time : 2021/3/27 0027 11:42
# @Author : zuozhu
# @File : url_ziyuan

import requests;
import json
import os
from bs4 import BeautifulSoup

root_url = r'https://www.bilibili.com/video/BV1gA411L7Gf?spm_id_from=333.851.b_7265636f6d6d656e64.4'

comm_headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Host':'api.bilibili.com',
    'Referer':'https://www.bilibili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

title_comm_headers={
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

video_audio_headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Origin':'https://www.bilibili.com',
    'Referer':'https://www.bilibili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

def get_bvid():
    bvid = '';
    bvids = root_url.split('?')[0].split('/')
    if bvids[-1]=='':
        bvid = bvids[-2];
    else:
        bvid = bvids[-1];
    return bvid;

def get_cid():
    bvid = get_bvid();
    cid_url = r'https://api.bilibili.com/x/player/pagelist?bvid=%s&jsonp=jsonp'%(bvid);
    r = requests.request(method='GET',url=cid_url,headers=comm_headers);
    r.encoding = r.apparent_encoding;
    back_info = r.text;
    back_info_str = str(back_info);
    cid_dict = json.loads(back_info_str);
    cids = cid_dict['data'];
    return cids;


def get_page_data(url,headers):
    r = requests.request(method='GET',url=url,headers = headers);
    try:
        r.raise_for_status()
    except:
        print('请求失败!!!!!')
    r.encoding = r.apparent_encoding;
    return r;

def get_video(page_back_dict,name):
    if type(page_back_dict) is dict:
        file_type = 'video'
        video_datas = page_back_dict['data']['dash']['video']
        print('开始保存video文件......');
        # 应该用命令行传入(这里写死)
        save_folder = r'E:/bilibili/%s' % (name);
        for video_data in video_datas:
            video_url = video_data['baseUrl'];
            print(video_url)
            name_list = video_url.split('.m4s');
            video_file_name = name_list[0].split('/')[-1];
            video_data = requests.request(method='GET',url=video_url,headers=video_audio_headers);
            save_file(file_type,save_folder,video_file_name,video_data);
        print('保存video文件结束......')


def get_audio(page_back_dict,name):
    if type(page_back_dict) is dict:
        file_type = 'audio';
        audio_datas = page_back_dict['data']['dash']['audio'];
        print('开始保存audio文件......')
        save_folder = r'E:/bilibili/%s' % (name);
        for audio_data in audio_datas:
            audio_url = audio_data['baseUrl'];
            print(audio_url, end='\n');
            name_list = audio_url.split('.m4s');
            audio_file_name = name_list[0].split('/')[-1];
            # 获取音频
            r_data = requests.request(method='Get', url=audio_url, headers=video_audio_headers);
            save_file(file_type,save_folder, audio_file_name, r_data);
        print('保存audio文件结束......');


def save_file(file_type,dir,file_name,data):
    if not os.path.exists(dir):
        os.mkdir(dir);
    file_path = dir+'/'+file_name+'.m4s';
    with open(dir+'/'+file_name+'.m4s','ab') as f:
        f.write(data.content);
    print('保存%s文件【name=%s】成功!!!'%(file_type,file_name));


def merge_video_audio(name):
    folder = r'E:/bilibili/%s/'%(name)
    merge_dir = r'E:/bilibili/merge'
    if not os.path.exists(merge_dir):
        os.mkdir(merge_dir);
    file_names = [];
    for root, dirs, files in os.walk(folder):
        file_names = files;
    files_list = ['%s%s'%(folder,item) for item in file_names];
    print(files_list)
    info_str = ' -i '.join(files_list);
    print(info_str)
    cmd_str = 'ffmpeg -y -i %s -codec copy %s/%s.mp4'%(info_str,merge_dir,name);
    print(cmd_str)
    os.system(cmd_str);
    print('下载完成......')
    print('视频保存位置为:【%s/%s.mp4】'%(merge_dir,name))



def get_title():
    r = requests.request(method='GET', url=root_url, headers=title_comm_headers);
    bsoup = BeautifulSoup(r.text, 'html.parser');
    title = bsoup.find('div', attrs={'class': 'l-con'}).find('h1', attrs={'class': 'video-title'})['title'];
    new_title = title.replace(' ','');
    print(new_title)
    return new_title;

def get_video_audio():
    bvid = get_bvid();
    cids = get_cid();
    title = get_title();
    count = 0;
    for item in cids:
        count+=1;
        print('第%d-P开始'%(count));
        cid=item['cid'];
        name = item['part'];
        name_trip = name.replace(' ', '');
        new_titile = title+name_trip;
        video_audio_url = r'https://api.bilibili.com/x/player/playurl?cid={}&bvid={}&qn=0&type=&otype=json&fourk=1&fnver=0&fnval=80'.format(cid,bvid);
        r = get_page_data(video_audio_url,comm_headers);
        page_back_info = r.text;
        page_back_dict = json.loads(page_back_info);
        get_video(page_back_dict,new_titile);
        get_audio(page_back_dict,new_titile);
        merge_video_audio(new_titile);
        print('第%d-P完成'%(count));

if __name__ == '__main__':
    # get_cid();
    get_video_audio();