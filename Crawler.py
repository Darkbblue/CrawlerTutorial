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
	# 数据存储
	data = []
	# 创建保存图片的文件夹
	if not os.path.exists('pic'):
		os.makedirs('pic')

	# url 跳转：顺序修改 url
	for page_index in range(0, 250, 25): # 页码
		url = 'https://movie.douban.com/top250?start={}&filter='.format(page_index)

		# 获得当前页面
		html = get_page(url).text

		# 遍历当前页面的各电影
		html = extract(html, re.compile(r'<ol class="grid_view">(.*?)</ol>', re.S))[0]
		chunks = extract(html, re.compile(r'<li>(.*?)</li>', re.S))
		for i, chunk in enumerate(chunks):
			film_index = page_index + i + 1

			# 对应当前电影的列表项
			info = {}
			info['index'] = film_index

			# 标题
			title_exp = re.compile(r'<span class="title">(.*?)</span>', re.S)
			title_inf = extract(chunk, title_exp)
			info['title'] = title_inf[0]
			print('{}\t{}'.format(film_index, info['title']))

			# 海报
			pic_exp = re.compile(r'<div class="pic">.*?<img.*?src="(.*?)".*?>.*?</div>', re.S)
			pic_url = extract(chunk, pic_exp)
			pic_name = 'pic' + os.path.sep + str(film_index) + ' ' + str(info['title'])
			#get_pic(pic_url[0], pic_name)

			# 导演
			director_exp = re.compile(r'<div class="bd">.*?导演: (.*?)&.*?</div>', re.S)
			director_inf = extract(chunk, director_exp)
			info['director'] = director_inf[0].split(' / ')
			print('\t{}'.format(info['director']))

			# 上映日期+地区+类型
			try:
				general_exp = re.compile(r'<div class="bd">.*?<br>(.*?)</p>.*?</div>', re.S)
				general_inf = extract(chunk, general_exp)[0].replace('&nbsp;', '').split('/')
				date_inf = general_inf[0].replace('\n', '').replace(' ', '')
				region_inf = general_inf[1].split(' ')
				genre_inf = extract(general_inf[2], re.compile(r'(.*)\n', re.S))[0].split(' ')
				info['date'] = date_inf
				info['region'] = region_inf
				info['genre'] = genre_inf
				print('\t{} {} {}'.format(date_inf, region_inf, genre_inf))
			except:
				info['date'] = '0'
				info['region'] = []
				info['genre'] = []

			data.append(info) # 新增列表项

	# 保存记录
	filename = 'info'
	save_json(data, filename)