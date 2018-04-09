#!/usr/bin/env python

import sqlite3
from collections import defaultdict
from datetime import datetime

import pandas as pd
from janome.tokenizer import Tokenizer


BEGIN = '__BEGIN_SENTENCE__'
END = '__END_SENTENCE__'


def preprocess(df):
    """
    テキストから不要な記号を削除して、行ごとに改行を入れる
    """
    df_tweets = df['text']
    # メンションはずす
    df_tweets = df_tweets.replace('@[\w]+', '', regex=True)
    # URLはずす
    df_tweets = df_tweets.replace('https?://[^\s]+', '', regex=True)
    # スペースとタブを消す
    df_tweets = df_tweets.replace('[ \t]+', '', regex=True)
    # 区切り文字を改行に変換する
    df_tweets = df_tweets.replace('([。．\.])', r'\1\n', regex=True)
    return df_tweets


def make_triplet_freqs(sentence, triplet_freqs):
    """
    文字列を3つ組にする
    """
    # Janomeで単語に分割する
    t = Tokenizer()
    morphemes = [token.surface for token in t.tokenize(sentence)]

    if len(morphemes) < 3:
        return {}

    # 繰り返し
    for i in range(len(morphemes) - 2):
        triplet = tuple(morphemes[i:i+3])
        triplet_freqs[triplet] += 1

    # beginを追加
    triplet = (BEGIN, morphemes[0], morphemes[1])
    triplet_freqs[triplet] = 1

    # endを追加
    triplet = (morphemes[-2], morphemes[-1], END)
    triplet_freqs[triplet] = 1

    return triplet_freqs


def save(triplet_freqs):
    """
    triplet_freqsのデータをDBに保存する
    """
    # DBオープン
    con = sqlite3.connect('chain.db')
    sql = '''drop table if exists chain_freqs;
    create table chain_freqs (
    id integer primary key autoincrement not null,
    prefix1 text not null,
    prefix2 text not null,
    suffix text not null,
    freq integer not null
    );'''
    con.executescript(sql)
    # データ整形
    data = [(t[0], t[1], t[2], freq) for (t, freq) in triplet_freqs.items()]
    # データ挿入
    p_statement = u"insert into chain_freqs (prefix1, prefix2, suffix, freq) values (?, ?, ?, ?)"
    con.executemany(p_statement, data)

    # コミットしてクローズ
    con.commit()
    con.close()


def main():
    df = pd.read_csv('tweets.csv')
    df_tweets = preprocess(df)

    # 3つ組の出現回数
    triplet_freqs = defaultdict(int)
    for idx, tweet in enumerate(df_tweets):
        if idx % 100 == 0:
            print('{}: {}'.format(idx, datetime.now()))
        for sentence in tweet.splitlines():
            make_triplet_freqs(sentence, triplet_freqs)

    # DBに保存する
    save(triplet_freqs)


if __name__ == '__main__':
    main()
