import re
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

text = re.sub(r'        \)\n    \}\n// ==========================================\n// ADMIN STAFF CONTROL PANEL', r'        )\n    }\n    }\n}\n// ==========================================\n// ADMIN STAFF CONTROL PANEL', text)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
