import json
from lxml import html, etree
import requests
import re

OUTPUT_DIRECTORY = "./64kjp"
json_content = []

def clean_string(text):
    cleaned_text = text.strip("\n")
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text)
    return cleaned_text
def requestURL(url):
    return requests.get(url)
def requestSub2(url,text,index):
    print("processing:", url)
    res = requestURL(url)
    res.encoding = res.apparent_encoding
    tree = html.fromstring(res.text)
    elements = tree.cssselect('div.post_content')
    str_html = (etree.tostring(elements[0], encoding='unicode', method='html'))
    with open(OUTPUT_DIRECTORY + "/" + index + "_" + text + ".txt", "w") as f:
        f.write(str_html)


def requestSub(url, text, index):
    print("processing:", url)
    res = requestURL(url)
    res.encoding = res.apparent_encoding
    tree = html.fromstring(res.text)
    blockquotes = tree.cssselect('div.post_content > blockquote')

    output = {
        "index": index,
        "g": text,
        "gy": clean_string(blockquotes[0].text_content()),
        "t": clean_string(blockquotes[1].text_content()),
        "x": clean_string(blockquotes[2].text_content())
    }
    print(output)
    json_content.append(output)

input_json_test = [{"href":"https://www.ekigaku-shinkou-kyoukai.jp/koniti","text":"坤為地（こんいち）","order":"2"}
]

input_json = [
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/kenniten/","text":"乾為天（けんいてん）","order":"1"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/koniti","text":"坤為地（こんいち）","order":"2"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/suiraichun","text":"水雷屯（すいらいちゅん）","order":"3"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/sansuimou","text":"山水蒙（さんすいもう）","order":"4"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/suitenju","text":"水天需（すいてんじゅ）","order":"5"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tensuishou","text":"天水訟（てんすいしょう）","order":"6"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tisuisi","text":"地水師（ちすいし）","order":"7"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/suitihi","text":"水地比（すいちひ）","order":"8"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/fuutenshoutiku","text":"風天小畜（ふうてんしょうちく）","order":"9"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tentakuri","text":"天澤履（てんたくり）","order":"10"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/titentai/","text":"地天泰（ちてんたい）","order":"11"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tentihi/","text":"天地否（てんちひ）","order":"12"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tenkadoujin/","text":"天火同人（てんかどうじん）","order":"13"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/katentaiyuu/","text":"火天大有（かてんたいゆう）","order":"14"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tizanken/","text":"地山謙（ちざんけん）","order":"15"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/raitiyo/","text":"雷地予（らいちよ）","order":"16"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/takuraizui/","text":"澤雷隨（たくらいずい）","order":"17"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/sanpuuko/","text":"山風蠱（さんぷうこ）","order":"18"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/titakurin/","text":"地澤臨（ちたくりん）","order":"19"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/fuutikan/","text":"風地観（ふうちかん）","order":"20"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/karaizeigou/","text":"火雷噬嗑（からいぜいごう）","order":"21"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/sankahi/","text":"山火賁（さんかひ）","order":"22"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/santihaku/","text":"山地剥（さんちはく）","order":"23"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tiraifuku/","text":"地雷復（ちらいふく）","order":"24"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tenraimumou/","text":"天雷无妄（てんらいむもう）","order":"25"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/santentaitiku/","text":"山天大畜（さんてんたいちく）","order":"26"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/sanraii/","text":"山雷頤（さんらいい）","order":"27"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/takufuutaika/","text":"澤風大過（たくふうたいか）","order":"28"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/kannisui/","text":"坎為水（かんいすい）","order":"29"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/riika/","text":"離為火（りいか）","order":"30"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/takuzankan/","text":"澤山咸（たくざんかん）","order":"31"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/raifuukou/","text":"雷風恒（らいふうこう）","order":"32"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tenzanton/","text":"天山遯（てんざんとん）","order":"33"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/raitentaisou/","text":"雷天大壮（らいてんたいそう）","order":"34"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/katisin/","text":"火地晋（かちしん）","order":"35"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tikameii/","text":"地火明夷（ちかめいい）","order":"36"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/fuukakajin/","text":"風火家人（ふうかかじん）","order":"37"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/katakukei/","text":"火澤睽（かたくけい）","order":"38"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/suizanken/","text":"水山蹇（すいざんけん）","order":"39"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/raisuikai/","text":"雷水解（らいすいかい）","order":"40"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/santakuson/","text":"山澤損（さんたくそん）","order":"41"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/fuuraieki/","text":"風雷益（ふうらいえき）","order":"42"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/takutenkai/","text":"澤天夬（たくてんかい）","order":"43"},
 {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tenpuukou/","text":"天風姤（てんぷうこう）","order":"44"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/takutisui/","text":"澤地萃（たくちすい）","order":"45"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/tifuushou/","text":"地風升（ちふうしょう）","order":"46"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/takusuikon/","text":"澤水困（たくすいこん）","order":"47"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/suifuusei/","text":"水風井（すいふうせい）","order":"48"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/takukakaku/","text":"澤火革（たくかかく）","order":"49"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/kafuutei/","text":"火風鼎（かふうてい）","order":"50"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/sinirai/","text":"震為雷（しんいらい）","order":"51"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/gonisan/","text":"艮為山（ごんいさん）","order":"52"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/fuuzanzen/","text":"風山漸（ふうざんぜん）","order":"53"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/raitakukimai/","text":"雷澤帰妹（らいたくきまい）","order":"54"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/raikahou/","text":"雷火豊（らいかほう）","order":"55"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/kazanryo/","text":"火山旅（かざんりょ）","order":"56"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/sonifuu/","text":"巽為風（そんいふう）","order":"57"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/daitaku/","text":"兌為澤（だいたく）","order":"58"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/fuusuikan/","text":"風水渙（ふうすいかん）","order":"59"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/suitakusetu/","text":"水澤節（すいたくせつ）","order":"60"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/fuutakuchuufu/","text":"風澤中孚（ふうたくちゅうふ）","order":"61"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/raizanshouka/","text":"雷山小過（らいざんしょうか）","order":"62"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/suikakisei/","text":"水火既済（すいかきせい）","order":"63"},
  {"href":"https://www.ekigaku-shinkou-kyoukai.jp/kasuibisei/","text":"火水未済（かすいびせい）","order":"64"}]


if __name__ == '__main__':
    for j in input_json:
        requestSub(j["href"],j["text"],j["order"])
    with open(OUTPUT_DIRECTORY + "/data.json", "w", encoding="utf-8") as json_file:
        json.dump(json_content, json_file, ensure_ascii=False)