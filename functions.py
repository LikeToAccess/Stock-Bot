from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from threading import Thread
import os
import time
import urllib
import threading


def read_file(filename):
	with open(filename, "r") as f:
		lines = f.read().split("\n")
	return lines

def write_file(filename, msg):
	with open(filename, "w") as f:
		f.write(msg)

def append_file(filename, msg):
	with open(filename, "a") as f:
		f.write(msg)

def remove_pattern(msg, patterns):
	for pattern in patterns:
		msg = msg.replace(pattern,"")
		#print(msg)
	return msg

def format(url, value):
	current_time = time.localtime()
	current_time = time.strftime("%H:%M:%S", current_time)
	if "https://www." in url:
		vendor = url.split("https://www.")[1].split(".com/")[0]
	elif "https://shop." in url:
		vendor = url.split("https://shop.")[1].split(".com/")[0]
	if "UNKNOWN" in value or "error" in value:
		status = "error"
	else:
		status = "info"
	value = value.split("\"")
	data = f"[{current_time}] {status} :: [{vendor}] [{value[1]}] :: {value[2][4:]}"
	return data

def beautifulsoup_scraper(url, tag="class", anchor=["data",""]):
	req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})
	try:
		page_source = urlopen(req).read()
	except urllib.error.URLError as e:
		return str(str(e))
	page_soup = soup(page_source, "html.parser")
	containers = page_soup.find_all(tag, {anchor[0]:anchor[1]})
	return str(containers)

def get_name(url, *args):
	#print(url)
	if "newegg" in url:
		name_containers = beautifulsoup_scraper(url, "h1", ["class","product-title"])
	elif "amazon" in url:
		name_containers = beautifulsoup_scraper(url, "span", ["id","productTitle"])
		#print(name_containers)
	elif "microcenter" in url:
		name_containers = beautifulsoup_scraper(url, "span", ["class","ProductLink_"])
	elif "amd" in url:
		name_containers = beautifulsoup_scraper(url, "h2", ["",""])
	else:
		name_containers = beautifulsoup_scraper(url, args[0], args[1])
		if name_containers == "[]":
			name_containers = False
	return remove_pattern(name_containers, [
		"[<h1 class=\"product-title\">",
		"</h1>]",
		"[<span class=\"a-size-large product-title-word-break\" id=\"productTitle\">",
		"\n",
	])

def get_stock(url, *args):
	if "newegg" in url:
		containers_list = [
			beautifulsoup_scraper(url, "div", ["class","product-buy"]),
			beautifulsoup_scraper(url, "div", ["class","flags-body has-icon-left fa-exclamation-triangle"]),
			beautifulsoup_scraper(url, "div", ["class","flags-body has-icon-left fa-star"]),
		]
	elif "amazon" in url:
		containers_list = [
			beautifulsoup_scraper(url, "span", ["class","a-size-medium a-color-price"]),
			beautifulsoup_scraper(url, "div", ["id","outOfStock"]),
			beautifulsoup_scraper(url, "span", ["data-action","show-all-offers-display"]),
			beautifulsoup_scraper(url, "span", ["class","a-declarative"]),
		]
	elif "microcenter" in url:
		containers_list = [
			beautifulsoup_scraper(url, "span", ["class","inventoryCnt"]),
		]
	elif "amd" in url:
		containers_list = [
			beautifulsoup_scraper(url, "p", ["class","product-out-of-stock"]),
			beautifulsoup_scraper(url, "div", ["class","dr_stockStatus cartLineItem"]),
		]
	for containers in containers_list:
		#print(f"containers: {containers}")
		containers = str(containers)
		stock_containers = containers
		in_stock = get_stock_value(stock_containers)
		if in_stock[0]:
			return in_stock
	return in_stock

def get_stock_value(stock_containers):
	stock_containers = stock_containers.lower()
	#print(stock_containers)
	if " out" in stock_containers or "out " in stock_containers or "unavailable" in stock_containers:
		return True, "OUT OF STOCK"
	elif "backordered" in stock_containers:
		return True, "BACKORDERED"
	elif "in stock" in stock_containers or "add to cart" in stock_containers or "buy now" in stock_containers or "available" in stock_containers:
		return True, "IN STOCK"
	else:
		#print(f"\n\n{stock_containers}\n\n")
		return False, "UNKNOWN"

def check_stock(url):
	stock = get_stock(url)
	name = get_name(url)
	#print(name)
	#print(stock)
	if not stock or name == []:
		return False
	data = "\"{}\" is {}".format([name[:50].strip()+"..." if len(name) > 30 else name][0], stock[1])
	formated_data = format(url, data)
	print(formated_data)
	if "IN STOCK" in formated_data:
		os.system(f"python \"notify.py\" {formated_data}")
	return data
	
if __name__ == "__main__":
	print("Wrong module, switchihng to \"main.py\"...")
	os.system("python main.py")
