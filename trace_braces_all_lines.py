import sys

def check():
    with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    count = 0
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    
    with open("braces_depth_all.txt", "w") as out:
        for line_num, line in enumerate(lines):
            i = 0
            while i < len(line):
                c = line[i]
                
                if in_line_comment:
                    if c == '\n':
                        in_line_comment = False
                    i += 1
                    continue
                if in_block_comment:
                    if c == '*' and i+1 < len(line) and line[i+1] == '/':
                        in_block_comment = False
                        i += 2
                        continue
                    i += 1
                    continue
                if in_string:
                    if c == '\\':
                        i += 2
                        continue
                    if c == '"':
                        in_string = False
                    i += 1
                    continue
                if in_char:
                    if c == '\\':
                        i += 2
                        continue
                    if c == "'":
                        in_char = False
                    i += 1
                    continue
                    
                if c == '/' and i+1 < len(line):
                    if line[i+1] == '/':
                        in_line_comment = True
                        i += 2
                        continue
                    if line[i+1] == '*':
                        in_block_comment = True
                        i += 2
                        continue
                        
                if c == '"':
                    in_string = True
                elif c == "'":
                    in_char = True
                elif c == '{':
                    count += 1
                elif c == '}':
                    count -= 1
                    
                i += 1
            if line.strip():
                out.write(f"{line_num+1:4d}: depth={count} {line.strip()[:40]}\n")

check()
