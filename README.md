# BuscaWeb
### Using Depth-First-Search (DFS) to find the URLs between two websites, given the amount of tries.

*Authors: Gabriela Bezerra, Guilherme Araújo, Ítalo Bruno, Pedro Moura.*

Implemented with Python 3.8.5 and Beautiful Soup 4.

## Getting Started
Enter the project's venv

`source buscaweb/bin/activate`

Install the dependencies

`pip install -r requirements.txt --user`

Setup the script as executable

`chmod +x crawler-busca-web.py`

Run the script

`./crawler_busca_web.py "http://pyfound.blogspot.com" "https://careers.google.com" 9`

Another way to run the script would be

`python crawler_busca_web.py "http://pyfound.blogspot.com" "https://careers.google.com" 9`

Usage

`./crawler_busca_web.py <https://www.origin.com> <https://www.destiny.com> [<amount of searches allowed>]`


## 📚 Many pages make a thick book.

Video with Code explanation in portuguese: https://youtu.be/VhKkGs4ooO0

### A short (informal) general explanation of the algorithm workflow.

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
7. Create a children urls list and append all the urls found inside any \<a href=''\> tag to it.
8. Check if the children urls list contains the destiny url.
    8.1. If it does, the algorithm prints all the urls between the origin url and the destiny url then End program.
    8.2. If it doesn't, append all the urls of the children urls list to the processing stack. 
9. Go back to step 3.
