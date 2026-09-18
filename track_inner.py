with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

def track(start, end):
    balance = 0
    for i in range(start, end):
        clean = lines[i].strip()
        if clean.startswith('//'): continue
        for char in clean:
            if char == '{': balance += 1
            elif char == '}': balance -= 1
    return balance

print("PrincipalERPPanel leak:", track(929, 1512))
print("AdminERPPanel leak:", track(1512, 1644))
print("TeacherERPPanel leak:", track(1644, 1963))
print("StudentERPPanel leak:", track(1963, 2098))
