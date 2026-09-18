import re
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

text = re.sub(r'\}\s*,\s*modifier = Modifier', r'},\n                            modifier = Modifier', text)

text = re.sub(r'Text\("Save Facility Setup Configuration", fontWeight = FontWeight\.Bold\)\s*\}\s*\}\s*3 -> \{ // COMPREHENSIVE SECURITY AUDITS LOG', r'Text("Save Facility Setup Configuration", fontWeight = FontWeight.Bold)\n                        }\n                    }\n                }\n                3 -> { // COMPREHENSIVE SECURITY AUDITS LOG', text)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
