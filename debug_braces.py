with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

balance = 0
for i, line in enumerate(lines):
    clean = line.strip()
    if clean.startswith('//'): continue
    
    for char in clean:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
        
    if balance == 0:
        print(f"Line {i+1} hits balance 0.")
