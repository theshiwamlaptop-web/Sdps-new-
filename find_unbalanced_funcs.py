with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

count = 0
current_func = None
for i, line in enumerate(lines):
    if line.startswith("fun ") or (line.startswith("@Composable") and i+1 < len(lines) and lines[i+1].startswith("fun ")):
        if current_func is not None and count != 0:
            print(f"Function {current_func} ended with count {count}")
        if line.startswith("fun "):
            current_func = line.strip()
        else:
            current_func = lines[i+1].strip()
        count = 0
        
    for char in line:
        if char == '{': count += 1
        elif char == '}': count -= 1

if current_func is not None and count != 0:
    print(f"Function {current_func} ended with count {count}")
