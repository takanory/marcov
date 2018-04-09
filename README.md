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