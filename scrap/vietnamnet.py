import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.utils import escape
import time

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
	'\x1f':'\\x1f'  #	US
    }	
	
	if ch in illegal_xlsx_chars:
		return illegal_xlsx_chars[ch]
	
	return ch
	
def escape_xlsx_string(st):
	return ''.join([escape_xlsx_char(ch) for ch in st])

def scrap_from_page(page_num, ws):
    base_url = f"https://vietnamnet.vn/phap-luat-page{page_num}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    # Tìm các bài báo
    articles = soup.find_all(["h2", "h3"], class_="vnn-title")

    for article in articles:
        link = article.find("a").get("href")
        data = get_news_content(link, page_num)
        if data is not None:
            try:
                ws.append(data)
            except Exception as e:
                print(f"Error when writing data to worksheet: {e}")
                continue

def get_news_content(link, page_num):
    if "https://vietnamnet.vn" not in link:
        base_url = f"https://vietnamnet.vn/{link}"
    else:
        base_url = link
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {link}: {e}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    h2 = soup.find_all(["h2", "h3"], class_="content-detail-sapo")
    if len(h2) == 0:
        return None
    
    if h2[0].text == "":
        summarize = h2[0].findNext('h2')
    else:
        summarize = h2[0].text
    
    content_text = ""
    content_container = soup.find_all("div", class_="maincontent main-content")
    if len(content_container) == 0:
        return None
    
    contents = content_container[0].find_all("p")
    if len(contents) < 2:
        return None
    
    for content in contents:
        content_text += content.text + " "
    
    content_text = content_text.rsplit(".", 1)[0]
    
    return [summarize, escape_xlsx_string(content_text), link]

def handle_page(page_num):
    wb = Workbook()
    ws = wb.active
    ws.append(["Summarize", "Content", "Link"])
    for i in range(1, page_num):
        print(i)
        scrap_from_page(i, ws)
        time.sleep(1)  # Add delay to avoid overwhelming the server
    wb.save("PhapLuat_VietnamNet.xlsx")
    print("Đã lưu dữ liệu vào file Excel.")


handle_page(1500)