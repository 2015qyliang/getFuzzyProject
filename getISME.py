# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-03
# Description:
# 1) download papers from "ISME"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python getISME.py

import os
import requests
import re
import wget
import time

# define main function
def get_project():
	for i in range(1,50):
		PdfListUrl = 'https://www.nature.com/ismej/articles?searchType=journalSearch&sort=PubDate&page=' + str(i)
		checkRequest = requests.get(PdfListUrl)
		print("-----------"*6)
		# check request URL
		if checkRequest.status_code == 200:
			pdfUrlList = re.findall("(<a href=\")(/articles/.{4,19})(\" itemprop=\"url\" data-track)",checkRequest.text)
			print("---- check AEM_url status: ",checkRequest.status_code)
			print("---- pdf urls number : ",len(pdfUrlList))
			# print(pdfUrlList)
			ismeUrl = 'https://www.nature.com'
			for pdfurl in pdfUrlList:
				pdfCheckRequest = requests.get(ismeUrl + pdfurl[1])
				print("---- check pdf_url status:",ismeUrl + pdfurl[1],pdfCheckRequest.status_code)
				hitStrFind = re.findall("([A|a]ccession n)(.{5,90}[P|E|D|S].{5,90})(\.</)",pdfCheckRequest.text)
				print("---- accession searched :", hitStrFind)
				if len(hitStrFind) != 0 and pdfCheckRequest.status_code == 200:
					for hitstr in hitStrFind[0]:
						hitProject = re.search("(\s[P|E|D|S].{5,15}[^\)])", hitstr)
						print("---- fuzzy projectStr : ",hitProject)
						if str(hitProject) != 'None':
							hitProject = hitProject.group(1)
							print("--*--*-- searched fuzzy projectStr : ",hitProject)
							S16 = re.findall("(16S)",checkRequest.text)
							if len(S16) != 0:
								urlList = ismeUrl + pdfurl[1] + '\t' + str(hitProject) + '\t16S\n'
							else:
								urlList = ismeUrl + pdfurl[1] + '\t' + str(hitProject) + '\t----\n'
							print("---- writing : ",urlList)
							open('get_papers_project.txt','a',encoding='utf-8').write(urlList)
				else:
					print("---- dont searched fuzzy project in ",ismeUrl + pdfurl[1])
					open('failed_log.txt','a',encoding='utf-8').write("failed until " + ismeUrl + pdfurl[1] + '\n')
				open('run_list.txt', 'a',encoding='utf-8').write(ismeUrl + pdfurl[1] + '\n')
				time.sleep(0.3)

# try ... except ...
try:
	get_project()
except Exception as e:
	raise e
