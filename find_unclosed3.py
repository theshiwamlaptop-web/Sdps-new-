with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines):
    for char in line:
        if char == '{': count += 1
        elif char == '}': count -= 1
    
    if line.startswith('fun ') or line.startswith('@Composable'):
        print(f"Line {i+1} starts function, count={count}")
