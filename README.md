# markov

* sample code for markov chain

## env

```
$ python3.6 -mv venv env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
```

## analyze

* Download full tweets data form twitter(zip file)
* unzip tweets data and copy tweets.csv
* run text2markov_chain.py

```
(env) $ python text2markov_chain.py
```

## generate

* run generate_text.py

```
(env) $ python generate_text.py
アカウント作っている。
(env) $ python generate_text.py
名古屋みやげのTシャツです。
```

## reference

* [マルコフ連鎖を使って自分らしい文章をツイートする - Qiita](https://qiita.com/hitsumabushi845/items/647f8bbe8d399f76825c)
* [Pythonリハビリのために文章自動生成プログラムを作ってみた - \[\[ともっくす alloc\] init\]](http://o-tomox.hatenablog.com/entry/2014/11/14/190632)
* [o-tomox/TextGenerator: マルコフ連鎖を使った文章自動生成プログラム](https://github.com/o-tomox/TextGenerator)
