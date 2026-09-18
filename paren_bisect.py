import sys

def check_parens(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    count_paren = 0
    count_brace = 0
    in_block_comment = False
    
    for line_num, line in enumerate(lines, 1):
        i = 0
        in_string = False
        while i < len(line):
            char = line[i]
            if in_block_comment:
                if char == '*' and i + 1 < len(line) and line[i+1] == '/':
                    in_block_comment = False
                    i += 1
            elif in_string:
                if char == '\\':
                    i += 1
                elif char == '"':
                    in_string = False
            else:
                if char == '"':
                    in_string = True
                elif char == '/' and i + 1 < len(line) and line[i+1] == '/':
                    break # end of line
                elif char == '/' and i + 1 < len(line) and line[i+1] == '*':
                    in_block_comment = True
                    i += 1
                elif char == '(': count_paren += 1
                elif char == ')': count_paren -= 1
                elif char == '{': count_brace += 1
                elif char == '}': count_brace -= 1
            i += 1
        if line_num % 1000 == 0:
            print(f"Line {line_num}: paren={count_paren} brace={count_brace}")

check_parens("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt")
