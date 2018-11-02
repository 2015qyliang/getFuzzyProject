# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-1
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
		urlList = []
		checkURL = 'https://www.frontiersin.org/articles/10.3389/fmicb.' + str(year) + '.' + str(i).zfill(5) + '/full'
		checkRequest = requests.get(checkURL)
		print("--------------------"*6)
		# check request URL
		print("---- check url status: ",checkRequest.status_code)
		if checkRequest.status_code != 404:
			# assemble pdfURL
			pdfURL = 'http://sci-hub.tw/10.3389/fmicb.' + str(year) + '.' + str(i).zfill(5)
			checkPdfDownload = re.search('(iframe src = ")(.*\.pdf)(#view=FitH)',requests.get(pdfURL).text)
			downloadurl = checkPdfDownload.group(2)
			print("---- pdf url : ", downloadurl)
			# check download_url format
			if 'http' not in downloadurl:
				downloadurl = 'https:' + downloadurl
			if 'tree.sci-hub' in downloadurl:
				print("---- this url failed & wont get pdf ")
				continue
			print("---- checked pdf url : ",downloadurl)
			pdfTile = str(year) + '_' + str(i).zfill(5) + '.pdf'
			wget.download(downloadurl,out = pdfTile)
			print("---- pdf file downloaded : ",pdfTile)
			# get file size (B)
			fileSize = os.path.getsize(pdfTile)
			print("---- checking file size : %d Kb "%(fileSize/1024))
			# checked file-size to filted pdf file, which failed downloading
			if fileSize > 1024*200:
				# file size > 200 Kb
				pdffile = open(pdfTile,'rb')
				# parse pdfFiles & mining project
				pdfobject = PyPDF2.PdfFileReader(pdffile,strict=False)
				page_count = pdfobject.getNumPages()
				print("---- pdf file parsed ")
				for pgi in range(0,page_count):
					pagetext = str(pdfobject.getPage(pgi).extractText()).replace('\n',"").replace('\r',"")
					hitStrFind = re.findall("(accessionn)(.{5,15}[P|E|D|S].{5,90})",str(pagetext))
					if len(hitStrFind) != 0:
						hitProject = re.search("([P|E|D|S].{5,20})", hitStrFind[0][1].split('.')[0])
						print("---- fuzzy projectStr : ",hitProject)
						if str(hitProject) != 'None':
							hitProject = hitProject.group(1)
							print("---- searched fuzzy projectStr : ",hitProject)
							S16 = re.findall("(16S)",pagetext)
							if len(S16) != 0:
								urlList.append(checkURL + '\t' + str(hitProject) + '\t16S\n')
							else:
								urlList.append(checkURL + '\t' + str(hitProject) + '\t----\n')
					else:
						hitStrFind = re.findall("(EuropeanNucleotideArchive)(.*[P|E|D|S].{5,90})",str(pagetext))
						if len(hitStrFind) != 0:
							hitProject = re.search("([P|E|D|S].{5,20})", hitStrFind[0][1].split('.')[0])
							print("---- fuzzy projectStr : ", hitProject)
							if str(hitProject) != 'None':
								hitProject = hitProject.group(1)
								print("---- searched fuzzy projectStr : ", hitProject)
								S16 = re.findall("(16S)", pagetext)
								if len(S16) != 0:
									urlList.append(checkURL + '\t' + str(hitProject) + '\t16S\n')
								else:
									urlList.append(checkURL + '\t' + str(hitProject) + '\t----\n')
				pdffile.close()
				print("---- writing : ",urlList)
				open('get_papers_project.txt','a',encoding='utf-8').writelines(urlList)
			else:
				print("---- pdf file size too small !!! ")
			os.remove(pdfTile)
		else:
			open('failed_log.txt','a',encoding='utf-8').write("failed until " + str(i).zfill(5) + '\n')
		open('run_list.txt', 'a',encoding='utf-8').write(checkURL + '\n')
		time.sleep(0.3)

# try ... except ...
try:
	get_project(str(args.year), str(args.start), str(args.end))
except Exception as e:
	raise e