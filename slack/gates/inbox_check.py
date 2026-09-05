#!/usr/bin/env python3
"""Read-only: replies from endorsers (Wood, Por, Prellberg, Pikhurko, Schmitt, Warrington, Kaplan) or arXiv mail in studio@ over the last 4 days."""
from google.oauth2 import service_account
from googleapiclient.discovery import build
KEY = "/Users/iwasborninbali/.config/nusadua-studio-agent/sa-key.json"; ME = "studio@nusadua.dev"
creds = service_account.Credentials.from_service_account_file(KEY, scopes=["https://mail.google.com/"]).with_subject(ME)
svc = build("gmail", "v1", credentials=creds)
q = "newer_than:4d (from:monash.edu OR from:wku.edu OR from:arxiv.org OR from:uni-bielefeld.de OR from:qmul.ac.uk OR from:warwick.ac.uk OR from:middlebury.edu OR from:uvm.edu OR from:uci.edu OR subject:endorse OR subject:endorsement)"  # Gmail matches whole words: endorse != endorsement (missed Prellberg 5.09)
res = svc.users().messages().list(userId="me", q=q, maxResults=20).execute()
msgs = res.get("messages", [])
print("писем по запросу:", len(msgs))
for m in msgs:
    h = {x["name"]: x["value"] for x in svc.users().messages().get(userId="me", id=m["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"]).execute()["payload"]["headers"]}
    print("  ", h.get("Date", "")[:22], "|", h.get("From", "")[:45], "|", h.get("Subject", "")[:70])
