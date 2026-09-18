with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

def print_unclosed(start, end):
    stack = []
    for i in range(start, end):
        clean = lines[i].strip()
        if clean.startswith('//'): continue
        for char in clean:
            if char == '{': stack.append(i+1)
            elif char == '}': 
                if stack: stack.pop()
    print(f"Unclosed {start}-{end}: {stack}")

print_unclosed(1230, 1370)
