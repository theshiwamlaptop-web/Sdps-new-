import sys

def check_parens(filename):
    with open(filename, 'r') as f:
        text = f.read()
    
    count_paren = 0
    count_brace = 0
    in_string = False
    in_comment = False
    in_block_comment = False
    
    i = 0
    while i < len(text):
        char = text[i]
        
        if in_string:
            if char == '\\':
                i += 2
                continue
            elif char == '"':
                in_string = False
        elif in_comment:
            if char == '\n':
                in_comment = False
        elif in_block_comment:
            if char == '*' and i + 1 < len(text) and text[i+1] == '/':
                in_block_comment = True # wait, it should be False
                in_block_comment = False
                i += 1
        else:
            if char == '"':
                # check for triple quotes
                if i + 2 < len(text) and text[i+1] == '"' and text[i+2] == '"':
                    in_string = True
                    # skip triple quotes? no wait this is just a quick script.
                else:
                    in_string = True
            elif char == '/' and i + 1 < len(text) and text[i+1] == '/':
                in_comment = True
                i += 1
            elif char == '/' and i + 1 < len(text) and text[i+1] == '*':
                in_block_comment = True
                i += 1
            elif char == '(': count_paren += 1
            elif char == ')': count_paren -= 1
            elif char == '{': count_brace += 1
            elif char == '}': count_brace -= 1
            
        i += 1

    print(f"Final paren count: {count_paren}, Final brace count: {count_brace}")

check_parens("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt")
