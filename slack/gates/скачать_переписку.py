#!/usr/bin/env python3
"""Скачивает ПОЛНУЮ переписку с Ахимом Фламменкампом в локальный файл и выдаёт расписку.

ЗАЧЕМ. Дважды за два дня письмо готовилось на неполном знании: один раз я собирался
задать вопрос, на который он уже ответил, другой — сообщить как новость его собственное
число, о котором мы сами ему писали накануне. Контекст модели теряет детали при долгой
работе; переписка — нет. Значит перед всяким письмом её надо ПРОЧЕСТЬ ЦЕЛИКОМ, а не
вспомнить.

Расписка (READ_RECEIPT) содержит хеш содержимого переписки и время. Гейт на отправку
писем требует, чтобы расписка была свежей И соответствовала текущему содержимому:
если пришло новое письмо, расписка становится недействительной автоматически.
"""
import base64, hashlib, json, pathlib, subprocess, sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

КЛЮЧ = "/Users/iwasborninbali/.config/nusadua-studio-agent/sa-key.json"
КТО = "studio@nusadua.dev"
КУДА = pathlib.Path("/Users/iwasborninbali/saturation/docs/correspondence")
ФАЙЛ = КУДА / "achim_full.md"
РАСПИСКА = КУДА / "READ_RECEIPT.json"
ЗАПРОС = "from:achim@uni-bielefeld.de OR to:achim@uni-bielefeld.de"


def тело(p):
    if p.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8", "replace")
    for c in p.get("parts", []):
        if c.get("mimeType") == "text/plain":
            t = тело(c)
            if t:
                return t
    for c in p.get("parts", []):
        t = тело(c)
        if t:
            return t
    return ""


def main():
    creds = service_account.Credentials.from_service_account_file(
        КЛЮЧ, scopes=["https://mail.google.com/"]).with_subject(КТО)
    svc = build("gmail", "v1", credentials=creds)
    найдено = svc.users().messages().list(userId="me", q=ЗАПРОС, maxResults=200).execute()
    ветки = []
    for m in найдено.get("messages", []):
        if m["threadId"] not in ветки:
            ветки.append(m["threadId"])
    куски = ["# ПОЛНАЯ переписка с Ахимом Фламменкампом\n",
             "Скачано автоматически. НЕ РЕДАКТИРОВАТЬ РУКАМИ: файл перезаписывается.\n"]
    всего = 0
    for tid in ветки:
        th = svc.users().threads().get(userId="me", id=tid, format="full").execute()
        сообщения = sorted(th["messages"], key=lambda m: int(m["internalDate"]))
        куски.append(f"\n\n## ветка {tid} — сообщений {len(сообщения)}\n")
        for m in сообщения:
            h = {x["name"]: x["value"] for x in m["payload"]["headers"]}
            куски.append(f"\n### {h.get('Date','?')} | от: {h.get('From','?')} | кому: {h.get('To','?')}\n")
            куски.append(f"**Тема:** {h.get('Subject','?')}  \n")
            куски.append(f"**Message-ID:** `{h.get('Message-ID','')}`\n\n```\n")
            куски.append(тело(m["payload"]).strip())
            куски.append("\n```\n")
            всего += 1
    текст = "".join(куски)
    КУДА.mkdir(parents=True, exist_ok=True)
    ФАЙЛ.write_text(текст, encoding="utf-8")
    ц = hashlib.sha256(текст.encode("utf-8")).hexdigest()
    ts = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S %Z"], capture_output=True,
                        text=True, env={"TZ": "Asia/Makassar", "PATH": "/bin:/usr/bin"}).stdout.strip()
    РАСПИСКА.write_text(json.dumps({
        "sha256": ц, "сообщений": всего, "веток": len(ветки), "когда": ts,
        "файл": str(ФАЙЛ)}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"переписка скачана: {всего} сообщений в {len(ветки)} ветках -> {ФАЙЛ}")
    print(f"расписка: {ц[:16]}... от {ts}")
    print(f"\nПРОЧТИ ФАЙЛ ЦЕЛИКОМ ПЕРЕД ПИСЬМОМ. Гейт проверит только свежесть расписки,")
    print(f"прочтение он проверить не может — это на твоей совести.")


if __name__ == "__main__":
    main()
