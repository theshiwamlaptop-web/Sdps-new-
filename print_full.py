with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines[:3140]):
    for char in line:
        if char == '{': count += 1
        elif char == '}': count -= 1
    
    if i >= 3120:
        print(f"Line {i+1}: count {count} - {line.strip()}")
