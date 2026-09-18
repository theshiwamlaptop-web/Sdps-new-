with open('payment_dialog.txt', 'r') as f:
    lines = f.readlines()

count = 0
for line in lines:
    if line.strip().startswith('//'): continue
    for char in line:
        if char == '{': count += 1
        elif char == '}': count -= 1
    
print(f"Original text uncommented brace count: {count}")
