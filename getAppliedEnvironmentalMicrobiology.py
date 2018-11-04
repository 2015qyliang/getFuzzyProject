# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-03
# Description:
# 1) download papers from "Applied and Environmental Microbiology"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python getAppliedEnvironmentalMicrobiology.py 2018 1 22
'''
# 2013	Volume: 79 Issue: 1-24
# 2014	Volume: 80 Issue: 1-24
# 2015	Volume: 81 Issue: 1-24
# 2016	Volume: 82 Issue: 1-24
# 2017	Volume: 83 Issue: 1-24
# 2018	Volume: 84 Issue: 1-22
# https://aem.asm.org/content/83/10
# re.findall(("content/83/10/.{9}"),html.text)
'''

import os
import PyPDF2
import requests
import re
import wget
import time
import argparse

# parse argument
parser = argparse.ArgumentParser()
parser.add_argument('-y','--year',type=int,dest = 'year',help = "Input which year to download in the journal...")
parser.add_argument('-s','--start',type=int,dest = 'start',help = "Issue start number...")
parser.add_argument('-e','--end',type=int,dest = 'end',help = "Issue end number...")
args = parser.parse_args()

# define main function
def get_project(year,start,end):
	if str(year) == '2013':
		volume = '79'
	elif str(year) == '2014':
		volume = '80'
	elif str(year) == '2015':
		volume = '81'
	elif str(year) == '2016':
		volume = '82'
	elif str(year) == '2017':
		volume = '83'
	elif str(year) == '2018':
		volume = '84'
	for i in range(int(start),int(end)):
		checkURL = 'https://aem.asm.org/content/' + volume + '/' + str(i)
		checkRequest = requests.get(checkURL)
		print("--------------------"*6)
		# check request URL
		if checkRequest.status_code == 200:
			searchPattern = '/content/' + volume + '/' + str(i) + '/'
			pdfUrlList = re.findall("(%s.{1,9})(\" class=\"highwire-cite-linked-title\")"%searchPattern,checkRequest.text)
			print("---- check AEM_url status: ",checkRequest.status_code)
			print("---- pdf urls number : ",len(pdfUrlList))
			aemUrl = 'https://aem.asm.org'
			for pdfurl in pdfUrlList:
				pdfCheckRequest = requests.get(aemUrl + pdfurl[0])
				print("---- check pdf_url status:",aemUrl + pdfurl[0],pdfCheckRequest.status_code)
				hitStrFind = re.findall("([A|a]ccession n)(.{5,90}[P|E|D|S].{5,90})(\.</)",pdfCheckRequest.text)
				print("---- accession searched :", hitStrFind)
				if len(hitStrFind) != 0 and pdfCheckRequest.status_code == 200:
					for hitstr in hitStrFind[0]:
						hitProject = re.search("([P|E|D|S].{5,20})(\">[P|E|D|S])", hitstr)
						print("---- fuzzy projectStr : ",hitProject)
						if str(hitProject) != 'None':
							hitProject = hitProject.group(1)
							print("--*--*-- searched fuzzy projectStr : ",hitProject)
							S16 = re.findall("(16S)",checkRequest.text)
							if len(S16) != 0:
								urlList = aemUrl + pdfurl[0] + '\t' + str(hitProject) + '\t16S\n'
							else:
								urlList = aemUrl + pdfurl[0] + '\t' + str(hitProject) + '\t----\n'
							print("---- writing : ",urlList)
							open('get_papers_project.txt','a',encoding='utf-8').write(urlList)
				else:
					print("---- dont searched fuzzy project in ",aemUrl + pdfurl[0])
					open('failed_log.txt','a',encoding='utf-8').write("failed until " + aemUrl + pdfurl[0] + '\n')
				open('run_list.txt', 'a',encoding='utf-8').write(aemUrl + pdfurl[0] + '\n')
				time.sleep(0.3)

# try ... except ...
try:
	get_project(str(args.year), str(args.start), str(args.end))
except Exception as e:
	raise e
