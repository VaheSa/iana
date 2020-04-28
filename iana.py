from bs4 import BeautifulSoup
import requests as req
import json
import datetime


def get_tld_whois(tld_href):
    resp = req.get(tld_href)
    soup = BeautifulSoup(resp.content, 'lxml')
    b_tags = soup.findAll("b")
    host = "N/A"
    for b_tag in b_tags:
        if "WHOIS Server" in b_tag.text:
            host = b_tag.next_element.next_element.replace(" ", "").replace("\n", "").replace("\r", "")
    return host


def get_json(url):
    resp = req.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    tld_table = soup.find("tbody")

    now = datetime.datetime.now()
    to_json = {"_": {"last_update": now.strftime("%Y-%m-%d")}}
    for tld_tr in tld_table.find_all("tr"):
        tld_info = {}
        tld_tds = []
        for tld_td in tld_tr.find_all("td"):
            tld_tds.append(tld_td)
        tld_name = tld_tds[0]
        tld_clear_name = tld_name.text.replace('.', '').replace("\n", "").replace("\r", "")
        tld_type = tld_tds[1]
        tld_manager = tld_tds[2]
        tld_href = url+"/"+tld_clear_name+".html"
        tld_info["name"] = tld_clear_name
        tld_info["tld_type"] = tld_type.text
        tld_info["tld_manager"] = tld_manager.text
        tld_info["host"] = get_tld_whois(tld_href)
        to_json.update({tld_clear_name: tld_info})
        # For a quick check. Мake a comment after checking!
        # if tld_clear_name == "accountants":
        #     break
        # Мake a comment to here after checking
    with open('tld_info.json', 'w') as json_file:
        json.dump(to_json, json_file)


if __name__ == '__main__':
    url = "https://www.iana.org/domains/root/db"
    get_json(url)