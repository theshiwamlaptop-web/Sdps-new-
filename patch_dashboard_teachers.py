import re
with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

t = """    val currentUser by viewModel.currentUser.collectAsState()
    val students by viewModel.studentsState.collectAsState()"""
r = """    val currentUser by viewModel.currentUser.collectAsState()
    val teachersList by viewModel.teachersState.collectAsState()
    val students by viewModel.studentsState.collectAsState()"""
content = content.replace(t, r)

t2 = "val teacherRecord = viewModel.teachersState.value.find { it.teacherId == currentUser?.userId }"
r2 = "val teacherRecord = teachersList.find { it.teacherId == currentUser?.userId }"
content = content.replace(t2, r2)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
