#!/usr/bin/env python3

import argparse
import pytz
from datetime import datetime
import csv


from bs4 import BeautifulSoup

def main():
	parser = argparse.ArgumentParser(description="Extract Facebook comments from file")
	parser.add_argument("ifile", type=str)
	parser.add_argument("--timezone", type=str, default="Europe/Moscow")
	parser.add_argument("--include-replies", action="store_true")
	parser.add_argument("ofile", type=str)
	args = parser.parse_args()

	with open(args.ifile, "r") as f:
		data = f.read()
	if not data:
		return
	tz = pytz.timezone(args.timezone)
	soup = BeautifulSoup(data)
	comments = soup.findAll("div", {"aria-label": "Comment"})
	if args.include_replies:
		comments += soup.findAll("div", {"aria-label": "Comment reply"})
	with open(args.ofile, "w", newline="") as of:
		writer = csv.writer(of, delimiter=",", quotechar="\"")
		writer.writerow(["timestamp", "name", "comment"])
		for comment in comments:
			try:
				livetimestamp = comment.find("abbr", {"class": "livetimestamp"})["data-utime"]
				iso_time = datetime.fromtimestamp(int(livetimestamp), tz).strftime("%Y-%m-%d %H:%M:%S")
				name = comment.find("a", {"class": "_6qw4"}).contents[0]
				body = comment.find("span", {"class": "_3l3x"}).find("span").contents[0]
				writer.writerow([iso_time, name, body])
			except Exception:
				pass

if __name__ == "__main__":
	main()
