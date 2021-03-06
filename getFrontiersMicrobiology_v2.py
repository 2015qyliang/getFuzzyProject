# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-03
# Description:
# 1) download papers from "Fronters in Microbiology"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python get_FrontersMicrobiology.py 2018 1 1700

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
parser.add_argument('-s','--start',type=int,dest = 'start',help = "DOI start number...")
parser.add_argument('-e','--end',type=int,dest = 'end',help = "DOI end number...")
args = parser.parse_args()

# define main function
def get_project(year,start,end):
	for i in range(int(start),int(end)):
		checkURL = 'https://www.frontiersin.org/articles/10.3389/fmicb.' + str(year) + '.' + str(i).zfill(5) + '/full'
		checkRequest = requests.get(checkURL)
		print("--------------------"*6)
		# check request URL
		print("---- check url status: ",checkRequest.status_code)
		print("---- papers : ",str(year) + '.' + str(i).zfill(5))
		hitStrFind = re.findall("(accession n)(.{5,15}[P|E|D|S].{5,90})(\.</)",checkRequest.text)
		if len(hitStrFind) != 0 and checkRequest.status_code == 200:
			hitProject = re.search("([P|E|D|S].{5,20})", hitStrFind[0][1].split('.')[0])
			print("---- fuzzy projectStr : ",hitProject)
			if str(hitProject) != 'None':
				hitProject = hitProject.group(1)
				print("---- searched fuzzy projectStr : ",hitProject)
				S16 = re.findall("(16S)",checkRequest.text)
				if len(S16) != 0:
					urlList = checkURL + '\t' + str(hitProject) + '\t16S\n'
				else:
					urlList = checkURL + '\t' + str(hitProject) + '\t----\n'
				print("---- writing : ",urlList)
				open('get_papers_project.txt','a',encoding='utf-8').write(urlList)
		else:
			print("---- dont searched fuzzy project ")
			open('failed_log.txt','a',encoding='utf-8').write("failed until " + str(i).zfill(5) + '\n')
		open('run_list.txt', 'a',encoding='utf-8').write(checkURL + '\n')
		time.sleep(0.3)

# try ... except ...
try:
	get_project(str(args.year), str(args.start), str(args.end))
except Exception as e:
	raise e