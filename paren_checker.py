import sys

def check_parens(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    count_paren = 0
    for i, line in enumerate(lines):
        for char in line:
            if char == '(': count_paren += 1
            elif char == ')': count_paren -= 1
        if count_paren < 0:
            print(f"Error: Negative paren count at line {i+1}")
            count_paren = 0
    print(f"Final paren count: {count_paren}")

check_parens("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt")
