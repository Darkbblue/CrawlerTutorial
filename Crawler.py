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


if __name__ == '__main__':
	html = get_page('http://www.mtime.com/top/movie/top100/').text
	print(html)
	print('\n')