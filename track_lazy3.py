with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

balance = 0
for i in range(164, 873):
    line = lines[i]
    clean = line.strip()
    if clean.startswith('//'): continue
    
    for char in clean:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
        
    if balance <= 0 and i > 165:
        print(f"Block drops to {balance} at line {i+1}: {line.strip()[:60]}")
