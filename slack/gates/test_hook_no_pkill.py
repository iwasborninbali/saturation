#!/usr/bin/env python3
"""Ворота обязаны доказать, что умеют И запрещать, И пропускать.
Ворота, которые только запрещают, отключат в тот же день — вместе с защитой."""
import json, subprocess

HOOK = "/Users/iwasborninbali/.claude/hooks/no_pkill_f.py"
K = "pk" + "ill"
DANGER = K + " -f kissat"
REMOTE = 'gcloud compute ssh vm --command="' + K + ' -f sos_named"'
SAFE_X = K + " -x kissat"
SAFE_COUNT = "pgrep -fc plane_sweep"
IN_HEREDOC = "cat > f.sh <<'EOF'\nтекст про " + K + " -f нельзя\nEOF\ngit commit -m x"
IN_COMMENT = "# нельзя " + K + " -f\nls -la"

CASES = [
    (DANGER, 2, "настоящая команда"),
    (REMOTE, 2, "она же через ssh"),
    (SAFE_X, 0, "точное имя процесса"),
    (SAFE_COUNT, 0, "счётный pgrep"),
    (IN_HEREDOC, 0, "образец внутри heredoc"),
    (IN_COMMENT, 0, "образец в комментарии"),
]

ok = True
for cmd, want, label in CASES:
    p = subprocess.run(["python3", HOOK],
                       input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}),
                       capture_output=True, text=True)
    good = p.returncode == want
    ok &= good
    print(f"  {'ВЕРНО ' if good else 'ОШИБКА'}: код {p.returncode} (ждали {want}) — {label}")
print("ИТОГ:", "ворота умеют и запрещать, и пропускать" if ok else "ВОРОТА НЕГОДНЫ")
