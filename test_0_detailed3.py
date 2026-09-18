with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

stack = []
for i in range(978, 1144):
    clean = lines[i].strip()
    if clean.startswith('//'): continue
    for c in clean:
        if c == '{': stack.append(i+1)
        elif c == '}': 
            if stack: stack.pop()
    print(f"Line {i+1}: {clean[:40]} -> Stack size: {len(stack)} | Stack: {stack}")
