import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def escape_xlsx_char(ch):
	illegal_xlsx_chars = {
	'\x00':'\\x00',	#	NULL
	'\x01':'\\x01',	#	SOH
	'\x02':'\\x02',	#	STX
	'\x03':'\\x03',	#	ETX
	'\x04':'\\x04',	#	EOT
	'\x05':'\\x05',	#	ENQ
	'\x06':'\\x06',	#	ACK
	'\x07':'\\x07',	#	BELL
	'\x08':'\\x08',	#	BS
	'\x0b':'\\x0b',	#	VT
	'\x0c':'\\x0c',	#	FF
	'\x0e':'\\x0e',	#	SO
	'\x0f':'\\x0f',	#	SI
	'\x10':'\\x10',	#	DLE
	'\x11':'\\x11',	#	DC1
	'\x12':'\\x12',	#	DC2
	'\x13':'\\x13',	#	DC3
	'\x14':'\\x14',	#	DC4
	'\x15':'\\x15',	#	NAK
	'\x16':'\\x16',	#	SYN
	'\x17':'\\x17',	#	ETB
	'\x18':'\\x18',	#	CAN
	'\x19':'\\x19',	#	EM
	'\x1a':'\\x1a',	#	SUB
	'\x1b':'\\x1b',	#	ESC
	'\x1c':'\\x1c',	#	FS
	'\x1d':'\\x1d',	#	GS
	'\x1e':'\\x1e',	#	RS
	'\x1f':'\\x1f'}	#	US
	
	if ch in illegal_xlsx_chars:
		return illegal_xlsx_chars[ch]
	
	return ch
	
def escape_xlsx_string(st):
	return ''.join([escape_xlsx_char(ch) for ch in st])

def scrap_from_page(page_num, ws):
    base_url = f"https://vnexpress.net/phap-luat-p{page_num}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Tìm các bài báo
    articles = soup.find_all(["h2", "h3"], class_="title-news")
    print(len(articles))
    for article in articles:
        link = article.find("a").get("href")
        data = get_news_content(link)
        if data is not None:
            ws.append(data)


def get_news_content(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    summarize = soup.find_all("p", class_="description")
    if len(summarize) == 0:
        return None
    summarize = summarize[0].text
    
    content_text = ""
    contents = soup.find_all("p", class_="Normal")
    if len(contents) < 2:
        return None
    
    for content in contents:
        content_text += content.text + " "

    return [summarize, escape_xlsx_string(content_text), link]

def handle_page(page_num):
    wb = Workbook()
    ws = wb.active
    ws.append(["Summarize", "Content", "Link"])
    for i in range(1, page_num + 1):
        scrap_from_page(i, ws)
    wb.save("PhapLuat_VnExpress.xlsx")
    print("Đã lưu dữ liệu vào file Excel.")


handle_page(1000)