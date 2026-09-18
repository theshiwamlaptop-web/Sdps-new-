import re
with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

t = """                                    Text(
                                        text = if (teacher.classTeacherOf.isNotEmpty()) "Class Teacher of ${teacher.classTeacherOf}" else "Not Assigned",
                                        style = MaterialTheme.typography.bodySmall.copy(
                                            color = if (teacher.classTeacherOf.isNotEmpty()) Color(0xFF10B981) else Color(0xFF94A3B8), 
                                            fontWeight = FontWeight.Bold
                                        )
                                    )"""
r = """                                    Text(
                                        text = if (teacher.classTeacherOf.isNotEmpty()) "CLASS TEACHER OF ${teacher.classTeacherOf.uppercase()}" else "SUBJECT TEACHER",
                                        style = MaterialTheme.typography.bodySmall.copy(
                                            color = if (teacher.classTeacherOf.isNotEmpty()) Color(0xFF10B981) else Color(0xFF94A3B8), 
                                            fontWeight = FontWeight.Bold
                                        )
                                    )"""
content = content.replace(t, r)
with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
