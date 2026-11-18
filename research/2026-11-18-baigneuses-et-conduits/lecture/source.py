"""Extrait les vers numérotés de Monumenta. Le répertoire HTML est un cache local."""
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, urljoin

BASE = "https://monumenta.ch/latein/"
INDEX = BASE + "verzeichnis4.php?lang=0&level=3&tabelle=Petrus_de_Ebulo&xy=Petrus+de+Ebulo,+De+Balneis+Puteolanis"


class Catalogue(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = {}
        self.url = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("class") == "titel99":
            self.url = urljoin(BASE, quote(attrs["href"], safe=":/?&=+,%"))

    def handle_endtag(self, tag):
        if tag == "a":
            self.url = None

    def handle_data(self, data):
        if self.url:
            self.links[data.strip()] = self.url


class Vers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.number = None
        self.in_anchor = False
        self.lines = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.in_anchor = True
            if attrs.get("class") == "satznummer":
                self.number = int(attrs["name"])
                assert self.number not in self.lines
                self.lines[self.number] = []

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_anchor = False
        if tag in ("table", "body"):
            self.number = None

    def handle_data(self, data):
        if self.number and not self.in_anchor:
            self.lines[self.number].append(data)


def download(url, dest):
    if not dest.exists():
        subprocess.run(["curl","--fail","--location","--retry","2","--silent","--show-error",
                        "--output",str(dest),url],check=True)
    return dest.read_text()


def extract(folder):
    folder.mkdir(parents=True, exist_ok=True)
    index = Catalogue()
    index.feed(download(INDEX, folder / "index.html"))
    assert len(index.links) == 34
    items = []
    for i, (title, url) in enumerate(index.links.items()):
        parsed = Vers()
        parsed.feed(download(url, folder / f"{i:02}.html"))
        assert list(parsed.lines) == list(range(1,len(parsed.lines)+1)) and parsed.lines, title
        lines = [" ".join("".join(parts).split()) for parts in parsed.lines.values()]
        assert all(re.fullmatch(r"[A-Za-zÀ-ž ~·,.;:!?()’'\-\[\]]+", line) for line in lines), (title,lines)
        items.append(dict(titre=title,url=url,vers=lines))
    return items


if __name__ == "__main__":
    folder = Path(sys.argv[1])
    items = extract(folder)
    data = (json.dumps(items, ensure_ascii=False,indent=1)+"\n").encode()
    sha = sha256(data).hexdigest()
    local = Path(__file__).resolve().parent
    manifest = [dict(titre=c["titre"],url=c["url"],vers=len(c["vers"])) for c in items]
    evidence = dict(sha256=sha, notices=manifest)
    descriptor = local / "SOURCE.json"
    if descriptor.exists():
        assert json.loads(descriptor.read_text()) == evidence, "La source ou la segmentation a changé"
    else:
        descriptor.write_text(json.dumps(evidence,ensure_ascii=False,indent=1)+"\n")
    (folder / "vers.json").write_bytes(data)
    print(len(items),sum(len(c["vers"]) for c in items),sha)
