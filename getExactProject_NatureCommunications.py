# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-13
# Description:
# 1) download papers from "Nature Communications"
# 2) parsing pdf file and extract fuzzy projectNumber, related microbial community study
# using deome: python getSciReport.py -s 1 -e 420

import requests
import re
import wget
import time
import argparse

# pages 1 - 420

# parse argument
parser = argparse.ArgumentParser()
parser.add_argument('-s','--start',type=int,dest = 'start',help = "Pages start number...")
parser.add_argument('-e','--end',type=int,dest = 'end',help = "Pages end number...")
args = parser.parse_args()

# define main function
def get_project(start,end):
	for i in range(int(start),int(end)):
		PdfListUrl = 'https://www.nature.com/ncomms/articles?searchType=journalSearch&sort=PubDate&type=article&page=' + str(i)
		checkRequest = requests.get(PdfListUrl)
		print("-----------"*6)
		# check request URL
		if checkRequest.status_code == 200:
			pdfUrlList = re.findall("(<a href=\")(/articles/.{4,19})(\" itemprop=\"url\" data-track)",checkRequest.text)
			print("---- pdf urls number : ",len(pdfUrlList))
			# print(pdfUrlList)
			nctUrl = 'https://www.nature.com'
			for pdfurl in pdfUrlList:
				print("--------------------------------")
				print("---- current pages:",str(i))
				print("---- check pdf_url:",nctUrl + pdfurl[1])
				text = requests.get(nctUrl + pdfurl[1]).text
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
					open('getExactProject.txt','a',encoding='utf-8').write(nctUrl + pdfurl[1] + '\t' + Prjstr +  '\t' + SRPstr + '\t' + '16S' + 
						'\t' + SAMNstr + '-' + SRXstr + '\n')
				else:
					open('getExactProject.txt','a',encoding='utf-8').write(nctUrl + pdfurl[1] + '\t' + Prjstr + '\t' + SRPstr + '\t' + '---' + 
						'\t' + SAMNstr + '-' + SRXstr + '\n')
				time.sleep(0.3)



# try ... except ...
try:
	get_project(str(args.start), str(args.end))
except Exception as e:
	raise e
