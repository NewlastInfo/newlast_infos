import requests
from bs4 import BeautifulSoup

url = 'http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;szzf;pn50;ddesc;qsd20220309;qed20230309;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
print(soup)

table = soup.find_all('table')[0]
rows = table.find_all('tr')

for row in rows[1:]:
    cols = row.find_all('td')
    rank = cols[0].text.strip()
    name = cols[1].text.strip()
    code = cols[2].text.strip()
    daily_return = cols[3].text.strip()
    print(rank, name, code, daily_return)
