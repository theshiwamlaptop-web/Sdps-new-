with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

b = 0
for i in range(979, 1144):
    clean = lines[i].strip()
    if clean.startswith('//'): continue
    for c in clean:
        if c == '{': b += 1
        elif c == '}': b -= 1

print(f"Balance inside 0 -> : {b}")
