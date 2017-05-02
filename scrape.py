# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

#Get JSON result of italki queries
#'import socket
#import socks
import requests
import json
import re
import os
import sys
import argparse

#TOR SETUP
'''
ipcheck_url = 'http://checkip.amazonaws.com/'
print("ip",requests.get(ipcheck_url).text)
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
noTor = socket.socket
tor = socks.socksocket
#socket.socket = tor
print("Getting TOR ip...")
print("TOR ip",requests.get(ipcheck_url).text)
'''


def drawLoadingBar(val,maximum):
	if val <= maximum:
		val = min(val,maximum) # prevent overshooting
		maxLength = 50
		barLength = int((val/maximum)*maxLength)
		percentage = (val/maximum)*100.0
		if sys.version_info[:2] <= (2, 7):
			barStr = "|"+"█"*barLength + " "*(maxLength-barLength-1)+"|"
		else:
			barStr = "|"+"█"*barLength + "▒"*(maxLength-barLength-1)+"|"
		barStr += " "+ '{0:.2f}'.format(percentage)+"%" + " ("+ str(val)+"/" + str(maximum)+ ")"
		print(barStr+"\r",end="")
	else:
	    print()


#******* MAIN CODE *********
def getDocuments(outputDir,languages,maxPerLang=1000):

	#Create output directories
	try:
		os.makedirs(outputDir)
	except:
		pass
	try:
		os.makedirs(outputDir+"/tokenized")
	except:
		pass

	#Get languages
	for language in languages:

		docsOutput = []

		#Check if some documents have already been downloaded
		# filename = os.path.join(outputDir,language+".json")
		# currentCount = 0
		# try:
		# 	f = open(filename,"r")
		# 	docsOutput = json.load(f)
		# 	f.close()
		# 	currentCount = len(docsOutput)
		# except:
		# 	pass
		currentCount = 0
		print()
		print(language)
		page = currentCount//15
		#page = 50
		while currentCount < maxPerLang:
			#get list of notebooks
			api = "https://www.italki.com/api/notebook?&author_language="+language+"&language="+"english"+"&page="+str(page)
			r = requests.get(api)

			#Check if last page
			if not(json.loads(r.text)['meta']['has_next']):
				print("NO MORE PAGES")
				break

			docs = json.loads(r.text)['data']

			for i,d in enumerate(docs):
				if currentCount > maxPerLang:
					break

				drawLoadingBar(currentCount,maxPerLang)
				currentCount += 1
				#Get full notebook
				#print("getting notebook...")
				url = "https://www.italki.com/api/notebook/"+str(d['id'])+""
				r = requests.get(url)
				try:
					doc = json.loads(r.text)['data']

					#Check id is unique
					goodId = True
					for d in docsOutput:
						if d["id"] == doc["id"]:
							goodId = False
					if goodId:
						#Get full author
						url = "https://www.italki.com/api/user/"+str(doc['author_obj']['id'])+""
						r = requests.get(url)
						author = json.loads(r.text)['data']
						doc['author_obj'] = author
						doc['NL'] = re.sub(r'\([^)]*\)', '',language)
						
						#Tokenize data
						#	TODO
						from nltk.tokenize import TweetTokenizer
						tknzr = TweetTokenizer()
						tk = " ".join(tknzr.tokenize(doc["content"]))

						#Write to file
						import codecs
						f = codecs.open(outputDir+"/tokenized/"+str(doc["id"])+".txt",'w','utf-8')
						f.write(tk)
						f.close()

						#Add index entry
						f = open(outputDir+"/index.csv","a")

						proficiency = 0
						for l in doc["author_obj"]["language_obj_s"]:
							if l["language"] == "english":
								proficiency = l["level"]
						s = str(doc["id"])+".txt,0,"+doc["NL"]+","+str(proficiency)+"\n"
						f.write(s)
						f.close()
				
						docsOutput.append(doc)
					else:
						#print("Duplicate id")
						pass

				except Exception as err:
					print(err)
					import sys
					print(sys.exc_info())

			page+=1


# def main(params,inDir,outDir):
# 	print(outDir)
# 	getDocuments(outDir,params[0]["value"],params[1]["value"])


if __name__ == "__main__":

	print("Getting language list...")
	#Get list of constants
	r = requests.get("https://www.italki.com/i18n/en_us.json?v=v1.2.0")
	constants = json.loads(r.text)
	languages = []
	for c in constants.keys():
		if c.lower() == c:
			languages.append(c)


	#Parse CLI arguments
	parser = argparse.ArgumentParser(description='Download raw documents.')
	parser.add_argument('langs',
						nargs='+', 
						choices=languages,
	                    help='List of languages to download')
	parser.add_argument('-s', '--output-dir',
						required=False,
						default="italki",
	                    help='Directory to output documents')
	parser.add_argument('-r', '--max-per-lang',
						required=False,
						type=int,
						default=1000,
	                    help='Maximum number of documents to be downloaded per language')
	args = parser.parse_args()
	print("Languages valid")


	#Call main code
	print("Creating corpus at :",args.output_dir,"...\n\n")
	getDocuments(args.output_dir,args.langs,args.max_per_lang)
	print("\n\nDONE!")
