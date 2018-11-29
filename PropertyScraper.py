import csv
import urllib2
from collections import OrderedDict

from bs4 import BeautifulSoup
import requests


def main():
    all_properties_url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=23'
    single_property_url = 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId='
    final_list = []

    lines = []

    s = requests.Session()
    r = s.get(all_properties_url)
    soup = BeautifulSoup(r.text, "html.parser")
    property_ids = soup.find_all("td", attrs={"class": "hidden-print"})
    for property_id in property_ids:
        print("Property Found"),
        property_id = str(property_id).split("PropertyId=", 1)[1].split('\"')[0]
        property_url = single_property_url + property_id
        property_page = s.get(property_url)
        property_page = BeautifulSoup(property_page.text, "html.parser")
        print(">"),

        t_info = property_page.find_all("table")[0]
        t_status = property_page.find_all("table")[1]

        for line in t_info:
            info = str(line).strip('<tr>').strip('</tr>').replace('<td>','').replace('</td>','').replace('\n','')
            if info != '':
                lines.append(info)
        print(">"),
        d = OrderedDict()
        for line in lines:
            if "Sheriff # :" in line:
                d['Sheriff #'] = line.split(":")[1]
            elif "Sales Date :" in line:
                d['Sales Date'] = line.split(":")[1]
            elif "Address :" in line:
                d['Address'] = line.split(":")[1].replace('<br/>', ', ')
            elif "Debt Amount :" in line:
                d['Debt Amount'] = line.split(":")[1]
        print(">"),
        for status in t_status:
            status = str(status).strip('<tr>').strip('</tr>').replace('\n', '').replace('</td><td>', ' : ').rstrip()
            if status != '' and status.startswith("<td>"):
                d['Latest Status'] = status.split(" : ")[0].strip("<td>")
                d['Latest Status Date'] = status.split(" : ")[1].strip("</td>")
                break
        print(">")
        d['Link'] = property_url
        final_list.append(d.copy())
        lines = []
        d.clear()

    for item in final_list:
        print item

    with open('test.csv', 'w+') as csv_file:
        fieldnames = ['Sheriff #', 'Sales Date', 'Address', 'Debt Amount', 'Link', 'Latest Status', 'Latest Status Date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(final_list)

    #
    # all_properites_page = urllib2.urlopen(all_properties_url)
    #
    #
    #
    #
    # #for property_id in name_box:
    # property_id = name_box[0]
    #
    # print single_property_url + property_id
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    # try:
    #     single_property_page = requests.get(single_property_url + property_id, headers=headers)
    # except requests.exceptions.RequestException as e:
    #     print(e)
    #     exit()
    # soup = BeautifulSoup(single_property_page.text, "html.parser")
    # print soup


if __name__ == "__main__":
    main()
