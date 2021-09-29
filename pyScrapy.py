#! /usr/bin/python3
#written by David Herman
import threading

import argparse
import requests
import regex
import concurrent.futures
from itertools import repeat


def scrape(url):
	print(f"In scrape, the target is {url}")
	#successful_URL = ""
	session = requests.Session()

	r = session.get(url)
	return r

def read_wordlist(args):
	wordlist = args.wordlist
	futures_list = []
	print(f"in read_wordlist {wordlist}")
	with concurrent.futures.ThreadPoolExecutor(args.workers) as executor:
		for word in wordlist:
			print(f'in read_wordlist the word is {word}')
			url = f"{args.url}/{word.strip()}"
			futures = executor.submit(scrape,url)
			futures_list.append(futures)
		#print(f"in read_wordlist {futures}")
	return futures_list

def main():
	parser = argparse.ArgumentParser(description='Scrape a website directory')
	parser.add_argument('url', help='the url to scrape')
	parser.add_argument('wordlist',type=argparse.FileType('r'), help=' The wordlist to scrape with',default="./directory.txt")
	parser.add_argument('--workers',type=int, help='Number of threads to use',default=10,required=False)
	args = parser.parse_args()
	#First pass of the word list
	futures = read_wordlist(args)
	successful_URL = []
	for future in futures:
		if(regex.match(r"(?!403)[3-5](\d{2})",str(future.result().status_code))): 
		#or not regex.search(r"(?<=\.)\w+",url_last[-1])):
			print(F"this url failed {future.result().url} with {future.result().status_code}	")
		
		else: 
			#print(successful_URL)
			successful_URL.append(future.result().url)

	print(str(successful_URL))



if __name__ == "__main__":
	main()