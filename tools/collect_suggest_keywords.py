# -*- coding: utf-8 -*-
"""Collect Naver and Google autocomplete suggestions for flagship model families.

Usage: python3 collect.py out.csv
Needs network access to ac.search.naver.com and suggestqueries.google.com.
"""
import csv, json, sys, time, urllib.parse, urllib.request

FAMILIES = {
    '갤럭시 S26': ['갤럭시 s26', '갤럭시s26', 's26', '갤럭시 s26 울트라', '갤럭시 s26 플러스', '갤럭시 s26 fe', 's26 울트라'],
    '아이폰17': ['아이폰17', '아이폰 17', '아이폰17 프로', '아이폰17 프로맥스', '아이폰 에어', '아이폰17e', 'iphone 17'],
    '아이폰18': ['아이폰18', '아이폰 18', '아이폰18 프로', '아이폰18 프로맥스', '아이폰 듀오', '아이폰 폴드', 'iphone 18'],
    '갤럭시 S27': ['갤럭시 s27', '갤럭시s27', 's27', '갤럭시 s27 울트라', 's27 울트라'],
    '갤럭시 Z폴드8': ['갤럭시 z폴드8', '폴드8', '갤럭시 폴드8', '폴드8 울트라', 'z폴드8'],
    '갤럭시 Z플립8': ['갤럭시 z플립8', '플립8', '갤럭시 플립8', 'z플립8', '플립8 fe'],
}
# Suffixes widen the autocomplete beyond the top 10 for each seed.
SUFFIXES = [''] + [' ' + c for c in 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ'] + [' ' + c for c in 'abcdefghijklmnopqrstuvwxyz0123456789']
UA = {'User-Agent': 'Mozilla/5.0'}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode('utf-8', 'replace')


def naver(q):
    url = 'https://ac.search.naver.com/nx/ac?' + urllib.parse.urlencode({
        'q': q, 'con': 1, 'frm': 'nv', 'ans': 2, 'r_format': 'json', 'r_enc': 'UTF-8',
        'r_unicode': 0, 't_koreng': 1, 'run': 2, 'rev': 4, 'q_enc': 'UTF-8', 'st': 100})
    data = json.loads(get(url))
    return [item[0] for group in data.get('items', []) for item in group if item]


def google(q):
    url = 'https://suggestqueries.google.com/complete/search?' + urllib.parse.urlencode({'client': 'firefox', 'hl': 'ko', 'gl': 'kr', 'q': q})
    return json.loads(get(url))[1]


def main(out):
    seen = {}
    for fam, seeds in FAMILIES.items():
        for seed in seeds:
            for suf in SUFFIXES:
                q = seed + suf
                for engine, fn in (('네이버', naver), ('구글', google)):
                    try:
                        sugg = fn(q)
                    except Exception as e:  # noqa: BLE001 - keep going on one bad query
                        print('fail', engine, q, e, file=sys.stderr)
                        continue
                    for s in sugg:
                        key = (fam, s.replace(' ', '').lower())
                        row = seen.setdefault(key, {'family': fam, 'keyword': s, 'engines': set(), 'seeds': set()})
                        row['engines'].add(engine)
                        row['seeds'].add(q)
                    time.sleep(0.15)
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['번호', '모델군', '키워드', '나온 검색창', '찾은 입력어'])
        rows = sorted(seen.values(), key=lambda r: (r['family'], -len(r['engines']), r['keyword']))
        for i, r in enumerate(rows, 1):
            w.writerow([i, r['family'], r['keyword'], '·'.join(sorted(r['engines'])), ' | '.join(sorted(r['seeds']))[:200]])
    print('rows', len(seen))


if __name__ == '__main__':
    main(sys.argv[1])
