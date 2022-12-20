import requests
from bs4 import BeautifulSoup


url = 'https://www.investing.com/equities/nike'
page = requests.get(url)
#print(page.status_code)
soup = BeautifulSoup(page.text, 'html.parser')
print(soup)



#company = soup.find('h1', {'class': 'text-2xl font-semibold instrument-header_title__gCaMF mobile:mb-2'}).text

# print('Loading: ',page)
#print(company, price, change)


#price = soup.find('div', {'class': 'instrument-price_instrument-price__3uw25 flex items-end flex-wrap font-bold'}).find_all('span')[0].textchange = soup.find('div', {'class': 'instrument-price_instrument-price__3uw25 flex items-end flex-wrap font-bold'}).find_all('span')[2].text
#company = soup.find('span', {'class': 'text-2xl'}).text
#price = soup.find('div', {'class': 'instrument-price_instrument-price__3uw25 flex items-end flex-wrap font-bold'}).find_all('span')[0].text
#change = soup.find('div', {'class': 'instrument-price_instrument-price__3uw25 flex items-end flex-wrap font-bold'}).find_all('span')[2].text


#print(f'company: {company}') # \n price: {price} \n change: {change}')
