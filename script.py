import requests
from bs4 import BeautifulSoup
import os
import re
import unicodedata
import json

def normalize_filename(s):
    s = re.sub(r'[^\w\s-]', '', s).strip().lower()
    s = re.sub(r'[-\s]+', '-', s)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    return s

def download_images_from_page(url, image_data):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    img_tags = soup.find_all('a', class_='short-poster')
    for img in img_tags:
        image_url = img.find('img')['data-src']
        alt_text = img.find('img')['alt']
        href = img['href']
        image_name = normalize_filename(alt_text)
        image_data.append({
            "url": image_url,
            "name": image_name
        })
        
        # Append the href to data.txt
        with open('data.txt', 'a') as file:
            file.write(href + '\n')

base_url = 'https://fr.fss.lol/films/page/'
image_data = []

for page_num in range(1, 1094):
    url = f'{base_url}{page_num}/'
    print(f'Téléchargement à partir de {url} ...')
    download_images_from_page(url, image_data)

# Save image data to img.json
with open('img.json', 'w', encoding='utf-8') as json_file:
    json.dump(image_data, json_file, ensure_ascii=False, indent=4)

print('Les données des images ont été sauvegardées dans img.json et les hrefs ont été ajoutés à data.txt')
