import json
import subprocess
import urllib.request
import sys

def get_token():
    try:
        cred = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            text=True,
            capture_output=True,
            check=True,
        )
        for line in cred.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1]
    except Exception:
        pass
    return None

token = get_token()

def api_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "repo-monitor",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))

print("=================== 1. RMerl/asuswrt-merlin.ng ===================")
for branch in ("3004.388", "main", "3006.102-wifi6"):
    try:
        cs = api_get(f"https://api.github.com/repos/RMerl/asuswrt-merlin.ng/commits?sha={branch}&per_page=3")
        print(f"[{branch}]")
        for c in cs:
            print(f"  {c['sha'][:8]} {c['commit']['author']['date']} | {c['commit']['message'].splitlines()[0]}")
    except Exception as e:
        print(f"  [{branch}] Error: {e}")

try:
    prs = api_get("https://api.github.com/repos/RMerl/asuswrt-merlin.ng/pulls?state=all&sort=updated&direction=desc&per_page=5")
    print("Recent PRs:")
    for p in prs:
        print(f"  #{p['number']} [{p['state']}] updated={p['updated_at']} @{p['user']['login']}: {p['title']}")
except Exception as e:
    print(f"PRs Error: {e}")

print("\n=================== 2. gnuton/asuswrt-merlin.ng ===================")
for branch in ("master", "master-3006"):
    try:
        cs = api_get(f"https://api.github.com/repos/gnuton/asuswrt-merlin.ng/commits?sha={branch}&per_page=3")
        print(f"[{branch}]")
        for c in cs:
            print(f"  {c['sha'][:8]} {c['commit']['author']['date']} | {c['commit']['message'].splitlines()[0]}")
    except Exception as e:
        print(f"  [{branch}] Error: {e}")

try:
    g_prs = api_get("https://api.github.com/repos/gnuton/asuswrt-merlin.ng/pulls?state=all&sort=updated&direction=desc&per_page=5")
    print("Recent PRs:")
    for p in g_prs:
        print(f"  #{p['number']} [{p['state']}] updated={p['updated_at']} @{p['user']['login']}: {p['title']}")
except Exception as e:
    print(f"gnuton PRs Error: {e}")

try:
    g_issues = api_get("https://api.github.com/repos/gnuton/asuswrt-merlin.ng/issues?state=all&sort=updated&direction=desc&per_page=4")
    print("Recent Issues:")
    for i in g_issues:
        if "pull_request" not in i:
            print(f"  #{i['number']} [{i['state']}] updated={i['updated_at']} @{i['user']['login']}: {i['title']}")
except Exception as e:
    print(f"gnuton Issues Error: {e}")

print("\n=================== 3. Watched Forks ===================")
fork_names = [
    "jef00/asuswrt-merlin.ng",
    "ste94pz/asuswrt-merlin.ng",
    "m0wseu/asuswrt-merlin.ng",
    "bstard/asuswrt-merlin.ng",
    "kaaburgh/asuswrt-merlin.ng",
]

for repo in fork_names:
    try:
        info = api_get(f"https://api.github.com/repos/{repo}")
        print(f"[{repo}] pushed_at={info.get('pushed_at')}")
    except Exception as e:
        print(f"[{repo}] Error: {e}")

try:
    forks = api_get("https://api.github.com/repos/gnuton/asuswrt-merlin.ng/forks?sort=newest&per_page=50")
    active_forks = [f for f in forks if (f.get("pushed_at") or "") > "2026-11-13T00:00:00Z"]
    active_forks = sorted(active_forks, key=lambda x: x.get("pushed_at") or "", reverse=True)
    if active_forks:
        print("Forks pushed since Nov 13:")
        for f in active_forks:
            print(f"  {f['full_name']} | pushed_at={f['pushed_at']}")
    else:
        print("No new forks pushed since Nov 13.")
except Exception as e:
    print(f"Fork discovery error: {e}")

if "--detail" in sys.argv:
    print("\n=================== 4. Detailed Updates ===================")
    try:
        m_cs = api_get("https://api.github.com/repos/m0wseu/asuswrt-merlin.ng/commits?per_page=3")
        print("[m0wseu latest commits]")
        for c in m_cs:
            print(f"  {c['sha'][:8]} {c['commit']['author']['date']} | {c['commit']['message'].splitlines()[0]}")
    except Exception as e:
        print(f"m0wseu error: {e}")

    try:
        p923 = api_get("https://api.github.com/repos/RMerl/asuswrt-merlin.ng/pulls/923")
        print(f"[RMerl PR #923] updated={p923['updated_at']} commits={p923['commits']}")
        p923_cs = api_get("https://api.github.com/repos/RMerl/asuswrt-merlin.ng/pulls/923/commits?per_page=3")
        for c in p923_cs[-2:]:
            print(f"  {c['sha'][:8]} {c['commit']['author']['date']} | {c['commit']['message'].splitlines()[0]}")
    except Exception as e:
        print(f"PR 923 error: {e}")

    try:
        issue1026 = api_get("https://api.github.com/repos/gnuton/asuswrt-merlin.ng/issues/1026/comments?per_page=3")
        print("[gnuton Issue #1026 latest comment]")
        if issue1026:
            c = issue1026[-1]
            print(f"  @{c['user']['login']} ({c['created_at']}): {c['body'][:220].replace(chr(10), ' ')}")
    except Exception as e:
        print(f"Issue 1026 error: {e}")

