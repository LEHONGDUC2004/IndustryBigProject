import os, requests
from urllib.parse import urlparse

def _parse(url: str):
    u = urlparse(url.strip())
    assert u.netloc in ("github.com", "www.github.com"), "Only github.com allowed"
    parts = [p for p in u.path.split("/") if p]
    assert len(parts) >= 2, "URL must be github.com/<owner>/<repo>"
    owner = parts[0]
    repo  = parts[1].removesuffix(".git")
    ref_in_url = parts[3] if len(parts) >= 4 and parts[2] in ("tree","tag","releases","commit") else None
    return owner, repo, ref_in_url

def download_public_zip(github_url: str, dest_dir: str, ref: str | None = None, max_mb: int = 200):
    owner, repo, ref_in_url = _parse(github_url)
    chosen = (ref or ref_in_url or "main").strip()
    os.makedirs(dest_dir, exist_ok=True)

    tried = [chosen] + (["master"] if chosen != "master" else [])
    for candidate in tried:
        zip_url = f"https://codeload.github.com/{owner}/{repo}/zip/{candidate}"
        r = requests.get(zip_url, stream=True, timeout=20)
        if r.status_code != 200:
            continue
        filename = f"{repo}-{candidate}.zip"
        out_path = os.path.join(dest_dir, filename)
        limit = max_mb * 1024 * 1024
        total = 0
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(262_144):
                if not chunk: continue
                total += len(chunk)
                assert total <= limit, "ZIP too large"
                f.write(chunk)
        return out_path, filename

    raise ValueError(f"{owner}/{repo} (tried: {', '.join(tried)})")
