import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

def replace_braces(comment, count):
    global text
    # Match one or more `}` optionally separated by whitespace, followed by the comment
    pattern = r"(\}\s*)+(" + re.escape(comment) + r")"
    replacement = "}\n" * count + r"        \2"
    text = re.sub(pattern, replacement, text, count=1)

replace_braces("// Contact details update (Only for own profile)", 3)
replace_braces("// Security key updates (Only for own profile)", 4)
replace_braces("// Theme Preferences (Only for own profile)", 3)
replace_braces("// Alert Toggles (Only for own profile)", 3)
replace_braces("// Principal permanent deletion capability (Visible ONLY to the Principal)", 4)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
