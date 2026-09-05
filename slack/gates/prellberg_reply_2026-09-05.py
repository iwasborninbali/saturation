#!/usr/bin/env python3
"""Reply to Thomas Prellberg in his own thread (arXiv endorsement, 5 Sep 2026), from studio@nusadua.dev via the Gmail API.
Owner's word: "отправляй письмо бро" (5 Sep 22:45 WITA). Body = docs/correspondence/drafts/prellberg_reply_2026-09-05.md.
Threading: In-Reply-To / References = his Message-ID; threadId = the thread of our request of 5 Sep 07:50 WITA."""
import base64, json, sys, time
from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
KEY = "/Users/iwasborninbali/.config/nusadua-studio-agent/sa-key.json"; ME = "studio@nusadua.dev"
TO = "Thomas Prellberg <t.prellberg@qmul.ac.uk>"
SUBJECT = "Re: arXiv endorsement request (math.CO): no-three-in-line in the cube"
HIS_MSGID = "<AS4PR07MB877715F2CC397F6BDEB8B490CCB42@AS4PR07MB8777.eurprd07.prod.outlook.com>"
THREAD = "1a06ed4c42e21004"
BODY = """Dear Professor Prellberg,

Thank you — that is very kind, and the timing is no problem at all: I will simply wait until 2606.08834 counts.

I will gladly keep you posted. The two notes will appear on arXiv as soon as the endorsement goes through, and I will send you
their identifiers together with whatever is new on the three-dimensional problem by then.

With best regards,
Aleksei Kudriashov (Alex Komang)
Independent researcher, Nusa Dua, Bali, Indonesia
studio@nusadua.dev — https://github.com/iwasborninbali
"""
OUT = "/Users/iwasborninbali/saturation/docs/correspondence/prellberg_reply_sent_2026-09-05.json"
def main(dry):
    msg = EmailMessage(); msg["To"] = TO; msg["From"] = f"Aleksei Kudriashov <{ME}>"; msg["Subject"] = SUBJECT
    msg["In-Reply-To"] = HIS_MSGID; msg["References"] = HIS_MSGID; msg.set_content(BODY)
    if dry: print(msg.as_string()); return
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=["https://mail.google.com/"]).with_subject(ME)
    svc = build("gmail", "v1", credentials=creds)
    r = svc.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode(), "threadId": THREAD}).execute()
    rec = {"to": TO, "id": r.get("id"), "threadId": r.get("threadId"), "sent": time.strftime("%Y-%m-%d %H:%M:%S %z")}
    json.dump(rec, open(OUT, "w"), indent=1); print("sent:", rec)
if __name__ == "__main__": main(dry="--dry" in sys.argv)
