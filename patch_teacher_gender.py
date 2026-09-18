import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

# Add tGender
t1 = "        var tPhotoUrl by remember { mutableStateOf(\"\") }"
r1 = "        var tGender by remember { mutableStateOf(\"\") }\n        var isTGenderExpanded by remember { mutableStateOf(false) }\n        var tPhotoUrl by remember { mutableStateOf(\"\") }"
content = content.replace(t1, r1)

# Ensure Capitalization for tName
t2 = "onValueChange = { tName = it },"
r2 = "onValueChange = { tName = it.uppercase() },"
content = content.replace(t2, r2)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
