import re
with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

t = """                            text = "OFFICIAL INSTRUCTOR","""
r = """                            text = if (resolvedClassTeacher.isNotEmpty()) "CLASS TEACHER OF ${resolvedClassTeacher.uppercase()}" else "SUBJECT TEACHER","""
content = content.replace(t, r)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
