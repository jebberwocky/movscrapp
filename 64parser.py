import json
from lxml import html, etree
import re

OUT64 = "./64output"
html_file_path = "./64.html"
json_content = []

def get_next_p(element):
    p = element.getnext()
    #print(p.text_content())
    return p

def parse_next_table(element):
    # Get the table element
    table = element.getnext()
    outter = []
    for row in table.findall('tbody/tr'):
        inner = []
        for cell in row.findall('td'):
            # Process the cell element
            inner.append(cell.text_content().strip())
        outter.append(inner)
    return outter

if __name__ == '__main__':
    with open(html_file_path, 'r', encoding="utf-8") as f:
        html_content = f.read()
        tree = html.fromstring(html_content)
        elements = tree.cssselect('div.ztext> h2')
        for element in elements:
            p = get_next_p(element)
            p2 = get_next_p(p)
            p3 = get_next_p(p2)
            output = {
                "g":element.text_content(),
                "gy":p.text_content(),
                "t":p2.text_content(),
                "x":p3.text_content(),
                "yy":parse_next_table(p3)
            }
            json_content.append(output)
    with open(OUT64+'/data.json', 'w', encoding='utf-8', ) as outfile:
        # Use json.dump() to write the data to the file
        json.dump(json_content, outfile, ensure_ascii=False)
