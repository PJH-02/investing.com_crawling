import cloudscraper # type: ignore
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4
import time

# Scraper 객체 생성
scraper = cloudscraper.create_scraper()

# 검색어 입력
query_txt = input("티커를 입력하세요: ")

# 검색 URL
search_url = f"https://www.investing.com/search/?q={query_txt}"

# 페이지 요청 및 파싱
response = scraper.get(search_url)
time.sleep(3) #이전 데이터를 실수로 읽어오는 case 방지 위해 3초 기다리도록 설정
soup = BeautifulSoup(response.content, "html.parser")

# 검색 결과에서 첫 번째 종목 링크 추출
result = soup.find("a", {"class": "js-inner-all-results-quote-item row"})
if result:
    stock_url = "https://www.investing.com" + result["href"]
else:
    print("해당 티커에 대한 정보를 찾을 수 없습니다.")


#기술적 분석 스크래핑
scraper = cloudscraper.create_scraper()
html = scraper.get(stock_url).content

soup = BeautifulSoup(html, 'html.parser')

divs = soup.find_all('div', {'class':'flex flex-1 flex-col items-start gap-1 rounded'})

for div in divs:
    tech = div.get_text()

result = (tech.replace('Technical Analysis', 'Technical Analysis-').split('-'))
result.insert(0, query_txt)

#애널리스트 분석 스크래핑
scraper = cloudscraper.create_scraper()
html = scraper.get(stock_url).content

soup = BeautifulSoup(html, 'html.parser')

div2 = soup.find_all('div', {'class':'flex flex-col items-start gap-2 self-stretch rounded md:h-[84px]'})

for Div in div2:
    Ana = Div.get_text()

result2 = Ana.replace('Sentiment', 'Sentiment;').replace('Price', ';Price').replace('Target', 'Target;').split(';')

price = soup.find_all('div', {'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]'})
for today in price:
    present = today.get_text()

#출력
print(result, result2, present)