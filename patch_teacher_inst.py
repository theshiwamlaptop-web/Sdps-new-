import re
with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

t = """                                    val newTeacher = Teacher(
                                        teacherId = finalId,
                                        name = tName,
                                        subject = primarySubject,
                                        classesAssigned = extraChecked,
                                        phone = tPhone,"""
r = """                                    if (tGender.isBlank() || tGender == "Select Gender") {
                                        Toast.makeText(context, "Error: Please select a gender", Toast.LENGTH_SHORT).show()
                                        return@Button
                                    }
                                    val newTeacher = Teacher(
                                        teacherId = finalId,
                                        name = tName,
                                        subject = primarySubject,
                                        gender = tGender,
                                        classesAssigned = extraChecked,
                                        phone = tPhone,"""
content = content.replace(t, r)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
