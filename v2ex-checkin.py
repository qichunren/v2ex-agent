import os
import requests
from bs4 import BeautifulSoup
import re

# 配置信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Cookie': os.environ.get('V2EX_COOKIE', ''),
}
MISSION_URL = 'https://v2ex.com/mission/daily'

def main():
    # 访问每日任务页面
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        # 获取任务页面内容
        response = session.get(MISSION_URL)
        if response.status_code != 200:
            print(f'错误：无法访问页面，状态码 {response.status_code}')
            return

        # 解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
        button = soup.find('input', {
            'class': 'super normal button',
            'value': re.compile(r'领取 X 铜币')
        })

        # Print current login user name
        tools_div = soup.find('div', class_='tools')
        if not tools_div:
            print("Not find .tools element!")
            return None
        # 查找所有包含 "/member/" 的链接
        user_links = tools_div.find_all('a', href=lambda href: href and href.startswith('/member/'))
    
        if not user_links:
            return None
    
        # 提取第一个匹配链接的用户名（通常唯一）
        user_link = user_links[0]
        username = user_link.get_text(strip=True)
        print("Current user:", username)
    
        # 检查是否已领取
        if not button:
            print("今日奖励已领取或按钮不存在")
            return

        # 提取once参数
        onclick_js = button.get('onclick', '')
        once_match = re.search(r'once=(\d+)', onclick_js)
        if not once_match:
            print("错误：无法提取once参数")
            return

        once_value = once_match.group(1)
        redeem_url = f'https://v2ex.com/mission/daily/redeem?once={once_value}'

        # 发送领取请求
        redeem_resp = session.get(redeem_url)
        if redeem_resp.status_code == 200:
            print("铜币领取成功！")
        else:
            print(f"领取失败，状态码：{redeem_resp.status_code}")

    except Exception as e:
        print(f"发生异常：{str(e)}")

if __name__ == '__main__':
    main()
