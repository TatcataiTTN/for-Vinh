# -*- coding: utf-8 -*-
import sqlite3, json, os, shutil, decimal, datetime, sys

BASE = "/Users/tuannghiat/Downloads/for-Vinh-Exercises"
sys.path.insert(0, os.path.join(BASE, "build"))
from questions_source import QUESTIONS

DATA_DIR = os.path.join(BASE, "data")
TMP_DIR = "/tmp/sql_judge_build"
os.makedirs(TMP_DIR, exist_ok=True)

def clean(v):
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    return v

def run_select(dbpath, sql):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = [[clean(v) for v in row] for row in cur.fetchall()]
    conn.close()
    return {"columns": cols, "rows": rows}

def run_dml_then_verify(dbpath, dml_sql, verify_sql):
    tmp = os.path.join(TMP_DIR, "tmp_" + os.path.basename(dbpath))
    shutil.copyfile(dbpath, tmp)
    conn = sqlite3.connect(tmp)
    cur = conn.cursor()
    cur.executescript(dml_sql)
    conn.commit()
    cur.execute(verify_sql)
    cols = [d[0] for d in cur.description]
    rows = [[clean(v) for v in row] for row in cur.fetchall()]
    conn.close()
    os.remove(tmp)
    return {"columns": cols, "rows": rows}

out_questions = []
by_db_count = {}

for q in QUESTIONS:
    dbpath = os.path.join(DATA_DIR, f"{q['db']}.sqlite")
    if not os.path.exists(dbpath):
        print("MISSING DB:", dbpath); sys.exit(1)

    item = {
        "id": q["id"],
        "db": q["db"],
        "difficulty": q["difficulty"],
        "type": q["type"],
        "topic": q["topic"],
        "title": q["title"],
        "prompt": q["prompt"],
        "hint": q["hint"],
        "solutionSql": q["referenceSql"],
    }

    if q["type"] == "select":
        try:
            item["expected"] = run_select(dbpath, q["referenceSql"])
        except Exception as e:
            print("ERROR (select) in", q["id"], ":", e); sys.exit(1)
    elif q["type"] == "dml":
        item["verifySql"] = q["verifySql"]
        try:
            item["expected"] = run_dml_then_verify(dbpath, q["referenceSql"], q["verifySql"])
        except Exception as e:
            print("ERROR (dml) in", q["id"], ":", e); sys.exit(1)
    else:
        print("UNKNOWN TYPE", q["id"]); sys.exit(1)

    out_questions.append(item)
    by_db_count[q["db"]] = by_db_count.get(q["db"], 0) + 1

out_path = os.path.join(DATA_DIR, "questions.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out_questions, f, ensure_ascii=False, indent=2)

print("TOTAL QUESTIONS:", len(out_questions))
print("BY DB:", by_db_count)
print("WROTE:", out_path)
