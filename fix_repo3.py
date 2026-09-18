with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    text = f.read()

lines = text.split("\n")
out = []
i = 0
while i < len(lines):
    line = lines[i]
    if "scope.launch {" in line and ("db.timetableDao().insertTimetable" in "".join(lines[i:i+15]) or "db.chatDao().insertMessage" in "".join(lines[i:i+15]) or "db.userDao().insertUser(processedUser)" in "".join(lines[i:i+25])):
        if "db.withTransaction" not in line and "db.withTransaction" not in "".join(lines[i:i+3]):
            i += 1
            # find corresponding close brace
            j = i
            brace_count = 1
            while j < len(lines):
                if "{" in lines[j]:
                    brace_count += lines[j].count("{")
                if "}" in lines[j]:
                    brace_count -= lines[j].count("}")
                if brace_count == 0:
                    lines[j] = lines[j].replace("}", "", 1)
                    break
                j += 1
            continue
    out.append(line)
    i += 1

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write("\n".join(out))
