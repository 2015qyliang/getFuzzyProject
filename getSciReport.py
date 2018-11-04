# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-03
# Description:
# 1) download papers from "SciReport"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python getSciReport.py

import os
import requests
import re
import wget
import time
import argparse

# pages 1 -1579

# parse argument
parser = argparse.ArgumentParser()
parser.add_argument('-s','--start',type=int,dest = 'start',help = "Pages start number...")
parser.add_argument('-e','--end',type=int,dest = 'end',help = "Pages end number...")
args = parser.parse_args()

# define main function
def get_project(start,end):
	for i in range(int(start),int(end)):
		PdfListUrl = 'https://www.nature.com/srep/articles?searchType=journalSearch&sort=PubDate&type=article&page=' + str(i)
		checkRequest = requests.get(PdfListUrl)
		print("-----------"*6)
		# check request URL
		if checkRequest.status_code == 200:
			pdfUrlList = re.findall("(<a href=\")(/articles/.{4,19})(\" itemprop=\"url\" data-track)",checkRequest.text)
			print("---- pdf urls number : ",len(pdfUrlList))
			# print(pdfUrlList)
			scireportUrl = 'https://www.nature.com'
			for pdfurl in pdfUrlList:
				pdfCheckRequest = requests.get(scireportUrl + pdfurl[1])
				print("--------------------------------")
				print("---- current pages:",str(i))
				print("---- check SciReport_url status: ",checkRequest.status_code)
				print("---- check pdf_url status:",scireportUrl + pdfurl[1],pdfCheckRequest.status_code)
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
								urlList = scireportUrl + pdfurl[1] + '\t' + str(hitProject) + '\t16S\n'
							else:
								urlList = scireportUrl + pdfurl[1] + '\t' + str(hitProject) + '\t----\n'
							print("---- writing : ",urlList)
							open('get_papers_project.txt','a',encoding='utf-8').write(urlList)
				else:
					print("---- dont searched fuzzy project in ",scireportUrl + pdfurl[1])
					open('failed_log.txt','a',encoding='utf-8').write("failed until " + scireportUrl + pdfurl[1] + '\n')
				open('run_list.txt', 'a',encoding='utf-8').write(scireportUrl + pdfurl[1] + '\n')
				time.sleep(0.3)

# try ... except ...
try:
	get_project(str(args.start), str(args.end))
except Exception as e:
	raise e
