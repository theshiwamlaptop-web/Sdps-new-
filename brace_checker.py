import sys

def check_braces(filename, start_line, end_line):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    count = 0
    for i in range(start_line - 1, end_line):
        line = lines[i]
        for char in line:
            if char == '{': count += 1
            elif char == '}': count -= 1
    print(f"Brace count from {start_line} to {end_line}: {count}")

check_braces("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 7123, 8158)
