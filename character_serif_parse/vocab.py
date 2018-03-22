# -*- coding: utf-8 -*-
import MeCab
import sys

def ranking_words(word2freq,num=3,rev=False):
    rank_words = []
    i = 0
    #助詞等の情報は省く(カルピスはユーザーの呼称)
    word_rule = ['\n','…','の','て','に','は','。','も','が','た','を','カルピス','で','し','な','と','よ',',','、','「','」','!(','!)']
    for k,v in sorted(word2freq.items(),key=lambda x:x[1],reverse=rev):
        if k not in word_rule:
            rank_words.append(k)
            i += 1
            if i == num:
                break;
    return rank_words

def parse(f_name):
    #使用する変数等
    mecab = MeCab.Tagger("-Owakati")
    name_list = []
    vocab = set()
    name2vocab = {}
    serif_num = 0
    word2freq = {}
    #キャラのセリフの頻出語と希少語の取得
    name2freq_words = {}
    name2infreq_words = {}
    for line in open(f_name,'r'):
        line = line.rstrip().split(' ')
        name = line[0]
        #最初のキャラだけいれる
        if not name_list:
            name_list.append(name)
        #キャラ名が変わると変わる前のキャラのデータを作成し、セリフデータをリセットする
        if name not in name_list:
            #データ作成
            target_chara = name_list[-1]
            freq_words = ranking_words(word2freq,num=10,rev=True)
            infreq_words = ranking_words(word2freq,num=10)
            #キャラ毎のセリフ量や単語数などのデータ
            #語彙(セリフの単語数)、セリフ数、語彙力のようなものが入っている
            name2vocab[target_chara] = len(vocab),serif_num,len(vocab) / serif_num
            #頻出単語(num位まで)
            name2freq_words[target_chara] = freq_words
            name2infreq_words[target_chara] = infreq_words
            #リセット
            serif_num = 0
            name_list.append(name)
            vocab = set()
            word2freq = {}
        serif = line[1]
        serif_num += 1
        mecab_result = mecab.parse(serif).split(' ')
        for word in mecab_result:
            word2freq[word] = word2freq.get(word,0) + 1
            vocab.add(word)
    return name2vocab,name2freq_words,name2infreq_words


def output_data(name2vocab,name2freq_words,name2infreq_words):
    for name,vocab in sorted(name2vocab.items(),key=lambda x:x[1][2],reverse=True):
        print(name,vocab[1])
        print(name2freq_words[name])
        print(name2infreq_words[name])

def main():
    f_name = sys.argv[1]
    #キャラ名をキーとした辞書データ
    name2vocab,name2freq_words,name2infreq_words = parse(f_name)
    output_data(name2vocab,name2freq_words,name2infreq_words)

if __name__ == '__main__':
	main()
