#! /usr/bin/python3

import threading

import argparse
import requests
import regex



def scrape(args,session):
	successful_URL = []
	for word in args.wordlist:
		word = word.strip()
		url=f"{args.url}/{word}"
		#print(url)
		r = session.get(url)
		#
		if(regex.match(r"(?!403)4(\d\d)",str(r.status_code))):
			pass	
		else: 
			print(f"{url} responds with {r.status_code}")
			successful_URL.append(url)
			scrape(args,session)
	print(successful_URL)

def main():
	parser = argparse.ArgumentParser(description='Scrape a website directory')
	parser.add_argument('url', help='the url to scrape')
	parser.add_argument('wordlist',type=argparse.FileType('r'), help=' The wordlist to scrape with',default="./directory.txt")

	s = requests.Session()
	args = parser.parse_args()
	scrape(args,s)
if __name__ == "__main__":
	main()