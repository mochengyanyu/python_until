# -*- coding: utf-8 -*-
# @Time : 2021/4/18 0018 22:18
# @Author : zuozhu
# @File : down_video

# 下载小电影(py,你懂得)

# video1 代表大陆
# video2 代表日韩
# video3 代表欧美
# video4 代表动画
# video5 代表三级

import os;
import requests;
from bs4 import BeautifulSoup;

root_url = r'https://b8tang.vip/html/category/video/';

vide_type=['video1','video2','video3','video4','video5'];

# save_file_dir = r'E:/video/大陆/';

headers={
    'Upgrade-Insecure-Requests':'1',
    'content-type':'text/html; charset=utf-8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

video_headers={
    'Origin':'https://b8xiao.vip',
    'Referer':'https://b8xiao.vip/html/264165/',
    'content-type':'video/mp2t',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

video_count = 0;

def get_video_info(url,dir):
    r = requests.request(method='GET',headers=headers,url=url);
    try:
        r.raise_for_status();
    except:
        print('请求失败!!!');
    bsoup = BeautifulSoup(r.text,'html.parser');
    div_info = bsoup.find(attrs={'class':'lb_nr lb_nrn'});
    lis = div_info.ul.find_all('li');
    for li in lis:
        try:
            li_info = li.p.a
            name = li_info.text.replace(' ','');
            end_url = li_info['href'];
            video_url = 'https://b8tang.vip'+end_url;
            video_real_url = down_video(video_url);
            # print('down video url:',video_real_url);
            r_data = requests.request(method='GET',url=video_real_url,headers=video_headers)
            save_video(r_data.content,name,dir);
        except:
            continue;

def down_video(video_url):
    r = requests.request(method='GET',url=video_url,headers = headers);
    try:
        r.raise_for_status();
    except:
        print('请求失败!!!');
    bsoup = BeautifulSoup(r.text,'html.parser');
    down_btn = bsoup.find(attrs={'id':'clickdownload'});
    a_info = down_btn.a
    down_url = a_info['href'];
    downurl_end = down_url.split('/')[-1]
    down_video_read_url = 'https://xia777zhai.com/assets/'+downurl_end;
    return down_video_read_url;

def save_video(data,video_name,dir):
    global video_count;
    video_count+=1;
    if not os.path.exists(dir):
        os.makedirs(dir);
    with open(dir+video_name+'.mp4','wb') as video_file:
        video_file.write(data);
    print('下载完成,视频保存位置为:【%s】----video count:%d'%(dir+video_name+'.mp4',video_count))

#<a href="https://xia777zhai.com/assets/6777ab2ae7a395eff4253120d977eff0.mp4" target="_self" rel="noopener noreferrer" id="downallurl">下载观看</a>

if __name__ == '__main__':
    # page_2.html
    count=0;
    for page in range(1,3):
        # video1-代表大陆 video2-代表日韩 video3-代表欧美 video4-代表动漫 video5-代表三级
        # page_%s代表页数
        url = root_url+'video3/page_%s.html'%(str(page));
        save_file_dir = r'E:/video/欧美/';
        if page % 5 == 0:
            count += 1;
        save_file_dir = save_file_dir + str(count) + '/';
        print('第%d页' % (page));
        get_video_info(url,save_file_dir);