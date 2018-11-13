# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-13
# Description:
# 1) download papers from "Fronters in Microbiology"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python getExactProject_FronterMicrobiology.py -y 2018 -s 1 -e 2800

# 2018 1 - 2800
# 2017 1 - 2658
# 2016 1 - 2205
# 2015 1 - 1528
# 2014 1 - 722
# 2013 1 - 418

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
		if checkRequest.status_code == 200:
			print("---- check url status: ",checkRequest.status_code)
			print("---- papers : ",str(year) + '.' + str(i).zfill(5))
			text = checkRequest.text
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
				open('getExactProject.txt','a',encoding='utf-8').write(checkURL + '\t' + Prjstr +  '\t' + SRPstr + '\t' + '16S' +
					'\t' + SAMNstr + '-' + SRXstr + '\n')
			else:
				open('getExactProject.txt','a',encoding='utf-8').write(checkURL + '\t' + Prjstr + '\t' + SRPstr + '\t' + '---' +
					'\t' + SAMNstr + '-' + SRXstr + '\n')
			time.sleep(0.3)

# try ... except ...
try:
	get_project(str(args.year), str(args.start), str(args.end))
except Exception as e:
	raise e