import sys, urllib.request, os

BASE = "https://docs.aws.amazon.com/step-functions/latest/dg/"
OUT = "/Users/adalundhe/Projects/hecate/.claude/worktrees/collector-rigor/.scratch/"

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
        'Accept': 'text/markdown,text/plain,text/html,*/*'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.geturl(), r.read().decode('utf-8', 'replace')

for page in sys.argv[1:]:
    if page.startswith("http"):
        url = page
        name = url.rstrip('/').split('/')[-1].replace('.md', '').replace('.html', '')
    else:
        url = BASE + page + ".md"
        name = page
    try:
        final, body = fetch(url)
        path = OUT + "md_" + name + ".md"
        open(path, "w").write(body)
        print("OK  %-55s %7d chars  final=%s" % (name, len(body), final))
    except Exception as e:
        print("ERR %-55s %s" % (name, e))
