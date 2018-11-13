# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-03
# Description:
# 1) download papers from "Applied and Environmental Microbiology"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python getExactProject_AEM.py -y 2018 -s 1 -e 22

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
			# print(pdfUrlList)
			aemUrl = 'https://aem.asm.org'
			for pdfurl in pdfUrlList:
				url = aemUrl + pdfurl[0]
				print("---- checked url:",i,url)
				text = requests.get(url).text
				hitPrjList = re.findall("PRJ[N|E][A|B]\d{4,6}",text)
				hitSRPList = re.findall("SRP[\d|\s]\d{4,6}",text)
				hitSAMNList = re.findall("SAMN\d{6,9}",text)
				hitSRXList = re.findall("SR[R|X|A]\d{5,8}",text)
				Prjstr = "-".join(hitPrjList)
				SRPstr = "-".join(hitSRPList)
				SAMNstr = "-".join(hitSAMNList)
				SRXstr = "-".join(hitSRXList)
				S16 = re.search("\s16S\s",text)
				if len(str(S16)) != 0:
					print("**** seaerched string:",Prjstr,SRPstr,SAMNstr,SRXstr)
					open('getExactProject_2.txt','a',encoding='utf-8').write(url + '\t' + Prjstr +  '\t' + SRPstr + '\t' + '16S' + 
						'\t' + SAMNstr + '-' + SRXstr + '\n')
				else:
					open('getExactProject_2.txt','a',encoding='utf-8').write(url + '\t' + Prjstr + '\t' + SRPstr + '\t' + '---' + 
						'\t' + SAMNstr + '-' + SRXstr + '\n')
				time.sleep(0.3)

# try ... except ...
try:
	get_project(str(args.year), str(args.start), str(args.end))
except Exception as e:
	raise e