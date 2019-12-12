import itertools
import requests
import jaconv
from name_devider import devide
import argparse

def main():
    myoji = args.myoji
    myoji_numbers = []
    for kanji in myoji:
        print(kanji)
        decoded_kanji = kanji.encode("unicode-escape").decode().replace("\\u","u+")
        myoji_numbers.append(get_kanji_number(decoded_kanji))
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
    myoji_number = myoji_numbers[-1]
    namaes = daikichi_names
    daikichi_names = []
    for namae in namaes:
        if type(namae) == list:
            ###if int(args.jinkaku) + namae[0] in daikichi_numbers:
            if myoji_number + namae[1] in daikichi_numbers:
                  daikichi_names.append(namae)
        if type(namae) == tuple:
            if myoji_number + namae[0][1] in daikichi_numbers:
                  daikichi_names.append(namae)
    print("daikichi_names@Jinkaku_part",len(daikichi_names))
    #print(daikichi_names)

    #Soukaku_part
    myoji_number = 0
    for i in myoji_numbers:
        myoji_number += i
    daikichi_numbers = [11,16,21,23,31,32,41,3,5,6,8,13,15,18,24,25,29,33,37,39,44,45,47,48,51,52]
    namaes = daikichi_names
    daikichi_names = []
    for namae in namaes:
        if type(namae) == list:
                 ###if args.soukaku + namae[1]  in daikichi_numbers:
                 if myoji_number + namae[1]  in daikichi_numbers:
                      daikichi_names.append(namae)
        if type(namae) == tuple:
            total = 0
            for part in namae:
                total +=part[1]
            ###if args.soukaku + total in daikichi_numbers:
            if myoji_number + total in daikichi_numbers:
                daikichi_names.append(namae)
    print("daikichi_names@Soukaku_part",len(daikichi_names))
    #print(daikichi_names)




    #Gaikaku_part
    if len(myoji_numbers) == 1:
        myoji_number = 1
    else:
        myoji_number = myoji_numbers[0]
    namaes = daikichi_names
    daikichi_names = []
    for namae in namaes:
        if type(namae) == list:
                 ###if args.gaikaku + namae[1] + 1  in daikichi_numbers:
                 if myoji_number + namae[1] + 1 in daikichi_numbers:
                      daikichi_names.append(namae)
        if type(namae) == tuple:
            total = 0
            ###if args.soukaku + total in daikichi_numbers:
            ###if args.gaikaku + namae[-1][1] in daikichi_numbers:
            if myoji_number + namae[-1][1] in daikichi_numbers:
                daikichi_names.append(namae)
    if len(daikichi_names) == 0:
        daikichi_names = []
        for namae in namaes:
            if type(namae) == list:
                     ###if args.gaikaku + namae[1] + 1  in daikichi_numbers:
                     if 6 + namae[1] + 1 in kichi_numbers:
                          daikichi_names.append(namae)
            if type(namae) == tuple:
                total = 0
                ###if args.soukaku + total in daikichi_numbers:
                ###if args.gaikaku + namae[-1][1] in daikichi_numbers:
                if 6 + namae[-1][1] in daikichi_numbers:
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
    query = {"読み":letter}
    r = requests.get(url = base_url,params=query)
    if r.json()["find"] == False:
         print("NO RESULT FOUND")
         list = []
    else:
        list = r.json()["results"]
    for i in list:
        moji = "\\"+i['UCS']["対応するUCS"].replace("+","").replace("^","\\").lower()
        kanji = chr(int(i['UCS']["対応するUCS"][2:], 16))
        kanjis.append([kanji,i["総画数"]])
    #katakana_part
    another_letter = jaconv.hira2kata(letter)
    query = {"読み":another_letter}
    r = requests.get(url = base_url,params=query)
    if r.json()["find"] == False:
         print("NO RESULT FOUND")
         list = []
    else:
        list = r.json()["results"]
    for i in list:
        kanji = chr(int(i['UCS']["対応するUCS"][2:], 16))
        kanjis.append([kanji,i["総画数"]])
    return(kanjis)

def get_kanji_number(letter):
    base_url= "https://mojikiban.ipa.go.jp/mji/q"
     
    #hiragana_part
    query = {"UCS":letter}
    r = requests.get(url = base_url,params=query)
    if r.json()["find"] == False:
         print("NO RESULT FOUND FOR:",letter)
         exit()
               
    result = r.json()["results"]
    return(result[0]["総画数"])

    

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
parser.add_argument('-m','--myoji', help='load log pattern for extract')
args = parser.parse_args()

yomi = args.yomi


main()
