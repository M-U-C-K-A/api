import requests
from bs4 import BeautifulSoup
import os
import re
import unicodedata

def normalize_filename(s):
    s = re.sub(r'[^\w\s-]', '', s).strip().lower()
    s = re.sub(r'[-\s]+', '-', s)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    return s

def download_images_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    image_data = []
    
    img_tags = soup.find_all('a', class_='short-poster')
    for img in img_tags:
        image_url = img.find('img')['data-src']
        alt_text = img.find('img')['alt']
        href = img['href']
        image_name = normalize_filename(alt_text)
        image_data.append((image_url, image_name, href))
    
    with open('data.txt', 'a') as file:
        for _, _, href in image_data:
            file.write(href + '\n')
    
    for image_url, image_name, _ in image_data:
        try:
            image_response = requests.get(image_url)
            subdir = 'src'
            if not os.path.exists(subdir):
                os.makedirs(subdir)
            image_path = os.path.join(subdir, f'{image_name}.jpg')
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)
            print(f'Téléchargé {image_name}.jpg depuis {image_url}')
        except Exception as e:
            print(f'Erreur lors du téléchargement de {image_url}: {str(e)}')

base_url = 'https://fr.fss.lol/films/page/'
for page_num in range(1, 11):
    url = f'{base_url}{page_num}/'
    print(f'Téléchargement à partir de {url} ...')
    download_images_from_page(url)
