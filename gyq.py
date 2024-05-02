import json

from lxml import html, etree
import requests
import re

GYQURL = "https://www.zhouyi.cc/lingqian/guanyin/"
GYQDOMAIN = "https://www.zhouyi.cc"
GYQOUT = "./gyqoutput"

output_jsons = []


def clean_string(text):
    cleaned_text = text.strip("\n")
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text)
    return cleaned_text


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return clean.sub('', text)


def replace_br_with_linebreak(text):
    clean = re.compile('<br>')
    text = clean.sub('', text)
    return text


def clean_nbsp(text):
    cleaned_text = re.sub(r"\s", "\n", text)
    return cleaned_text


def requestURL(url):
    return requests.get(url)


def extract_number(text):
    pattern = r'第(\d+)签'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    else:
        return None


def requestSub(text, url):
    _index = extract_number(text)
    _url = GYQDOMAIN + url
    res = requestURL(_url)
    res.encoding = res.apparent_encoding
    tree = html.fromstring(res.text)
    x = tree.cssselect('div.lianqianzi_wp > div.lq_tt.f14.fb.cf.tleft')
    elements = tree.cssselect('div.lianqianzi_wp > div.lq_m.f14.tleft.lh25')
    i = 0
    qian = {
        "i": _index,
        "text": "",
        "qianshi": "",
        "shiyi": "",
        "jieyue": "",
        "source": ""
    }
    for element in elements[:len(elements) - 1]:
        _out = etree.tostring(element, encoding='unicode', method='html')
        clean1 = replace_br_with_linebreak(_out)
        clean2 = remove_html_tags(clean1)
        clean2 = clean_nbsp(clean2)
        if i == 0:
            pattern = r'^(?:\n.*?){2}\n(.*)'
            match = re.search(pattern, clean2, re.MULTILINE)
            if match:
                second_line = match.group(1)
                qian['text'] = clean_string(second_line)

            # Extract the 签诗 block
            qian_shi_pattern = r'签诗\n(.*?)\n诗意'
            qian_shi_match = re.search(qian_shi_pattern, clean2, re.DOTALL)
            if qian_shi_match:
                qian_shi_block = qian_shi_match.group(1)
                qian['qianshi'] = clean_string(qian_shi_block)

            # Extract the 诗意 block
            shi_yi_pattern = r'诗意\n(.*?)\n解曰'
            shi_yi_match = re.search(shi_yi_pattern, clean2, re.DOTALL)
            if shi_yi_match:
                shi_yi_block = shi_yi_match.group(1)
                qian['shiyi'] = clean_string(shi_yi_block)

            # Extract the 解曰 block
            jie_yue_pattern = r'解曰\n(.*)\n整体解译'
            jie_yue_match = re.search(jie_yue_pattern, clean2, re.DOTALL)
            if jie_yue_match:
                jie_yue_block = jie_yue_match.group(1)
                qian['jieyue'] = clean_string(jie_yue_block)
        elif i == 2:
            qian['source'] = clean_string(clean2)
        with open(GYQOUT + "/" + x[0].text + "_" + str(i) + ".txt", "w") as f:
            f.write(clean2)
        i = i + 1
    output_jsons.append(qian)


if __name__ == '__main__':
    res = requestURL(GYQURL)
    res.encoding = res.apparent_encoding
    tree = html.fromstring(res.text)
    elements = tree.cssselect('div.gylqlist> ul > li > a')
    for element in elements:
        print(element.text, element.get("href"))
        requestSub(element.text, element.get("href"))
    print(output_jsons)
    with open(GYQOUT + "/data.json", "w", encoding="utf-8") as json_file:
        json.dump(output_jsons, json_file, ensure_ascii=False)
