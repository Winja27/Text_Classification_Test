import jieba
import os
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




technology_path = "technology"
finance_path = "finance"
t_files = os.listdir(technology_path)
f_files = os.listdir(finance_path)
technology_list = []
finance_list = []

for file in t_files:
    if not os.path.isdir(file):
        f = open(technology_path + "/" + file)
        iter_f = iter(f)  # 创建迭代器
        str = ""
        for line in iter_f:  # 遍历文件，一行行遍历，读取文本
            str = str + line
        technology_list.append(str)  # 每个文件的文本存到list中
technology_str = ''.join(technology_list)

for file in f_files:  # 遍历文件夹
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        f = open(finance_path + "/" + file)  # 打开文件
        iter_f = iter(f)  # 创建迭代器
        str = ""
        for line in iter_f:  # 遍历文件，一行行遍历，读取文本
            str = str + line
        finance_list.append(str)  # 每个文件的文本存到list中
finance_str = ''.join(finance_list)

all_str = technology_str + finance_str
words = jieba.lcut(all_str)
dic = {}

f1 = open("cn_stopwords.txt")
stopwords = f1.read()
f1.close()
stopwords_list = stopwords.split("\n")

for word in words:
    if word not in dic:
        if word not in stopwords_list:
            dic[word] = 1


def article_wordvector(article, dic):
    wordlist = []
    article_allwords = jieba.lcut(article)
    for word in dic:
        if word not in article_allwords:
            wordlist.append(0)
        else:
            wordlist.append(1)
    return wordlist


t0_wordvector = article_wordvector(technology_list[0], dic)
t1_wordvector = article_wordvector(technology_list[1], dic)
t2_wordvector = article_wordvector(technology_list[2], dic)
t3_wordvector = article_wordvector(technology_list[3], dic)
t4_wordvector = article_wordvector(technology_list[4], dic)
f0_wordvector = article_wordvector(finance_list[0], dic)
f1_wordvector = article_wordvector(finance_list[1], dic)
f2_wordvector = article_wordvector(finance_list[2], dic)
f3_wordvector = article_wordvector(finance_list[3], dic)
f4_wordvector = article_wordvector(finance_list[4], dic)

prior_probability = 0.5
tech_wordlist = jieba.lcut(technology_str)
fi_wordlist = jieba.lcut(finance_str)
tech_wordsnum = len(tech_wordlist)
fi_wordsnum = len(fi_wordlist)
condition_probability_tech = []
condition_probability_fi = []
for word in dic:
    if word in tech_wordlist:
        a = 2.0 / (tech_wordsnum + len(t0_wordvector))
        b = 1.2 / (fi_wordsnum + len(t0_wordvector))
    else:
        a = 1.0 / (tech_wordsnum + len(t0_wordvector))
        b = 4.0 / (fi_wordsnum + len(t0_wordvector))
    condition_probability_tech.append(a)
    condition_probability_fi.append(b)

#print("Please input the filename")
#filename = input()
#f = open(f"{filename}", "r")
f = open(f"{url}.txt","r")
content = f.read()
f.close()
input_news = article_wordvector(content, dic)
sum1 = 0.0
sum2 = 0.0
for index in range(len(input_news)):
    if input_news[index] == 1:
        a = condition_probability_tech[index]
        b = condition_probability_fi[index]
        sum1 = a + sum1
        sum2 = b + sum2
print(sum1)
print(sum2)
if sum1 > sum2:
    print("Technology")
else:
    print("Finance")

#https://new.qq.com/rain/a/20230325A01WR100
#https://new.qq.com/rain/a/20230325A02VVA00