# 发送请求所需
import requests
from time import sleep
import random
# 提取网页信息所需
import re
# 保存数据所需
import os
import json


# ----- 工具组件 ----- #


def get_page(url):
	'''
	获取单个 url 的资源
	:para url: str
	:return: 一个包装后的对象，一般需要取 .text 才是相应文本
	'''
	# headers 伪装
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
	}
	# 增大请求间隔
	sleep(random.uniform(3, 7))

	# 发送正式请求
	i = 0  # 重试计数器
	while i < 5:
		try:
			response = requests.get(url, headers=headers, timeout=5)
			if response.status_code == 200:  # 若正常获取则返回结果
				return response
			else:
				raise requests.exceptions.RequestException
		except requests.exceptions.RequestException:
			print('!reconnecting!')
			sleep(random.uniform(0.5, 1))
			i += 1  # 若出现错误，则进行有限次数重试
	return None  # 超出重试次数后则放弃本次获取
				 # 用户可以选择进行其他处理，如跳过本页面


def get_pic(url, name):
	'''
	获取图片，并按照给定名称进行保存
	:para url: 图片资源的 url
	:para name: 文件名，不包含扩展名部分
	'''
	filename = name + '.jpg'
	if os.path.exists(filename):  # 跳过已下载的图片
		return
	pic = get_page(url).content
	with open(filename, 'wb+') as f:
		f.write(pic)


def extract(text, exp):
	'''
	使用给定的正则表达式，从给定的文本中提取信息
	:para text: str
	:para exp: re.compile() 的返回值类型
	:return: list，返回全部符合正则表达式的匹配结果
	'''
	result = re.findall(exp, text)
	return result


def save_json(content, name):
	'''
	保存内容为 json 文件
	:para content: list or dict
	:para name: str
	'''
	filename = name + '.json'
	j_file = json.dumps(content)  # 转换到 json 文件
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(j_file)


# ----- 主逻辑 ----- #


if __name__ == '__main__':
	data = [] # 数据整体存储，初始化为空
	if not os.path.exists('pic'): # 创建保存图片的文件夹
		os.makedirs('pic')

	for page_index in range(1, 11): # 页码
		# 计算 URL
		if page_index == 1: # 首页
			url = 'http://www.mtime.com/top/movie/top100/'
		else: # 后续页
			url = 'http://www.mtime.com/top/movie/top100/' + 'index-' + str(page_index) + '.html'

		html = get_page(url).text # 获得当前页面

		for offset_index in range(1, 11): # 提取当前页面的各电影信息
			mov_index = offset_index + 10 * (page_index - 1) # 电影的完整序号
			print('\n'+str(mov_index))
			chunk_exp = re.compile(r'<li.*?<em>'+str(mov_index)+r'</em>.*?<div(.*?)mov_point.*?</div>', re.S) # 获取整块文本
			chunk = extract(html, chunk_exp)[0]

			info = {} # 新增列表项

			# 提取具体信息
			# 海报
			pic_exp = re.compile(r'mov_pic.*?img.*?src="(.*?)"', re.S)
			pic_url = extract(chunk, pic_exp)
			pic_name = 'pic' + os.path.sep + str(mov_index)
			download_pic(pic_url[0], pic_name)

			# 标题
			title_exp = re.compile(r'h2.*?_blank">(.*?)</a>', re.S)
			title_inf = extract(chunk, title_exp)
			info["title"] = title_inf[0]
			print(info["title"])

			# 导演
			director_exp = re.compile(r'导演.*?_blank">(.*?)</a>', re.S)
			director_inf = extract(chunk, director_exp)
			info["director"] = director_inf[0]
			print(info["director"])

			# 主演
			actor_exp0 = re.compile(r'主演.*?</p>.*?类型', re.S)
			actor_chunk = extract(chunk, actor_exp0)
			if actor_chunk: # 若不为空
				actor_exp1 = re.compile(r'_blank">(.*?)</a>', re.S)
				actor_inf = extract(actor_chunk[0], actor_exp1)
				info["actor"] = actor_inf # 类型为列表
			else:
				info["actor"] = [] # 空列表
			print(info["actor"])

			# 类型
			genre_exp0 = re.compile(r'类型(.*?)mt3', re.S)
			genre_chunk = extract(chunk, genre_exp0)
			if genre_chunk: # 若不为空
				genre_exp1 = re.compile(r'_blank">(.*?)</a>', re.S)
				genre_inf = extract(genre_chunk[0], genre_exp1)
				info["genre"] = genre_inf # 类型为列表
			else:
				info["genre"] = [] # 空列表
			print(info["genre"])

			# 简介
			summary_exp = re.compile(r'mt3">(.*?)</p>')
			summary_inf = extract(chunk, summary_exp)
			info["summary"] = summary_inf[0]
			print(info["summary"])

			data.append(info) # 新增列表项

	# 保存记录
	filename = 'info'
	save_json(data, filename)