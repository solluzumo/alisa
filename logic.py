import dbAPI as db
print(db.fetchall("lesson", "432-3;22.05.2023",["audience","teacher","start","end"]))