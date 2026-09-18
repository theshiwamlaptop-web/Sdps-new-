def trace(start, end):
    with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
        lines = f.readlines()
    balance = 0
    for i in range(start, end):
        clean = lines[i].strip()
        if clean.startswith('//'): continue
        for char in clean:
            if char == '{': balance += 1
            elif char == '}': balance -= 1
        print(f"Line {i+1} [{balance}]: {clean[:40]}")

trace(136, 874)
