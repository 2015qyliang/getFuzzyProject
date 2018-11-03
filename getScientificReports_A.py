# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-03
# Description:
# 1) download papers from "Scientific Report"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python getScientificReports_A.py 2016 18408 39929
'''
# version-A ---- This script
# https://www.nature.com/articles/srep03569
# 2013	srep01023	srep03568	|	1023	3568
# 2014	srep03572	srep07593	|	3572	7593
# 2015	srep07615	srep18634	|	7615	18634
# 2016	srep18408	srep39929	|	18408	39929
# 2017	srep39875	srep46762	|	39875	46762
# from 1023 to 46762
# ------------------------
# version-B
# https://www.nature.com/articles/s41598-018-34448-x
# 2017	s41598-017-01206-4	s41598-017-18356-0
# 2018	s41598-017-18550-0	s41598-018-34693-0
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
parser.add_argument('-s','--start',type=int,dest = 'start',help = "DOI start number...")
parser.add_argument('-e','--end',type=int,dest = 'end',help = "DOI end number...")
args = parser.parse_args()

# define main function
def get_project(year,start,end):
	for i in range(int(start),int(end)):
		checkURL = 'https://www.nature.com/articles/srep' + str(i).zfill(5)
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

