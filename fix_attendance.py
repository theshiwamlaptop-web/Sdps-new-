import re

with open("app/src/main/java/com/example/ui/screens/AttendanceScreens.kt", "r") as f:
    content = f.read()

content = content.replace("it.rollNumber.contains(", "it.rollNo.contains(")
content = content.replace("it.rollNumber.toIntOrNull()", "it.rollNo.toIntOrNull()")
content = content.replace("Text(\"Roll: ${student.rollNumber}\"", "Text(\"Roll: ${student.rollNo}\"")

content = content.replace("model = student.profilePhotoUrl.ifBlank { \"https://ui-avatars.com/api/?name=${student.name}&background=random\" },", "model = \"https://ui-avatars.com/api/?name=${student.name}&background=random\",")
content = content.replace("import coil.compose.AsyncImage", "import coil.compose.AsyncImage\nimport androidx.compose.ui.layout.ContentScale")

with open("app/src/main/java/com/example/ui/screens/AttendanceScreens.kt", "w") as f:
    f.write(content)

