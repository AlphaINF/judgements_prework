
class string2laws:
    law_name = ""
    law_list = []

    def full_width_punctuation(self, text):
        # 定义半角字符和对应的全角字符
        punc_map = {
            ',': '，',
            '.': '。',
            ';': '；',
            ':': '：',
            '?': '？',
            '!': '！',
            '(': '（',
            ')': '）',
            '[': '【',
            ']': '】',
            '{': '｛',
            '}': '｝',
            '<': '〈',
            '＜': '〈',
            '>': '〉',
            '＞':'〉'
        }

        # 创建字符映射表
        punc_map_table = str.maketrans(''.join(punc_map.keys()), ''.join(punc_map.values()))

        # 应用字符映射表
        return text.translate(punc_map_table)

    def cn_to_num(self, cn):
        if cn.startswith('十'):
            cn = '一' + cn
        num_dict = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                    '十': 10, '百': 100, '千': 1000, '万': 10000}
        cn_len = len(cn)
        num = 0
        tmp = 0
        b_unit = False  # 标识上一个字符是否为单位
        for i in range(cn_len):
            char = cn[i]
            if char in num_dict:
                val = num_dict[char]
                if val == 10 or val == 100 or val == 1000:
                    if i == 0 or b_unit:  # 首位为单位或上一个为单位，则不累加
                        b_unit = True
                    else:
                        b_unit = True
                        tmp = tmp * val
                        num += tmp
                        tmp = 0
                elif val == 10000:
                    b_unit = True
                    tmp = tmp * val
                    num += tmp
                    tmp = 0
                else:
                    b_unit = False
                    tmp = tmp + val
            else:  # 非数字
                return None
        num += tmp
        return num

    def __init__(self,string):
        self.law_name = ""
        self.law_list = []

        string = self.full_width_punctuation(string)

        name_first = string.find('《')
        name_last = string.find('》')

        self.law_name = string[name_first + 1: name_last]
        details = string[name_last+1:].split('、')

        tags = ['条','款','项']
        last_answer = [0, 0, 0]

        for detail in details:
            detail = detail.replace('（','')
            detail = detail.replace('）', '')
            answer = []
            for tag in tags:
                id = detail.find(tag)
                if id != -1:
                    sta = detail.find('第')
                    answer.append(self.cn_to_num(detail[sta+1:id]))
                    detail = detail[id+1:]
                else:
                    answer.append(0)

            if answer[0] == 0:
                answer[0] = last_answer[0]
                if answer[1] == 0:
                    answer[1] = last_answer[1]

            last_answer = answer
            if answer[2] == 0:
                answer.pop(2)
            if answer[1] == 0:
                answer.pop(1)
            self.law_list.append(answer)

    def outall(self):
        answers = []
        for one in self.law_list:
            answer = '《' + self.law_name + '》' + str(one)
            answers.append(answer)
        return answers

mp = {}
with open('../files/law_use_劳动争议.txt','r', encoding='utf-8', errors='ignore') as file:
    while True:
        string = file.readline()
        if string == '':
            break
        try:
            a = string2laws(string)
            for line in a.outall():
                if not line in mp:
                    mp[line] = 0
                mp[line] += 1
        except:
            a = ''

with open('../files/law_prob_劳动争议.txt','w', encoding = 'utf-8', errors='ignore') as f:
    for key, value in mp.items():
        f.write(key)
        f.write('\t')
        f.write(str(value))
        f.write('\n')