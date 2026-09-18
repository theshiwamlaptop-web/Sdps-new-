import re

with open("app/src/main/java/com/example/ui/screens/ChatScreens.kt", "r") as f:
    content = f.read()

# Replace profilePhotoUrl with empty string
content = re.sub(r'it\.profilePhotoUrl\.ifBlank \{ "[^"]+" \}', '""', content)
content = re.sub(r'it\.profilePhotoUrl', '""', content)
content = re.sub(r't\.profilePhotoUrl', '""', content)
content = re.sub(r's\.profilePhotoUrl', '""', content)

# Fix OutlinedTextField colors
content = content.replace("TextFieldDefaults.outlinedTextFieldColors", "OutlinedTextFieldDefaults.colors")

with open("app/src/main/java/com/example/ui/screens/ChatScreens.kt", "w") as f:
    f.write(content)

print("Fixed")
