#!/usr/bin/env python

# Dependencias
import sys
from queue import LifoQueue 
from functools import reduce
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

banner = """
 ____                    __        __   _     
| __ ) _   _ ___  ___ __ \ \      / /__| |__  
|  _ \| | | / __|/ __/ _` \ \ /\ / / _ \ '_ \ 
| |_) | |_| \__ \ (_| (_| |\ V  V /  __/ |_) |
|____/ \__,_|___/\___\__,_| \_/\_/ \___|_.__/ 

Many pages make a thick book.

Author: Gabriela Bezerra, Guilherme Araújo, Ítalo Bruno, Pedro Moura.
"""

# SCRIPT INFO
scriptname = "crawler_busca_web"
param1 = "<https://www.origem.com>"
param2 = "<https://www.destino.com>"
param3 = "[28]"
usage = "usage: ./"+scriptname+" "+param1+" "+param2+" "+param3+"\n"


# INPUT CHECK
# Params verification
verify_params_quant = len(sys.argv) != 4
if verify_params_quant:
    exit(usage)
    
param1_verify = len(urlparse(sys.argv[1]).netloc) == 0
param2_verify = len(urlparse(sys.argv[2]).netloc) == 0
param3_verify = len(sys.argv[3]) == 0 or int(sys.argv[3]) == None
if param1_verify or param2_verify or param3_verify:
    exit(usage)

# Initial URLs
origem = sys.argv[1]
destino = sys.argv[2]

# Search Limit
limit = int(sys.argv[3])


# DATA STRUCTURES
# Process Structure
stack = LifoQueue() 
# Seen URLs Dictionary
seen_urls = []

# FUNCTIONS
def depth_first_search(origin_url, destiny_url):
    
    stack.put(origin_url)  # start to search
    
    dfs_counter = 0

    path_to_destiny = []

    while (not stack.empty() and dfs_counter < limit):
        dfs_counter += 1
        print("\n🔎 depth first search number",dfs_counter,"of",limit)
        
        # Proccess URL and remove it from Stack
        current_url = stack.get()
        
        print("🧠 processing",current_url)
        print("🎲 stack has",stack.qsize(),"items")

        if (never_seen(current_url)):
            seen_urls.append(current_url)
            path_to_destiny.append(current_url)

            if current_url == destiny_url:
                return path_to_destiny
        
            # Add its children URLs to Stack
            children_urls = get_children_urls_from(current_url)
            if len(children_urls) == 0:
                path_to_destiny.pop()
            else:
                max_new_size = stack.qsize()+len(children_urls)
                for url in children_urls:
                    if (never_seen(url)): 
                        stack.put(url) 
                discarded_amount = max_new_size - stack.qsize()
                print("🎲 stack now has",stack.qsize(),"items. Discarded",discarded_amount,"urls (already seen).")   

def never_seen(url):
    has_not_be_seen = True
    for seen in seen_urls:
            if url == seen or url == seen+"/" or url+"/" == seen:
                has_not_be_seen = False    
    return has_not_be_seen

def sequencify_list(list, separator=" > "):
    return reduce(lambda ac,element: ac+element+separator,list, "")[:-2]

def map_path_to_url(path,url):
    if ("http" not in path):
        domain = urlparse(url)[1] if urlparse(url)[1][-1:] != "/" else urlparse(url)[1][:-1]
        fixed_path = path.replace("//","/")
        return urlparse(url)[0]+"://"+domain+fixed_path 
    else:
        return path

def get_children_urls_from(url):

    children = []

    extension = url.split(".")[-1:][0]
    if extension not in ["svg","png","jpg","ico","txt","pdf"]:
            
        print("📡 get request to",url)
        # Requisicao GET da origem
        try:
            response = urllib.request.urlopen(url)
            
        except:
            pass

        else:
            html = response.read()  # Resposta html em formato String
        
            # Parseando o texto html da resposta em componentes
            soup = BeautifulSoup(html, 'html.parser')

            links = soup.find_all('a') # + soup.find_all('link')
            link_paths = list(map(lambda link: link.get('href'), links))
            filtered_http_paths = list(filter(lambda path: (path != None and path != "/" and ("http://" in path or "https://" in path or (path[:1] == "/" and ":" not in path))), link_paths))
            http_urls = list(map(lambda path: map_path_to_url(path,url), filtered_http_paths))

            for url in http_urls: children.append(url)    

    print("🤷 Found no children urls" if (len(children) == 0) else "⭐️ Found "+str(len(http_urls))+" children urls")
    return children


# MAIN RUN

print(banner)
print("\nStarting at:",origem)
print("Looking for:",destino,"\n")
print("Amount of searches:",limit,"\n")

# Search
url_path_to_destiny = depth_first_search(origem, destino)
if url_path_to_destiny:
    sequencified_path_to_destiny = sequencify_list(url_path_to_destiny, separator="\n ")
    print("\n 🎯🎉 FOUND IT! This is the path:\n",sequencified_path_to_destiny, "\n")
else:
    sequencified_cheked_urls = sequencify_list(seen_urls, separator="\n ")
    print("\n 🙈 Destiny URL not found in",limit,"tries. Checked URLs:\n",sequencified_cheked_urls,"\n")