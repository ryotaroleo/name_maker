import itertools
import requests
import jaconv
from name_devider import devide
import argparse

def main():
    yomi = args.yomi
    devided_names = devide(yomi)
    kanji_stock = {}
    for devided_name in devided_names:
        for letter in devided_name:
             if letter not in kanji_stock.keys():
                 kanji_stock[letter]=get_kanji(letter)

    daikichi_names = []
    daikichi_numbers = [11,16,21,23,31,32,41]
    kichi_numbers = [11,16,21,23,31,32,41,3,5,6,8,13,15,18,24,25,29,33,37,39,44,45,47,48,51,52]

    #Jikaku_part
    for devided_name in devided_names:
        if len(devided_name) == 1:
            namaes = kanji_stock[devided_name[0]]
            for namae in namaes:
                 #if namae[1] == 11:
                 if namae[1] + 1 in daikichi_numbers:
                      daikichi_names.append(namae)
        if len(devided_name) == 2:
            namaes = list(itertools.product(kanji_stock[devided_name[0]],kanji_stock[devided_name[1]]))
            for namae in namaes:
                 total = 0
                 for part in namae:
                     total +=part[1]
                 #if total == 11:
                 if total in daikichi_numbers:
                     daikichi_names.append(namae)

    print("daikichi_names@Jikaku_part",len(daikichi_names))


    #Jinkaku_part
    namaes = daikichi_names
    daikichi_names = []
    for namae in namaes:
        if type(namae) == list:
            ###if int(args.jinkaku) + namae[0] in daikichi_numbers:
            if 4 + namae[1] in daikichi_numbers:
                  daikichi_names.append(namae)
        if type(namae) == tuple:
            if 4+ namae[0][1] in daikichi_numbers:
                  daikichi_names.append(namae)
    print("daikichi_names@Jinkaku_part",len(daikichi_names))
    #print(daikichi_names)

    #Soukaku_part
    daikichi_numbers = [11,16,21,23,31,32,41,3,5,6,8,13,15,18,24,25,29,33,37,39,44,45,47,48,51,52]
    namaes = daikichi_names
    daikichi_names = []
    for namae in namaes:
        if type(namae) == list:
                 ###if args.soukaku + namae[1]  in daikichi_numbers:
                 if 7 + namae[1]  in daikichi_numbers:
                      daikichi_names.append(namae)
        if type(namae) == tuple:
            total = 0
            for part in namae:
                total +=part[1]
            ###if args.soukaku + total in daikichi_numbers:
            if 7 + total in daikichi_numbers:
                daikichi_names.append(namae)
    print("daikichi_names@Soukaku_part",len(daikichi_names))
    #print(daikichi_names)




    #Gaikaku_part
    namaes = daikichi_names
    daikichi_names = []
    for namae in namaes:
        if type(namae) == list:
                 ###if args.gaikaku + namae[1] + 1  in daikichi_numbers:
                 if 3 + namae[1] + 1 in daikichi_numbers:
                      daikichi_names.append(namae)
        if type(namae) == tuple:
            total = 0
            ###if args.soukaku + total in daikichi_numbers:
            ###if args.gaikaku + namae[-1][1] in daikichi_numbers:
            if 3 + namae[-1][1] in daikichi_numbers:
                daikichi_names.append(namae)
    if len(daikichi_names) == 0:
        daikichi_names = []
        for namae in namaes:
            if type(namae) == list:
                     ###if args.gaikaku + namae[1] + 1  in daikichi_numbers:
                     if 3 + namae[1] + 1 in kichi_numbers:
                          daikichi_names.append(namae)
            if type(namae) == tuple:
                total = 0
                ###if args.soukaku + total in daikichi_numbers:
                ###if args.gaikaku + namae[-1][1] in daikichi_numbers:
                if 3 + namae[-1][1] in daikichi_numbers:
                    daikichi_names.append(namae)


        print("daikichi_names@Gaikaku_part2",len(daikichi_names))
        #print(daikichi_names)


    for namae in daikichi_names:
        if type(namae) == list:
            print(namae[0])
        if type(namae) == tuple:
            total = ""
            for part in namae:
                total +=part[0]
            print(total)
    import code; code.interact(local=locals())
def get_kanji(letter):
    base_url= "https://mojikiban.ipa.go.jp/mji/q"
    kanjis = []
    #hiragana_part
    query = {"読み":letter,"漢字施策":"人名用漢字"}
    r = requests.get(url = base_url,params=query)
    if r.json()["find"] == False:
         print("NO RESULT FOUND")
         list = []
    else:
        list = r.json()["results"]
    for i in list:
        moji = "\\"+i['UCS']["対応するUCS"].replace("+","").replace("^","\\").lower()
        kanji = moji.encode().decode("unicode-escape")
        kanjis.append([kanji,i["総画数"]])
    #katakana_part
    another_letter = jaconv.hira2kata(letter)
    query = {"読み":another_letter,"漢字施策":"人名用漢字"}
    r = requests.get(url = base_url,params=query)
    if r.json()["find"] == False:
         print("NO RESULT FOUND")
         list = []
    else:
        list = r.json()["results"]
    for i in list:
        moji = "\\"+i['UCS']["対応するUCS"].replace("+","").replace("^","\\").lower()
        kanji = moji.encode().decode("unicode-escape")
        kanjis.append([kanji,i["総画数"]])




    return(kanjis)


parser = argparse.ArgumentParser(
                prog='Script Name',
                usage='',
                description='description',
                epilog='end',
                add_help=True,
                )
parser.add_argument('-y','--yomi', help='load log pattern for extract')
parser.add_argument('-j','--jinkaku', help='load log pattern for extract')
parser.add_argument('-g','--gaikaku', help='load log pattern for extract')
parser.add_argument('-s','--soukaku', help='load log pattern for extract')
args = parser.parse_args()

yomi = args.yomi


main()
