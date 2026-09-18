import re

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

old_call = "viewModel.addOrUpdateStudent(newStudent)"
new_call = "viewModel.addOrUpdateStudent(newStudent, isEdit = false)"

content = content.replace(old_call, new_call)

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
    f.write(content)
