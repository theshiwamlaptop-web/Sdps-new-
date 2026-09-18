with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

stack = []
for i in range(979, 1144):
    clean = lines[i].strip()
    if clean.startswith('//'): continue
    for c in clean:
        if c == '{': stack.append(i+1)
        elif c == '}': 
            if stack: stack.pop()

print(f"Unclosed in 0 -> : {stack}")
