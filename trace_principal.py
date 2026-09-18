with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

balance = 0
for i in range(928, 977):
    line = lines[i]
    for char in line:
        if char == '{':
            balance += 1
        elif char == '}':
            balance -= 1
    print(f"Line {i+1}: Balance={balance} - {line.strip()[:30]}")
