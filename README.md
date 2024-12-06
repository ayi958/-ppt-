# 自动下载PPT文件工具

这是一个Python脚本，用于从指定的在线学习平台下载PPT文件。该工具通过自动化访问多个章节页面，提取必要的信息，生成下载链接，并下载 `.pptx` 格式的文件。

## 功能

- 自动提取课程章节的 `chapterId`、`courseId`、`clazzid` 等参数。
- 根据获取的 `objectId` 生成文件的下载链接。
- 下载 `.pptx` 格式的文件，并保存到本地指定目录。
- 仅下载符合条件的文件格式（`.pptx`）。

## 安装要求

- Python 3.x
- 安装以下依赖库：
    - `requests`
    - `beautifulsoup4`
    - `lxml`
    - `parsel`

安装依赖：

```bash
pip install requests beautifulsoup4 lxml parsel
```

## 配置脚本

- url：设置课程页面的 URL，通常可以通过浏览器获取该 URL。
- cookies：使用浏览器的开发者工具打开需要获取的资源的页面获取有效的 Cookies 信息。
- downloadpath：设置文件下载保存的本地路径。

## 运行脚本

```bash
python download_ppt.py
```
