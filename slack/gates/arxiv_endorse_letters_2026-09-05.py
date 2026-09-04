#!/usr/bin/env python3
"""Вторая волна писем-просьб об endorsement (arXiv math.CO), 5.09.2026, с studio@nusadua.dev через Gmail API.
Первая волна 3.09 (Wood, Pór) — без ответа за двое суток; слово владельца 5.09: «отправим ещё 4 как планировали».
Текст тела — тот же, что 3.09 (одобрен владельцем); абзац {why} — свой для каждого адресата, без ссылок,
которых в наших заметках нет. Адреса сверены 5.09 по страницам университетов."""
import base64, sys, json, time
from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
KEY = "/Users/iwasborninbali/.config/nusadua-studio-agent/sa-key.json"; ME = "studio@nusadua.dev"
CODE = "NJC4KO"
SIG = "Aleksei Kudriashov (Alex Komang)\nIndependent researcher, Nusa Dua, Bali, Indonesia\nstudio@nusadua.dev — https://github.com/iwasborninbali"
BODY = """Dear Professor {name},

I am an independent researcher working on the no-three-in-line problem and its three-dimensional variants
(OEIS A399138 — no three collinear points in the n x n x n grid, and A280537 — no four coplanar). I would
like to post two short notes to arXiv (math.CO) and need an endorsement for that archive. The endorsement
code is {code}; the form is at https://arxiv.org/auth/endorse (enter the code there).

{why}

The notes are already public with DOIs, and every configuration in them can be checked with a small script:
  - A280537 (no four coplanar), note v3.2: https://doi.org/10.5281/zenodo.22066410 — new lower bounds for
    n = 12, 21, 22, 27 beyond the monotone closure of the previously known values, and three pairwise
    inequivalent optimal configurations at n = 7 and at n = 8 found by exact optimisation inside symmetry
    classes of the cube group;
  - A399138 (no three collinear): https://doi.org/10.5281/zenodo.22019279 — certified exact values for
    n <= 6, and new lower bounds a(8) >= 94, a(9) >= 116, a(10) >= 138, a(11) >= 164 obtained the same way
    (witnesses and verifier in https://github.com/iwasborninbali/saturation, directory certs/no3_3d).

In the interest of full disclosure: as the notes state, the computations and a large part of the
mathematics were carried out by AI systems under my direction; every stated value is independently
verified by simple programs that are published with the notes. I have no formal affiliation.

I understand that an endorsement is a statement about the author rather than a review of the papers, and
that you may prefer not to endorse someone you do not know; in that case no reply is needed.

With best regards,
""" + SIG
GARDNER = ("Your paper with {others} on Martin Gardner's minimum no-3-in-a-line problem (American Mathematical\n"
           "Monthly, 2014) is the closest published work in the planar setting to the questions these notes ask in the\n"
           "cube, and you publish in math.CO; that is why I am writing to you.")
LETTERS = [
    ("Thomas Prellberg", "t.prellberg@qmul.ac.uk", "Prellberg",
     "Your two 2026 papers on the no-three-in-line problem — the constraint-programming enumeration (arXiv:2602.07751)\n"
     "and the checkerboard-grid variant with its capacity-two linear-programming bound (arXiv:2605.09215) — are cited\n"
     "in my companion notes on the planar problem; the two notes below are the three-dimensional side of the same work,\n"
     "and you publish in math.CO; that is why I am writing to you."),
    ("Oleg Pikhurko", "O.Pikhurko@warwick.ac.uk", "Pikhurko",
     GARDNER.format(others="Alec Cooper, John Schmitt and Gregory Warrington")),
    ("John R. Schmitt", "jschmitt@middlebury.edu", "Schmitt",
     GARDNER.format(others="Alec Cooper, Oleg Pikhurko and Gregory Warrington")),
    ("Gregory S. Warrington", "gswarrin@uvm.edu", "Warrington",
     GARDNER.format(others="Alec Cooper, Oleg Pikhurko and John Schmitt")),
]
OUT = "/Users/iwasborninbali/saturation/docs/correspondence/arxiv_endorsement_sent_2026-09-05.json"
def main(dry):
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=["https://mail.google.com/"]).with_subject(ME)
    svc = build("gmail", "v1", credentials=creds); out = []
    for full, addr, short, why in LETTERS:
        msg = EmailMessage(); msg["To"] = f"{full} <{addr}>"; msg["From"] = f"Aleksei Kudriashov <{ME}>"
        msg["Subject"] = "arXiv endorsement request (math.CO): no-three-in-line in the cube"
        msg.set_content(BODY.format(name=short, code=CODE, why=why))
        if dry: print("=" * 70); print(msg.as_string()); continue
        r = svc.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()
        out.append({"to": addr, "id": r.get("id"), "threadId": r.get("threadId"), "sent": time.strftime("%Y-%m-%d %H:%M:%S %z")}); print("отправлено:", addr, r.get("id"))
    if not dry: json.dump(out, open(OUT, "w"), indent=1)
if __name__ == "__main__": main(dry="--dry" in sys.argv)
