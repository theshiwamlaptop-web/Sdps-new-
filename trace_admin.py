import sys

def check():
    with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    count = 1
    for line_num in range(4300, 4600):
        line = lines[line_num]
        
        # very simple brace counter
        for c in line:
            if c == '{': count += 1
            elif c == '}': count -= 1
            
        print(f"L{line_num+1}: {count} {line.strip()[:40]}")
        if count == 0:
            print("REACHED ZERO!")
            break
            
check()
