import requests
import time

def get_comments(video_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': video_url
    }
    
    # 提取视频的BV号
    bv_id = video_url.split('/')[-1]
    
    # 获取视频的aid
    video_info_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bv_id}'
    response = requests.get(video_info_url, headers=headers)
    video_info = response.json()
    if video_info['code'] != 0:
        raise ValueError(f"无法获取视频信息: {video_info['message']}")
    
    aid = video_info['data']['aid']
    
    # 获取评论数据
    comment_url = f'https://api.bilibili.com/x/v2/reply?&oid={aid}&type=1'
    comments = []
    page = 1
    while True:
        response = requests.get(f"{comment_url}&pn={page}", headers=headers)
        data = response.json()
        if data['data']['replies']:
            for reply in data['data']['replies']:
                comments.append(reply['content']['message'])
            page += 1
            time.sleep(1)  # 控制请求频率
        else:
            break
    return comments

video_url = 'https://www.bilibili.com/video/BV1Kb421v78P'  # 替换为你的视频网址
try:
    comments = get_comments(video_url)
    for comment in comments:
        print(comment)
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
