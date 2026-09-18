with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

balance = 0
for i in range(735, 880):
    line = lines[i]
    clean = line.strip()
    if clean.startswith('//'): continue
    for char in clean:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
    print(f"{i+1} [{balance}]: {clean[:60]}")
