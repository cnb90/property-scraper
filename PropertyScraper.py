import csv, requests
from collections import OrderedDict
from bs4 import BeautifulSoup


def main():
    all_properties_url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=23'
    single_property_url = 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId='
    final_list = []
    lines = []

    # Create session to get all properties
    s = requests.Session()
    r = s.get(all_properties_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Get all properties
    property_ids = soup.find_all("td", attrs={"class": "hidden-print"})

    for property_id in property_ids:
        # Create the property url
        property_id = str(property_id).split("PropertyId=", 1)[1].split('\"')[0]
        property_url = single_property_url + property_id
        print("Property Found"),

        # Get the page data of the property
        property_page = s.get(property_url)
        property_page = BeautifulSoup(property_page.text, "html.parser")
        t_info = property_page.find_all("table")[0]
        t_status = property_page.find_all("table")[1]
        print(">"),

        # Filter out the unneeded and keep the good data
        for line in t_info:
            info = str(line).strip('<tr>').strip('</tr>').replace('<td>','').replace('</td>','').replace('\n','')
            if info != '':
                lines.append(info)
            print(">"),

        # Organize property info into a dictionary
        d = OrderedDict()

        # Get property status and last status date
        for status in t_status:
            status = str(status).strip('<tr>').strip('</tr>').replace('\n', '').replace('</td><td>', ' : ').rstrip()
            if status != '' and status.startswith("<td>"):
                d['Latest Status'] = status.split(" : ")[0].strip("<td>") + "d"
                d['Latest Status Date'] = status.split(" : ")[1].strip("</td>")
                break

        # Get sales date, sheriff #, address, and debt amount of property
        for line in lines:
            if "Sales Date :" in line:
                d['Sales Date'] = line.split(":")[1]
            elif "Sheriff # :" in line:
                d['Sheriff #'] = line.split(":")[1]
            elif "Address :" in line:
                d['Address'] = line.split(":")[1].replace('<br/>', ', ')
            elif "Debt Amount :" in line:
                d['Debt Amount'] = line.split(":")[1]

        # Get property url
        d['Link'] = property_url

        # Copy the contents of the property info dictionary into a list
        final_list.append(d.copy())
        lines = []
        d.clear()
        print(">")

    # create csv with all properties
    with open('test.csv', 'wb') as csv_file:
        fieldnames = [
            'Sheriff #',
            'Sales Date',
            'Latest Status',
            'Latest Status Date',
            'Address',
            'Debt Amount',
            'Link'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_list)


if __name__ == "__main__":
    main()
