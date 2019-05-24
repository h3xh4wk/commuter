from bs4 import BeautifulSoup
import requests

def save_population():
    url = 'https://www.census2011.co.in/data/district/242-bangalore-karnataka.html'
    response=requests.get(url)
    if response:
        base_url=response.url.split("/")[0] + "//" + response.url.split("/")[2]
        soup=BeautifulSoup(response.text)

        with open('data/population.csv', 'w') as f:
            print('writing population data....')
            rows_talukas=soup.find_all('tr', class_='tr1')

            for row in rows_talukas:
                # get the url of the taluka
                link=row.find('a').attrs['href']
                town_page_resp=requests.get(base_url + link)
                town_page_soup=BeautifulSoup(town_page_resp.text)

                vill_towns=town_page_soup.find_all('tr', class_='tr1')
                for r in vill_towns:
                    r_data=r.find_all('td')
                    line=r_data[1].text.strip()+","+ \
                            r_data[2].text.strip()+","+ \
                            r_data[3].text.strip().replace(",","")
                    f.write(line + "\n")


if __name__=="__main__":
    save_population()
