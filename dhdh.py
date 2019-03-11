from bs4 import BeautifulSoup
f= open('temp.html')
text=f.read()
soup = BeautifulSoup(text,'html.parser')
new_tag = soup.new_tag('a')
soup.find('p', {"class":'paginator'}).append(new_tag)
print(soup.prettify())
