from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import certifi

def search(search_phrase, results_amount=5):
    results = DDGS().text(search_phrase, max_results=results_amount)
    return results

def browse(url, verify=certifi.where()):
    webpage = requests.get(url,verify=certifi.where() )
    soup = BeautifulSoup(webpage.text, 'html.parser')
    return soup.get_text()

def type_content(content):
    print(content)

