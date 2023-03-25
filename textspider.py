from lxml import etree
import requests

print("Please input the news url")
news_url = input()
url = news_url[26:]
response = requests.get(news_url)
page_source = response.text
page_tree = etree.HTML(page_source)
div = page_tree.xpath('/html/body/div[3]/div[1]/div[1]/div[2]')[0]
content = div.xpath(".//text()")
text = ''.join(content)
text.replace(' ', '')
with open(f"{url}.txt", mode="w", encoding="utf-8") as f:
    f.write(text)
    f.close()
