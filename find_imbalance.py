with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

balance = 0
in_string = False
in_char = False
escape = False
in_line_comment = False
in_block_comment = False

i = 0
line_no = 1
while i < len(text):
    char = text[i]
    if char == '\n':
        line_no += 1
        
    if in_line_comment:
        if char == '\n':
            in_line_comment = False
        i += 1
        continue
        
    if in_block_comment:
        if char == '*' and i + 1 < len(text) and text[i+1] == '/':
            in_block_comment = False
            i += 2
        else:
            i += 1
        continue
        
    if in_string:
        if escape:
            escape = False
        elif char == '\\':
            escape = True
        elif char == '"':
            in_string = False
        i += 1
        continue
        
    if in_char:
        if escape:
            escape = False
        elif char == '\\':
            escape = True
        elif char == "'":
            in_char = False
        i += 1
        continue
        
    if char == '/' and i + 1 < len(text):
        if text[i+1] == '/':
            in_line_comment = True
            i += 2
            continue
        elif text[i+1] == '*':
            in_block_comment = True
            i += 2
            continue
            
    if char == '"':
        in_string = True
        i += 1
        continue
        
    if char == "'":
        in_char = True
        i += 1
        continue
        
    if char == '{':
        balance += 1
    elif char == '}':
        balance -= 1
        if balance < 0:
            print(f"Balance dropped to {balance} at line {line_no}")
            
    i += 1
