last = 0
for line in open("profile_trace.txt"):
    try:
        balance = int(line.split('[')[1].split(']')[0])
    except: continue
    
    if balance > last + 2:
        print("Jump up:", line)
    last = balance
