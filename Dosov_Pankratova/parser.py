#либы
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd


#получить html код страницы
def get_html(url):
	server_response = requests.get(url)
	return server_response.text

def get_all_links(html):
	soup_obj = BeautifulSoup(html, 'lxml')
	links = soup_obj.find('div', class_ ='words-drop-block').find('ul', class_='list').find_all('a', href=True)
	links_ = []

	
	for link in links:
		tag_a = link.get('href')
		domain_name = 'https://audio-english.ru' + tag_a
		links_.append(domain_name)
	
	links_.append('https://audio-english.ru/frequencydict/s_1_po_500/') 
	return links_	

def get_page_data(html):
	soup_obj = BeautifulSoup(html, 'lxml')	
	word = []
	#word_ = soup_obj.find('table', class_='table-l table-voc').find('tr').find('td', class_='v-word').find('div', class_='del-row float-l')
	tr = soup_obj.find('table', class_='table-l table-voc')#.find_all('tr')
	try:
		children = tr.findChildren('div', class_='del-row float-l')
	except:
		children = ''
	try:
		children2 = tr.findChildren('td', class_='v-tv')
	except:
		children2 = ''
	
	data = {'word' : children, 'frequency' : children2}
	return data
	

def write_csv(data):
	with open('freqdict.csv', 'a') as file:
		writer = csv.writer(file)
		writer.writerow( (data['word'], data['frequency']) )
		
		print(data['word'], 'parsed')

def main():
	start = datetime.now()

	url = 'https://audio-english.ru/frequencydict/s_1_po_500/'
	get_all_links(get_html(url))
	
	all_links = get_all_links(get_html(url))
	for i in all_links:
		data_ = get_page_data(get_html(i))
		write_csv(data_)
	

if __name__ == '__main__':
	main()