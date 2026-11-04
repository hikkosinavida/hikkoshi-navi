#!/usr/bin/env python3
"""IndexNowで検索エンジンに新しいURL・直したURLを知らせる。

  python3 indexnow.py blog/slug.html blog/slug2.html   指定したページだけ
  python3 indexnow.py --all                            sitemap.xmlの全URL
"""
import json, re, sys, urllib.request

HOST = "hikkosi-navi.com"
KEY = "ce4ba61d59f7908f3af983af939c9fa1"

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
if args == ["--all"]:
    urls = re.findall(r"<loc>(.*?)</loc>", open("public/sitemap.xml", encoding="utf-8").read())
else:
    urls = [f"https://{HOST}/{a.removeprefix('public/')}" for a in args]

body = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/{KEY}.txt",
    "urlList": urls,
}).encode()
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=body,
    headers={"Content-Type": "application/json; charset=utf-8"},
)
with urllib.request.urlopen(req) as res:
    print(res.status, len(urls), "件を送信")
