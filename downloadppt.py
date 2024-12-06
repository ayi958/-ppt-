import requests
import re
from bs4 import BeautifulSoup
import json
import requests
from bs4 import BeautifulSoup
import requests
from lxml import html
import os
import time
import parsel
def download_file(download_url, filename,headers,cookies):
    # 发起下载请求
    response = requests.get(download_url, stream=True,headers=headers,cookies=cookies)
    if response.status_code == 200:
        print(f"开始下载文件：{filename}")
        # 保存文件
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"文件下载完成：{filename}")
    else:
        print(f"下载失败，状态码：{response.status_code}")

def get_params(url):
    # 正则表达式，匹配 'chapterId'、'courseId' 和 'clazzid'
    pattern = r"([a-zA-Z0-9]+)=(\d+)"

    # 查找所有匹配的结果
    matches = re.findall(pattern, url)

    # 提取到的参数字典
    params = {match[0]: match[1] for match in matches}

    # 打印提取的结果
    #print(params)
    return params


def get_objectid(chapterId,courseId,clazzid,newurl,headers,cookies):

    session = requests.Session()
    # 访问初始页面，获取 Cookies
    response = session.get(newurl, headers=headers,cookies=cookies)

    if response.status_code == 200:
        print(f"成功访问初始页面！{newurl}")

    # 第二步：访问目标页面
    target_url = f"http://mooc1.xtu.edu.cn/mooc-ans/knowledge/cards?clazzid={clazzid}&courseid={courseId}&knowledgeid={chapterId}"

    # 模拟必要的请求头
    headers.update({
        "Referer": newurl,  # 设置 Referer，表明请求来源
    })

    # 使用相同的 session 和头部访问目标页面
    response = session.get(target_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        print(f"成功访问目标页面！{target_url}")
        #print(response.text)  # 输出页面内容
    else:
        print(f"访问目标页面失败，状态码：{response.status_code}")
    #print(response.json().get("filename"))
    objectId = re.findall('"objectid":"(.*?)",', response.text, re.S)
    print(objectId)
    return objectId
def get_download_url(objectid,headers,cookies,newurl):
    headers.update({
        "Referer": newurl,  # 设置 Referer，表明请求来源
    })

    to_download_url = f"http://mooc1.xtu.edu.cn/ananas/status/{objectid}?flag=normal"
    print(to_download_url)
    response = session.get(to_download_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        json_data = response.json()
            
        # 从 JSON 数据中提取文件名
        filename = json_data.get("filename")
        download = json_data.get("download")
        down_name_path = [filename,download]
            
    else:
        print(f"获取下载url，filename失败，状态码：{response.status_code}")
        return None
    return down_name_path
def download_file(download_url,filename,filepath,headers,cookies):
    
    download_path = os.path.join(filepath, filename)
    response = requests.get(download_url, stream=True,headers=headers,cookies=cookies)
    if response.status_code == 200:
        print(f"开始下载文件：{filename}")
        # 保存文件
        with open(download_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"文件下载完成：{filename}")

    else:
        print(f"下载失败，状态码：{response.status_code}")


def pre(url,chapterIds):
    pattern = r'(?<=chapterId=)\d+'  # 匹配 chapterId 后面的数字
    num = re.findall(pattern, url)
    pattern1 = r'.*chapterId='
    front = re.findall(pattern1,url)
    #print(front)
    pattern2 = r'&courseId=.*'
    behind = re.findall(pattern2,url)
    #print(behind)
    newurl = [None] * 100
    #print(newurl)
    for i in range(0,100):
        num[0] = chapterIds[i]
        if num[0] is None:
            num[0] = "0"
        #print(num)
        newurl[i] = front[0] + num[0] + behind[0]
        #get_objectid(num[0],courseId,clazzid,newurl)
    return newurl
def get_chapterId(courseid,clazzid,headers,cookies):
    newurl = f"https://mooc1-2.chaoxing.com/visit/stucoursemiddle?courseid={courseid}&clazzid={clazzid}"
    response = requests.get(newurl,cookies=cookies,headers=headers)
    selector = parsel.Selector(response.text)
    h3s = selector.css('h3.clearfix a::attr(href)')
    chapterIds = [None]*100
    i=0
    for h3 in h3s:
        #print(h3)
        chapterIds[i] = re.findall('chapterId=(.*?)&', h3.get(), re.S)[0]
        i = i + 1
        #print(chapterIds)    
    return chapterIds


if __name__ == "__main__":
    #随便一个章节的url
    url = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }
    #cookie值
    cookies = {

    }
    #设置下载路径
    downloadpath = r""


    params = get_params(url)
    courseId = params.get("courseId")
    clazzid = params.get("clazzid")    
    chapterIds = get_chapterId(courseId,clazzid,headers,cookies)
    chapterIds_lenth = len(list(filter(lambda x: x is not None, chapterIds)))
    print(f"章节列表获取成功，共{chapterIds_lenth}个章节")
    newurl = pre(url,chapterIds)

    for i in range(0,chapterIds_lenth):
        chapterId = chapterIds[i]
        time.sleep(10)
        objectId = get_objectid(chapterId,courseId,clazzid,newurl[i],headers,cookies)
        if objectId is None:
            continue
        for objectid in objectId:
            down_name_path = get_download_url(objectid,headers,cookies,newurl[i])
            filename = down_name_path[0]
            if filename.endswith('.pptx'):
                print("文件是 PPTX 格式")
                download_url = down_name_path[1]
                download_file(download_url,filename,downloadpath,headers,cookies)
                

        

