with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

b = 0
for i, line in enumerate(lines):
    for c in line:
        if c == '{': b += 1
        elif c == '}': b -= 1
    if b == 0 and '}' in line:
        print(f"Top level block closed at line {i+1}")
    elif b < 0:
        print(f"Negative balance {b} at line {i+1}: {line.strip()}")
