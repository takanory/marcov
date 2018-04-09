#!/usr/bin/env python

import random
import sqlite3

from text2markov_chain import BEGIN, END


def get_chains(con, prefixes):
    """
    指定したprefixがある情報を取得する
    """
    sql = "select prefix1, prefix2, suffix, freq from chain_freqs where prefix1 = ?"
    if len(prefixes) == 2:
        sql += " and prefix2 = ?"
    result = []
    cursor = con.execute(sql, prefixes)
    for row in cursor:
        result.append(dict(row))
    return result


def get_probable_triplet(chains):
    probability = []

    # 確率に合うように、インデックスを入れる
    for (index, chain) in enumerate(chains):
        for j in range(chain["freq"]):
            probability.append(index)

    # ランダムに1つを選ぶ
    chain_index = random.choice(probability)

    return chains[chain_index]


def get_first_triplet(con):
    prefixes = (BEGIN,)
    # チェーン情報を取得
    chains = get_chains(con, prefixes)
    # 取得したチェーンから、確率的に1つ選ぶ
    triplet = get_probable_triplet(chains)
    return (triplet["prefix1"], triplet["prefix2"], triplet["suffix"])


def get_triplet(con, prefix1, prefix2):
    # BEGINをprefix1としてチェーンを取得
    prefixes = (prefix1, prefix2)

    # チェーン情報を取得
    chains = get_chains(con, prefixes)
    # 取得したチェーンから、確率的に1つ選ぶ
    triplet = get_probable_triplet(chains)

    return (triplet["prefix1"], triplet["prefix2"], triplet["suffix"])


def main():
    con = sqlite3.connect('chain.db')
    con.row_factory = sqlite3.Row
    generated_text = ''

    morphemes = []
    # はじまりを取得
    first_triplet = get_first_triplet(con)
    morphemes.append(first_triplet[1])
    morphemes.append(first_triplet[2])

    # 文章を紡いでいく
    while morphemes[-1] != END:
        prefix1 = morphemes[-2]
        prefix2 = morphemes[-1]
        triplet = get_triplet(con, prefix1, prefix2)
        morphemes.append(triplet[2])

    result = "".join(morphemes[:-1])
    print(result)


if __name__ == '__main__':
    main()
