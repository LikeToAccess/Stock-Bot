# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Checks for stock of AMD products
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 12-03-2020
# version           : v1.0
# usage             : python main.py
# notes             : 
# license           : MIT
# py version        : 3.7.8 (must run on 3.6 or higher)
#==============================================================================
from time import sleep
from functions import *


os.system("cls")
urls = read_file("urllist.txt")

running = True
while running:
	urls = read_file("urllist.txt")
	for url in urls:
		if url != "" and url[:1] != "#":
			threaded_function = threading.Thread(target=check_stock, args=(url,))
			value = threaded_function.start()
			sleep(20)
