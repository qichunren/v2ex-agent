import os
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

# 配置信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Cookie': os.environ.get('V2EX_COOKIE', ''),
}

# Watch the following topics
WATCH_TOPICS = [
    'Ruby',
    'Rails',
    'Ruby on Rails',
    'Flutter',
    '电路',
    '路由器',
    '独立开发',
    '开发者',
    '付费',
    '上海'
]

# Define the patrol url list
PATROL_URLS = [
    'https://v2ex.com/?tab=tech', # 技术
    'https://v2ex.com/?tab=creative', # 创意
    'https://v2ex.com/?tab=play', # 好玩
    'https://v2ex.com/?tab=qna', # 问答
    'https://v2ex.com/?tab=hot', # 热门
    'https://v2ex.com/?tab=all', # 全部
    'https://v2ex.com/go/hardware', # 硬件
    'https://v2ex.com/go/programming', # 编程
    'https://v2ex.com/go/ror', # Ruby on Rails
    'https://v2ex.com/go/career', # 职场
    'https://v2ex.com/go/design', # 设计
    'https://v2ex.com/go/life', # 生活
    'https://v2ex.com/go/shanghai' # 上海
]

def contains_watch_topic(title):
    """检查标题是否包含关注的主题关键字"""
    return any(topic.lower() in title.lower() for topic in WATCH_TOPICS)

def visit_topic(session, topic_url):
    """访问帖子并记录"""
    try:
        full_url = f'https://v2ex.com{topic_url}' if topic_url.startswith('/') else topic_url
        response = session.get(full_url)
        if response.status_code == 200:
            print(f'成功访问帖子：{full_url}')
            # 记录到文件
            log_topic(full_url)
        else:
            print(f'访问帖子失败，状态码：{response.status_code}')
    except Exception as e:
        print(f'访问帖子出错：{e}')
    finally:
        # 避免请求过快
        time.sleep(3)

def log_topic(url):
    """记录感兴趣的帖子到文件"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('interesting_topics.log', 'a', encoding='utf-8') as f:
        f.write(f'{timestamp} - {url}\n')

def main():
    # 访问每日任务页面
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        # 获取任务页面内容
        for url in PATROL_URLS:
            print(f'开始巡逻：{url}')
            response = session.get(url)
            if response.status_code != 200:
                print(f'错误：无法访问页面，状态码 {response.status_code}')
                continue
            print(f'访问页面成功：{url}')

            # 测试时可以使用本地文件
            # with open('test/html_response.html', 'r') as file:
            #     response_text = file.read()
            # soup = BeautifulSoup(response_text, 'html.parser')
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # 获取帖子主标题列表
            title_list = soup.find_all('a', class_='topic-link')
            print(f'帖子主标题列表：（{len(title_list)}）')
            
            for title_elem in title_list:
                title_text = title_elem.get_text()
                topic_url = title_elem.get('href')
                print(f'检查标题：{title_text}')
                
                if contains_watch_topic(title_text):
                    print(f'发现感兴趣的主题：{title_text}')
                    visit_topic(session, topic_url)

            # 每个页面之间暂停一下
            time.sleep(10)
            
    except Exception as e:
        print(f'错误：{e}')

if __name__ == '__main__':
    main()
