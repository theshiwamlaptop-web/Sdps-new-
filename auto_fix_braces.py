import sys

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove extra braces before AttendanceManagementScreen
content = content.replace("}\n\n\n}\n}\n@Composable\nfun AttendanceManagementScreen", "@Composable\nfun AttendanceManagementScreen")
content = content.replace("}\n}\n}\n}\n@Composable\nfun AttendanceManagementScreen", "@Composable\nfun AttendanceManagementScreen")
content = content.replace("}\n}\n@Composable\nfun AttendanceManagementScreen", "@Composable\nfun AttendanceManagementScreen")

# 2. Remove extra braces before AcademicClassesScreen
content = content.replace("}\n}\n@Composable\nfun AcademicClassesScreen", "@Composable\nfun AcademicClassesScreen")

# 3. I added 2 extra braces in AttendanceManagementScreen before '} else {' around 4304. Let's revert it.
old_bad = "                    }\n                }\n            }\n        } else {\n            // Admin or Teacher Register Mode"
new_good = "                    }\n        } else {\n            // Admin or Teacher Register Mode"
content = content.replace(old_bad, new_good)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 'w', encoding='utf-8') as f:
    f.write(content)

