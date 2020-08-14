import re
import csv
from pypinyin import pinyin
import json


class Item:
    def __init__(self, id, token_list, pos_list, character_list, pypinyin_list, gold_pinyin_list):
        self.id = id
        self.token_list = token_list
        self.pos_list = pos_list
        self.character_list = character_list
        self.pypinyin_list = pypinyin_list
        self.gold_pinyin_list = gold_pinyin_list

    def printText(self):
        print(self.id + ':' + ' '.join(self.token_list))

    def printPos(self):
        print(self.id + ':' + ' '.join(self.pos_list))

    def printCharacter(self):
        print(self.id + ':' + ' '.join(self.character_list))

    def printPyPinyin(self):
        print(self.id + ':' + ' '.join(self.pypinyin_list))

    def printGoldPinyin(self):
        print(self.id + ':' + ' '.join(self.gold_pinyin_list))


def annotate(annotation_dictionary, word):
    if word.startswith('['):
        word = word[1:]
    if word in annotation_dictionary.keys():
        return annotation_dictionary.get(word)
    else:
        goldPinyin = []
        for c in word:
            pinyin_c = pinyin(c, heteronym=True)
            if len(pinyin_c[0]) ==1:
                pinyin_c = pinyin_c[0]
                goldPinyin.append(pinyin_c)
            else:
                print(word)
                print(pinyin_c[0])
                human_input = input('Please enter the correct pinyin:\n')
                if human_input.isdigit() and int(human_input) <= len(pinyin_c[0]):
                    gold_pinyin_c = pinyin_c[0][int(human_input)-1]
                    print('!' + gold_pinyin_c + '! is chosen as the correct one')
                else:
                    print('Invalid annotation. NaN is annotated')
                    gold_pinyin_c = 'NaN'
                pinyin_c = [gold_pinyin_c]
                goldPinyin.append(pinyin_c)
        annotation_dictionary[word] = goldPinyin
        return goldPinyin


def list_to_string(list):
    return '*'.join(list)


def export_result(data, outfile):
    with open(outfile, 'w') as f:
        for d in data:
            f.write(d.id+'\t'+list_to_string(d.token_list)+'\t'+list_to_string(d.character_list)+'\t'+list_to_string(d.pos_list)+'\t'+list_to_string(d.pypinyin_list)+'\t'+list_to_string(d.gold_pinyin_list))
    print('results exported')



def write_dictionary(dictionary):
    with open('annotation_dictionary.csv', 'w', encoding='utf-8') as f:
        for key in dictionary.keys():
            f.write("%s\t%s\n" % (key, dictionary[key]))


def read_dictionary(dictionary_path):
    annotation_dictionary = {}
    with open(dictionary_path, mode='r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            pinyin_array = []
            word = row[0]
            pinyin = row[1]
            matches = re.findall('\[\'.*?\'\]', pinyin, re.DOTALL)
            for m in matches:
                m = m.strip('\[\'\'\]')
                pinyin_array.append([m])
            annotation_dictionary[word] = pinyin_array
    return annotation_dictionary


def main():
    data = []
    try:
        annotation_dictionary = read_dictionary('annotation_dictionary.csv')
    except OSError as e:
        annotation_dictionary = {}

    lines = open('19980128.txt', encoding='utf-8').readlines()
    for line in lines:
        # skip empty line
        if not line.strip():
            continue
        print('******')
        print(line)
        item = Item(000,[],[],[],[],[])
        tokens = line.split('  ')
        for t in tokens:
            parts = t.split('/')
            word = parts[0]
            pos = parts[1]
            # find id
            patternID = re.compile('\d{8}-\d{2}-\d{3}-\d{3}')
            if patternID.match(word):
                item.id = word
                continue
            patternPoly = re.compile('\{.*\}')
            # find words contain polyphones
            if patternPoly.search(word):
                matches = re.findall('\{.*?\}', word, re.DOTALL)
                for m in matches:
                    word = re.sub(m, '', word)
                pyPinyin = pinyin(word)
                goldPinyin = annotate(annotation_dictionary, word)
            else:
                # find pinyin for normal words
                pyPinyin = pinyin(word)
                goldPinyin = pyPinyin
            # save word, pos, characters, pyPinyin and goldPinyin in Item
            item.token_list.append(word)
            item.pos_list.append(pos)
            for c in word:
                item.character_list.append(c)
            for p in pyPinyin:
                item.pypinyin_list.append(p[0])
            for p in goldPinyin:
                item.gold_pinyin_list.append(p[0])
        data.append(item)
    write_dictionary(annotation_dictionary)
    export_result(data, 'out_19980128_yd.tsv')

if __name__ == "__main__":
    main()
