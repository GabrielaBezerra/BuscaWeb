#!/usr/bin/env python

# Dependencias
import sys
import time
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

en-us: Finding the path between two web URLs using Depth-First-Search (DFS).
pt-br: Achando o caminho entre duas URLs web usando Busca em Profundidade.

Authors: Gabriela Bezerra, Guilherme Araújo, Ítalo Bruno, Pedro Moura.
"""

onboarding = """
A short explanation before we begin.

This algorithm consists of the following steps: (simplified step-by-step description)

    0. Define 3 main inputs: origin url, destiny url and the search limit amount.
    1. Initialize the seen urls list, the processing stack and the search counter.
    2. Add the origin url to the processing stack.
    3. Verify if the search limit amount has been reached by the search counter.
        3.1. If it did, print all the seen urls then End program.
        3.2. If it didn't, continue the algorithm.
    4. Process the last url of the stack by checking if it is the destiny url and append it to the seen urls list.
        4.1. If it is, the algorithm prints all the urls between the origin url and the destiny url then End program.
        4.2. It it isn't, continue the algorithm.
    5. Make a GET request to the processed url and increment search counter.
    6. Read the html page returned by the request.
    7. Create a children urls list and append all the urls found inside any <a href=''> tag to it.
    8. Check if the children urls list contains the destiny url.
        8.1. If it does, the algorithm prints all the urls between the origin url and the destiny url then End program.
        8.2. If it doesn't, append all the urls of the children urls list to the processing stack. 
    9. Go back to step 3.

"""

# SCRIPT INFO
scriptname = "crawler_busca_web.py"
param1 = "<https://www.origin.com>"
param2 = "<https://www.destiny.com>"
param3 = "[<amount of searches allowed>]"
usage = "usage: ./" + scriptname + " " + param1 + " " + param2 + " " + param3
example = (
    "You should try something like this: \n\n  ./"
    + scriptname
    + ' "http://pyfound.blogspot.com" "https://careers.google.com" 9'
)
message = "\n" + usage + "\n\n" + example + "\n"

# INPUT CHECK
# Params verification
verify_params_quant = len(sys.argv) != 4
if verify_params_quant:
    exit(message)

param1_verify = len(urlparse(sys.argv[1]).netloc) == 0
param2_verify = len(urlparse(sys.argv[2]).netloc) == 0
param3_verify = len(sys.argv[3]) == 0 or int(sys.argv[3]) == None
if param1_verify or param2_verify or param3_verify:
    exit(message)

# Initial URLs
origin = sys.argv[1]
destiny = sys.argv[2]

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

    while not stack.empty() and dfs_counter < limit:
        dfs_counter += 1
        print("\nDFS number", dfs_counter, "of", limit)

        # Proccess URL and remove it from Stack
        current_url = stack.get()

        print("processing", current_url)
        print("stack has", stack.qsize(), "items")

        if never_seen(current_url):
            seen_urls.append(current_url)
            path_to_destiny.append(current_url)

            if current_url == destiny_url or current_url + "/" == destiny_url:
                return path_to_destiny

            # Add its children URLs to Stack
            children_urls = get_children_urls_from(current_url)
            if len(children_urls) == 0:
                path_to_destiny.pop()
            else:
                # Checking all urls inside this page
                if destiny_url in children_urls or destiny_url + "/" in children_urls:
                    path_to_destiny.append(destiny_url)
                    return path_to_destiny

                # Adding urls to stack, for depth-first-search
                max_new_size = stack.qsize() + len(children_urls)
                for url in children_urls:
                    if never_seen(url):
                        stack.put(url)
                discarded_amount = max_new_size - stack.qsize()
                print(
                    "stack now has",
                    stack.qsize(),
                    "items. Discarded",
                    discarded_amount,
                    " already seen urls.",
                )


def never_seen(url):
    has_not_be_seen = True
    for seen in seen_urls:
        if url == seen or url == seen + "/" or url + "/" == seen:
            has_not_be_seen = False
    return has_not_be_seen


def sequencify_list(list, separator=" > "):
    return reduce(lambda ac, element: ac + element + separator, list, "")[:-2]


def map_path_to_url(path, url):
    if "http" not in path:
        domain = (
            urlparse(url)[1] if urlparse(url)[1][-1:] != "/" else urlparse(url)[1][:-1]
        )
        fixed_path = path.replace("//", "/")
        return urlparse(url)[0] + "://" + domain + fixed_path
    else:
        return path


def get_children_urls_from(url):

    children = []

    extension = url.split(".")[-1:][0]
    if extension not in ["svg", "png", "jpg", "ico", "txt", "pdf"]:

        print("get request to", url)
        # Requisicao GET da origem
        try:
            response = urllib.request.urlopen(url)

        except:
            pass

        else:
            html = response.read()  # Resposta html em formato String

            # Parseando o texto html da resposta em componentes
            soup = BeautifulSoup(html, "html.parser")

            links = soup.find_all("a")  # + soup.find_all('link')
            link_paths = list(map(lambda link: link.get("href"), links))
            filtered_http_paths = list(
                filter(
                    lambda path: (
                        path != None
                        and path != "/"
                        and (
                            "http://" in path
                            or "https://" in path
                            or (path[:1] == "/" and ":" not in path)
                        )
                    ),
                    link_paths,
                )
            )
            http_urls = list(
                map(lambda path: map_path_to_url(path, url), filtered_http_paths)
            )

            for url in http_urls:
                children.append(url)

    print(
        "Found no children urls"
        if (len(children) == 0)
        else "Found " + str(len(http_urls)) + " children urls"
    )
    return children


# MAIN RUN

print(banner)
time.sleep(3)
print(onboarding)
time.sleep(2)
print("\nStarting at:", origin)
print("Looking for:", destiny, "\n")
print("Amount of searches:", limit)

# Search
url_path_to_destiny = depth_first_search(origin, destiny)
if url_path_to_destiny:
    sequencified_path_to_destiny = sequencify_list(url_path_to_destiny, separator="\n ")
    print(
        "\nFOUND IT! After looking",
        len(url_path_to_destiny),
        "urls using DFS, this is the path:\n",
        sequencified_path_to_destiny,
        "\n",
    )
else:
    sequencified_cheked_urls = sequencify_list(seen_urls, separator="\n ")
    print(
        "\nDestiny URL not found in",
        limit,
        "tries. Checked URLs:\n",
        sequencified_cheked_urls,
        "\n",
    )
