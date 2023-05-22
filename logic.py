import dbAPI as db
response = db.fetchall("lesson", "432-3;22.05.2023",["audience","teacher","start","end"])
request=""
for s in response:
    for i in s:
        request+=f"{i} "
print(request)