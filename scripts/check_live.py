#!/usr/bin/env python3
"""Vérifie qu'une URL répond HTTP 200 (sans curl). Usage : check_live.py <url>"""
import sys
import urllib.request
import urllib.error


def main():
    if len(sys.argv) < 2:
        print("usage: check_live.py <url>")
        sys.exit(2)
    url = sys.argv[1]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"HTTP {r.status}")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}")
        sys.exit(1)
    except Exception as e:
        print(f"ERR {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
