with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

out = []
balance = 0
for line in lines:
    clean = line.strip()
    if not clean: 
        out.append("")
        continue
    if clean.startswith('//'):
        out.append("    " * balance + clean)
        continue
    
    # count closing braces at the start of the line to unindent early
    close_count_start = 0
    for char in clean:
        if char == '}': close_count_start += 1
        elif char == '{': break # Stop at first {
    
    # Actually a better heuristic is just:
    start_closing = clean.startswith('}')
    if start_closing:
        balance -= 1
        
    out.append("    " * balance + clean)
    
    # Now calculate effect of this line on next lines
    for char in clean:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
        
    if start_closing:
        balance += 1 # undo the early decrement for the loop
        
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt.formatted", "w") as f:
    f.write("\n".join(out))
