import sys

def check_braces(filename, start, end):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    count_brace = 0
    count_paren = 0
    for i in range(start-1, end):
        line = lines[i]
        for char in line:
            if char == '{': count_brace += 1
            elif char == '}': count_brace -= 1
            elif char == '(': count_paren += 1
            elif char == ')': count_paren -= 1
    print(f"Braces: {count_brace}, Parens: {count_paren}")

check_braces("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 8059, 8156)
