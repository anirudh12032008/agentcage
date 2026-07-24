from pathlib import Path

DIR = (Path(__file__).parent.parent / "fake_pages").resolve()

URL = {
    "https://example.com/faq": "company_faq.html",
    "https://blog.com/post1": "malicious.html",
}

def fetch(url: str) -> str:
    if url not in URL:
        return "ERROR: no such url here"
    filename = URL[url]
    t = (DIR/ filename)
    if not t.is_file():
        return "ERROR: file missing"
    return t.read_text()