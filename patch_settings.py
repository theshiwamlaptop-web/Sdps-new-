import re
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

t = """                        Text(
                            text = when (selectedUser.role.uppercase()) {
                                "PRINCIPAL" -> "👑 PRINCIPAL"
                                "ADMIN" -> "💼 ADMINISTRATOR"
                                "TEACHER", "CLASS_TEACHER" -> "📐 EDUCATOR"
                                else -> "🎓 SCHOLAR"
                            },"""
r = """                        Text(
                            text = when (selectedUser.role.uppercase()) {
                                "PRINCIPAL" -> "👑 PRINCIPAL"
                                "ADMIN" -> "💼 ADMINISTRATOR"
                                "TEACHER", "CLASS_TEACHER" -> {
                                    if (resolvedClassTeacher.isNotEmpty()) "📐 CLASS TEACHER OF ${resolvedClassTeacher.uppercase()}"
                                    else "📐 SUBJECT TEACHER"
                                }
                                else -> "🎓 SCHOLAR"
                            },"""

content = content.replace(t, r)
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
