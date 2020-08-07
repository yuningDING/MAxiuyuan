import re
from pypinyin import pinyin
import signal


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


def annotate(word):
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
    return goldPinyin


def export_result():
    print('results exported')


def main():
    lines = open('test.txt').readlines()
    current_line = 0
    for line in lines[::-1]:
        # skip empty line
        if not line.strip():
            current_line+=1
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
                goldPinyin = annotate(word)
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


if __name__ == "__main__":
    main()
