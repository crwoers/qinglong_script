import requests
from bs4 import BeautifulSoup
import json
import re

# 加载pt.json文件
def load_pt_sites():
    try:
        with open('./pt.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载pt.json文件失败: {e}")
        return []

# 检测站点是否开放注册
def check_registration_open(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 尝试绕过Cloudflare的基本防护
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(url, timeout=10)
        
        # 检查Cloudflare人机验证
        if 'cf-challenge-form' in response.text:
            print(f"检测到Cloudflare人机验证: {url}")
            return None  # 需要人工处理
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找注册表单中的输入框
        text_inputs = soup.find_all('input', {'type': 'text'})
        password_inputs = soup.find_all('input', {'type': 'password'})
        
        # 如果有文本输入框或密码输入框，可能开放注册
        if text_inputs or password_inputs:
            # 进一步检查是否有"注册"、"signup"等关键词
            page_text = response.text.lower()
            if 'signup' in page_text or 'register' in page_text or '注册' in page_text:
                return True
        
        return False
        
    except Exception as e:
        print(f"检测站点 {url} 时出错: {e}")
        return None

# 主函数
def main():
    pt_sites = load_pt_sites()
    if not pt_sites:
        print("没有加载到任何PT站点信息")
        return
    
    open_sites = []
    
    for site in pt_sites:
        name = site.get('name', '未知站点')
        url = site.get('href', '')
        
        if not url:
            continue
        
        print(f"正在检测: {name} - {url}")
        status = check_registration_open(url)
        
        if status is None:
            print(f"{name}: 检测失败，可能需要人工验证")
        elif status:
            print(f"{name}: 可能开放注册")
            open_sites.append(f"{name}: {url}")
        else:
            print(f"{name}: 未开放注册")
    
    # 发送通知
    if open_sites:
        content = "开放注册的站点如下:\n" + "\n".join(open_sites)
        print(content)
        content = "此检测基于页面元素分析，结果仅供参考\n" + content
        print(QLAPI.systemNotify({ "title": "PT站点开放注册通知", "content":  content}))
        
        # 青龙面板系统通知
        # try:
        #     QLAPI.systemNotify({
        #         "title": "PT站点开放注册通知",
        #         "content": content
        #     })
        # except Exception as e:
        #     print(f"发送通知失败: {e}")
    else:
        print("当前没有检测到开放注册的PT站点")

if __name__ == '__main__':
    main()