def find_unclosed(start, end):
    with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
        lines = f.readlines()
    stack = []
    for i in range(start, end):
        clean = lines[i].strip()
        if clean.startswith('//'): continue
        for char in clean:
            if char == '{': stack.append(i+1)
            elif char == '}': 
                if stack: stack.pop()
    print(f"Unclosed in {start}-{end}: {stack}")

find_unclosed(1975, 2115)
