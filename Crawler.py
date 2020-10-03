# 发送请求所需
import requests
from time import sleep
import random
# 提取网页信息所需
import re
# 保存数据所需
import os
import json

# ---------------------------- #
# 根据传入的 URL 发送 GET 申请
# 返回类型需要再取 .text 对象才是相应文本
def get_page(url):
	# headers 伪装
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
	}
	# 增大请求间隔
	sleep(random.uniform(3, 7))

	# 发送正式请求
	i = 0 # 重试计数器
	while i < 5:
		try:
			response = requests.get(url, headers=headers, timeout=5)
			if response.status_code == 200: # 若正常获取则返回结果
				return response
			else:
				raise requests.exceptions.RequestException
		except requests.exceptions.RequestException:
			print('!reconnecting!')
			sleep(random.uniform(0.5, 1))
			i += 1 # 若出现错误，则进行有限次数重试
	return None # 超出重试次数后则放弃本次获取
				# 用户可以选择进行其他处理，如跳过本页面

# 根据传入的文本和正则表达式进行信息提取
# 返回类型是一个列表
def extract(html, exp):
	result = re.findall(exp, html)
	return result

# 根据传入的 URL 获取图片，并根据传入的名称保存图片
def download_pic(url, name):
	filename = name + '.jpg' # 完成文件名
	if os.path.exists(filename): # 跳过已下载的图片
		return
	pic = get_page(url).content # 图片内容
	with open(filename, 'wb+') as f: # 写入文件
		f.write(pic)

# 根据传入的文件内容和文件名保存 json 文件
def save_json(content, filename):
	j_file = json.dumps(content) # 转换到 json 文件
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(j_file)

# --------------------------------- #

if __name__ == '__main__':
	html = get_page('http://www.mtime.com/top/movie/top100/').text
	print(html)
	print('\n')