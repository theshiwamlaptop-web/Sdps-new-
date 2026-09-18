with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

count = 0
min_count = 0
for i, line in enumerate(lines):
    for char in line:
        if char == '{': count += 1
        elif char == '}': count -= 1
    if count == 0 and i > 1990:
        print(f"Line {i+1} count reached 0: {line.strip()}")
