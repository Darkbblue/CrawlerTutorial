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
#		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate, br',
#		'Accept-Language': 'zh-CN,zh;q=0.9',
#		'Cache-Control': 'max-age=0',
#		'Connection': 'keep-alive',
		'Cookie': '_userCode_=2020103141518275; _userIdentity_=20201031415185687; homePageType=B; _tt_=E3E7E8FFD8DAEFF072B7611A4E334CE5; DefaultCity-CookieKey=290; userId=0; defaultCity=%25E5%258C%2597%25E4%25BA%25AC%257C290; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1601705718; strIdCity=China_Beijing; __utma=196937584.942153368.1601705718.1601705718.1601705718.1; __utmc=196937584; __utmz=196937584.1601705718.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmt_~1=1; maxShowNewbie=2; _userCode_=20201031415296208; _userIdentity_=20201031415292744; __utmb=196937584.4.10.1601705718; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1601705872',
#		'Host': 'movie.douban.com',
#		'Sec-Fetch-Dest': 'document',
#		'Sec-Fetch-Mode': 'navigate',
#		'Sec-Fetch-Site': 'none',
#		'Sec-Fetch-User': '?1',
#		'Upgrade-Insecure-Requests': 1,
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