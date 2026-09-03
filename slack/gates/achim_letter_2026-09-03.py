#!/usr/bin/env python3
"""Письмо Ахиму Фламменкампу (одно, короткое, по его вкусу) — по «да» владельца 3.09.2026 ~20:50 WITA; ветка прежняя."""
import base64, json, time
from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
KEY = "/Users/iwasborninbali/.config/nusadua-studio-agent/sa-key.json"; ME = "studio@nusadua.dev"
BODY = """Dear Achim,

one structural observation from your database, in case it is of interest: the direction spectrum of the
2n-point solutions (the mean number of point pairs of each primitive direction, for all n = 19..57) has a shape
that follows from the single rule "at most two points on every line": distributing 2n points over the lines of
one direction with that cap, with weight C(L,2) for a line of L cells, reproduces the ratios between fifteen
directions within 12% and their order, with no fitted parameter; the overall scale is not derived.  Seven of the
values were predicted before being measured.  Note and data: https://doi.org/10.5281/zenodo.22275037

One small question, only if the answer is short: on your density page the files n52_free_diag_2352.png and
n52_set_diag_2710.png return 403 -- if they are meant to be public, I would be glad to see them, since a
diagonal-occupation map may be the closest existing measurement.  Otherwise no reply needed.

Best,
Aleksei Kudriashov (Alex Komang)
Nusa Dua, Bali
"""
creds = service_account.Credentials.from_service_account_file(KEY, scopes=["https://mail.google.com/"]).with_subject(ME)
svc = build("gmail", "v1", credentials=creds)
msg = EmailMessage(); msg["To"] = "Achim Flammenkamp <achim@uni-bielefeld.de>"; msg["From"] = f"Aleksei Kudriashov <{ME}>"
msg["Subject"] = "One structural observation from your database (direction spectrum of the solutions)"
msg.set_content(BODY)
r = svc.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()
print("отправлено:", r.get("id"), time.strftime("%Y-%m-%d %H:%M:%S %z"))
json.dump({"to": "achim@uni-bielefeld.de", "id": r.get("id"), "sent": time.strftime("%Y-%m-%d %H:%M:%S %z"), "subject": msg["Subject"]},
          open("/Users/iwasborninbali/saturation/docs/correspondence/achim_letter_2026-09-03.json", "w"), indent=1)
