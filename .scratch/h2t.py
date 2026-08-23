import sys, re, html, urllib.request

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,*/*'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode('utf-8', 'replace')

def to_text(h, isolate=True):
    h = re.sub(r'(?is)<(script|style|svg|noscript)\b.*?</\1>', ' ', h)
    h = re.sub(r'(?is)<nav\b.*?</nav>', ' ', h)
    h = re.sub(r'(?is)<footer\b.*?</footer>', ' ', h)
    if isolate:
        m = re.search(r'(?is)<article\b[^>]*>(.*?)</article>', h)
        if not m:
            m = re.search(r'(?is)<main\b[^>]*>(.*?)</main>', h)
        if m:
            h = m.group(1)
    h = re.sub(r'(?is)<br\s*/?>', '\n', h)
    h = re.sub(r'(?is)</(p|div|li|tr|h1|h2|h3|h4|h5|h6|pre|section|table|thead|tbody|dd|dt)>', '\n', h)
    h = re.sub(r'(?is)<(h1|h2|h3|h4|h5|h6)[^>]*>', '\n\n#### ', h)
    h = re.sub(r'(?is)<li[^>]*>', '\n- ', h)
    h = re.sub(r'(?is)<t[dh][^>]*>', ' | ', h)
    h = re.sub(r'(?s)<[^>]+>', '', h)
    h = html.unescape(h)
    h = re.sub(r'[ \t]+', ' ', h)
    h = re.sub(r'\n\s*\n\s*\n+', '\n\n', h)
    return h.strip()

if __name__ == '__main__':
    url = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    raw = fetch(url)
    t = to_text(raw)
    if len(t) < 500:
        t = to_text(raw, isolate=False)
    if out:
        open(out, 'w').write(t)
        print("WROTE %s (%d chars) from %s" % (out, len(t), url))
    else:
        print(t)
