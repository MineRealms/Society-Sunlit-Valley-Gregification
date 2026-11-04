#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs/PLAYER_GUIDE.zh-CN.md -> 玩家教程 PDF（Chrome headless 打印）

用法:
    python docs/player-kit/build_guide_pdf.py [--out 路径]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'docs', 'PLAYER_GUIDE.zh-CN.md')

CHROME_CANDIDATES = [
    r'C:/Program Files/Google/Chrome/Application/chrome.exe',
    r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]

CSS = """
@page { size: A4; margin: 18mm 16mm 16mm; }
* { box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", sans-serif;
  font-size: 10.5pt; line-height: 1.75; color: #1c1a14; margin: 0;
}
h1 {
  font-size: 21pt; line-height: 1.3; margin: 0 0 6mm; padding-bottom: 4mm;
  border-bottom: 2px solid #d9a441; letter-spacing: -.02em;
}
h2 {
  font-size: 14pt; margin: 8mm 0 3mm; padding-left: 3mm;
  border-left: 4px solid #d9a441; line-height: 1.4;
  page-break-after: avoid;
}
h3 { font-size: 11.5pt; margin: 5mm 0 2mm; color: #4a4231; page-break-after: avoid; }
p { margin: 2mm 0; }
strong { color: #8a5a00; }
ul, ol { margin: 2mm 0 2mm 0; padding-left: 6mm; }
li { margin: 1mm 0; }
a { color: #8a5a00; text-decoration: none; word-break: break-all; }
code {
  font-family: "Cascadia Mono", Consolas, "SF Mono", Menlo, monospace;
  font-size: 9.5pt; background: #f4efe3; padding: .5mm 1.4mm; border-radius: 2px;
}
pre {
  background: #f7f3e9; border: 1px solid #e6ddc8; border-radius: 4px;
  padding: 3mm 4mm; margin: 3mm 0; page-break-inside: avoid; overflow: hidden;
}
pre code { background: none; padding: 0; font-size: 9pt; line-height: 1.6; white-space: pre-wrap; }
table {
  width: 100%; border-collapse: collapse; margin: 3mm 0; font-size: 9.5pt;
}
tr { page-break-inside: avoid; }
th, td { border: 1px solid #ddd3bd; padding: 1.6mm 2.4mm; text-align: left; vertical-align: top; }
th { background: #f6f1e4; font-weight: 700; }
blockquote {
  margin: 3mm 0; padding: 2mm 4mm; background: #fbf7ec;
  border-left: 3px solid #e0c98d; color: #4a4231; page-break-inside: avoid;
}
blockquote p { margin: 1mm 0; }
hr { border: 0; border-top: 1px solid #e6ddc8; margin: 6mm 0; }
h2, h3 { break-after: avoid; }
"""


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    for name in ('chrome', 'google-chrome', 'msedge'):
        p = shutil.which(name)
        if p:
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'player-kit',
                                                  '[教程]怎么游玩Sunlit服务器.pdf'))
    ap.add_argument('--html-only', action='store_true')
    args = ap.parse_args()

    if not os.path.exists(SRC):
        print('missing %s' % SRC)
        return 1

    with open(SRC, encoding='utf-8') as fh:
        text = fh.read()

    body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists'])
    html = (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<title>怎么游玩 Society Sunlit Valley 服务器</title>'
        '<style>%s</style></head><body>%s</body></html>' % (CSS, body)
    )

    out_dir = os.path.dirname(args.out)
    os.makedirs(out_dir, exist_ok=True)
    tmp_html = os.path.join(tempfile.gettempdir(), 'sunlit_guide_%d.html' % int(time.time()))
    with open(tmp_html, 'w', encoding='utf-8') as fh:
        fh.write(html)

    if args.html_only:
        print('html -> %s' % tmp_html)
        return 0

    chrome = find_chrome()
    if not chrome:
        print('找不到 Chrome / Edge，无法打印 PDF')
        return 1

    # 先写临时名再改名：目标被 WPS/阅读器锁住时 Chrome 会静默失败
    tmp_pdf = args.out + '.tmp.pdf'
    if os.path.exists(tmp_pdf):
        os.remove(tmp_pdf)

    cmd = [
        chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
        '--no-pdf-header-footer', '--virtual-time-budget=6000',
        '--print-to-pdf=' + tmp_pdf,
        'file:///' + tmp_html.replace('\\', '/'),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(tmp_pdf) or os.path.getsize(tmp_pdf) < 5000:
        print('PDF 生成失败')
        print((res.stderr or '')[-800:])
        return 1

    os.replace(tmp_pdf, args.out)
    print('PDF -> %s (%d bytes)' % (args.out, os.path.getsize(args.out)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
