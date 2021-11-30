# -*- coding: utf-8 -*-
# @ author:captain
# @ time:2021/11/26 0026:10:40

import requests
import re
import json
import pprint  # 格式化输出模块
import subprocess
import os


headers={
'Referer': 'https://www.bilibili.com/',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

def send_request(url):
    '''请求数据'''
    response = requests.get(url=url,headers=headers)
    return response


def get_video_data(html_data):
    '''解析视屏数据'''
    try:
        # 1.提取视频的标题
        title = re.findall('<span class="tit">(.*?)</span>', html_data)[0]

        # 2.提取视频对应的json数据
        json_data = re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0]

        # 3.将json格式数据转换为字典
        json_data = json.loads(json_data)

        # 4.提取音频的url地址
        audio_url = json_data['data']['dash']['audio'][0]['baseUrl']

        # 5.提取视屏的url地址
        video_url = json_data['data']['dash']['video'][0]['baseUrl']

        video_data = [title, audio_url, video_url]
        return video_data
    except:
        return False




def check_path(audio_path,video_path):
    '''检查视频是否已经存在'''
    # 新视频合成后，对原来的音频和视频进行删除
    # 删除原音频
    if os.path.exists(audio_path):
        os.remove(audio_path)
    # 删除原视频
    if os.path.exists(video_path):
        os.remove(video_path)


# 合成视频参考：https://blog.csdn.net/m0_50027019/article/details/120379003
def save_data(file_name,audio_url,video_url):
    # 请求数据
    print('正在请求音频数据...')
    audio_data = send_request(audio_url).content

    print('正在请求视屏数据...')
    video_data = send_request(video_url).content

    # 音频、视频名称和路径
    audio_name = file_name+'.mp3'
    video_name = file_name
    # file_path = 'C:\\Users\\Administrator\\Desktop\\spider\\05.多线程、进程、协程\\'
    file_path = os.getcwd()+'\\'
    audio_path = file_path + audio_name
    video_path = file_path + video_name
    all_path = file_path +file_name

    # 音频保存
    with open(audio_name, mode='wb') as f:
        f.write(audio_data)
        print('正在保存音频数据...')

    # 视频保存
    with open(video_name, mode='wb') as f:
        f.write(video_data)
        print('正在保存视频数据...')

     # 视频合成
    command = 'ffmpeg.exe -i {} -i {} -acodec copy -vcodec copy {}.mp4'.format(audio_path, video_path, all_path)
    os.system(command)
    check_path(audio_path,video_path)
    print('视频合并成功')


def user():
    '''人机交互'''
    # https://www.bilibili.com/video/BV1Yh411o7Sz?p=6
    print('*' * 100)
    print('                             ===B站视频下载注意点===                                               *')
    print('说明：从网页上复制的视频链接为https://www.bilibili.com/video/后的链接                              *')
    print('比如：此链接https://www.bilibili.com/video/BV1Yh411o7Sz?p=6，只需要BV1Yh411o7Sz?p=6就行            *')
    print('                               ===输入0退出程序===                                                 *')
    print('*' * 100)
    # url = 'https://www.bilibili.com/video/'
    # user_url = input('请输入视频连接：')
    # new_url = url+user_url
    # return new_url


# 函数调用模块
if __name__=='__main__':
    user()
    url = 'https://www.bilibili.com/video/'
    while True:
        # 用户交互
        user_url = input('请输入视频连接：')
        new_url = url + user_url
        if user_url=='0':
            break

        # 数据请求
        html_data = send_request(new_url).text

        # 数据处理，获取视频的标题、视频链接、音频链接
        video_data = get_video_data(html_data)
        if video_data==False:
            print('无法下载本视频！')
        else:
            # 视频合成与保存
            save_data(video_data[0],video_data[1],video_data[2])


