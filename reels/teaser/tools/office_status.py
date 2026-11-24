# Content agent -> AI Office status.
# Writes this agent's tasks to the office_status table in Supabase, which the office page reads every 5 s.
# Status text only: never put customer names, phone numbers or message text here.
#
#   python3 tools/office_status.py set "Social Media" "Reel: Own a local business? (13 s)" Running
#   python3 tools/office_status.py set "Social Media" "Reel ready: waiting for your OK to post" "Waiting for you"
#   python3 tools/office_status.py set "Social Media" "Reel posted to Instagram, Facebook, TikTok" Done
#
# Needs env vars (set in the environment, never committed):
#   SUPABASE_URL          https://wxmmixqqerdejkpigroa.supabase.co
#   SUPABASE_SERVICE_KEY  service role key (server-side only; NOT the publishable key in the page)
import json, os, sys, time, urllib.request, urllib.error

VALID = {"Running", "Waiting for you", "Not started yet", "Done", "Cancelled"}

def _env(name):
    v = os.environ.get(name, "").strip()
    if not v:
        sys.exit(f"missing env var {name}")
    return v

def read_tasks(agent):
    url = _env("SUPABASE_URL") + "/rest/v1/office_status?select=tasks&agent=eq." + urllib.request.quote(agent)
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=20) as r:
        rows = json.loads(r.read() or b"[]")
    return rows[0]["tasks"] if rows else []

def _headers():
    k = _env("SUPABASE_SERVICE_KEY")
    return {"apikey": k, "Authorization": "Bearer " + k, "Content-Type": "application/json"}

def set_task(agent, title, status, keep_last=8):
    if status not in VALID:
        sys.exit(f"status must be one of {sorted(VALID)}")
    tasks = [t for t in read_tasks(agent) if t[0] != title]          # update the same task instead of duplicating it
    tasks.insert(0, [title, status])
    tasks = tasks[:keep_last]
    body = json.dumps({"tasks": tasks, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}).encode()
    url = _env("SUPABASE_URL") + "/rest/v1/office_status?agent=eq." + urllib.request.quote(agent)
    req = urllib.request.Request(url, data=body, method="PATCH", headers={**_headers(), "Prefer": "return=minimal"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        sys.exit(f"Supabase rejected the update: HTTP {e.code}")

if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "set":
        print("ok", set_task(sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        sys.exit(__doc__)
