import sys

def check():
    with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    start_line = 2041 - 1
    end_line = 3130 - 1
    
    count = 0
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    
    # skip to start_line
    # we just want to count braces in the snippet to see if it drops below 1
    
    snippet = "".join(lines[start_line:end_line])
    
    i = 0
    while i < len(snippet):
        c = snippet[i]
        
        if in_line_comment:
            if c == '\n':
                in_line_comment = False
            i += 1
            continue
        if in_block_comment:
            if c == '*' and i+1 < len(snippet) and snippet[i+1] == '/':
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
            
        if c == '/' and i+1 < len(snippet):
            if snippet[i+1] == '/':
                in_line_comment = True
                i += 2
                continue
            if snippet[i+1] == '*':
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
            
        if count == 0 and c == '}':
            # find what line we are on in snippet
            sub = snippet[:i+1]
            line_in_snippet = sub.count('\n')
            print(f"Brace level reached 0 at line {start_line + line_in_snippet + 1}")
            # wait, count was 1 after the opening brace at start_line.
            
        i += 1
        
    print(f"Final count in snippet: {count}")

check()
