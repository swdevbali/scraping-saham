from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
# Here, we're just importing both Beautiful Soup and the Requests library

page_link = 'https://www.bca.co.id/Individu/Sarana/Kurs-dan-Suku-Bunga/Kurs-dan-Kalkulator'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.get(page_link, timeout=5)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")

# we use the html parser to parse the url content and store it in a variable

# print(page_content.prettify())

# tabel = page_content.find_all("div", {"class": "table-responsive col-md-8 kurs-e-rate"})
containers = page_content.find("tbody", {"class": "text-right"})
# containers = page_content.find_all('td', style=lambda value: value and 'background-color: white' in value)
table_rows = containers.find_all('tr')

print(table_rows)

res = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text.strip() for tr in td if tr.text.strip()]
    if row:
        res.append(row)
    #nama mata uang
    # data_mata_uang = containers

df = pd.DataFrame(res, columns=["mata_uang", 'e_jual', 'e_beli', 't_jual', 't_beli', 'b_jual', 'b_beli'])
print(df)

# print(mata_uang)
# print data to csv
file_path = os.path.join(os.getcwd(), 'data.csv')
# f = open(file_path, 'w')
# f.write('#Tanggal;Value\n')

df.to_csv(file_path, index=False)