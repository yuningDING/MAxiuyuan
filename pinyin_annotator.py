import re
import csv
from pypinyin import pinyin


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
                if int(human_input) <= len(pinyin_c[0]):
                    gold_pinyin_c = pinyin_c[0][int(human_input)-1]
                    print('!' + gold_pinyin_c + '! is chosen as the correct one')
                else:
                    print('Invalid annotation. !'+pinyin_c[0][0]+'! is chosen as the correct one')
                    gold_pinyin_c = pinyin_c[0][0]
                pinyin_c = [gold_pinyin_c]
                goldPinyin.append(pinyin_c)
        annotation_dictionary[word] = goldPinyin
        return goldPinyin


def export_result():
    #TODO: export items into json file
    print('results exported')


def write_dictionary(dictionary):
    with open('annotation_dictionary.csv', 'w') as f:
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
    try:
        annotation_dictionary = read_dictionary('annotation_dictionary.csv')
    except OSError as e:
        annotation_dictionary = {}

    lines = open('test.txt').readlines()
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
    write_dictionary(annotation_dictionary)

if __name__ == "__main__":
    main()
