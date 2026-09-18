with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

count = 0
in_teacher = False
for i, line in enumerate(lines):
    if "fun TeacherManagementScreen" in line:
        in_teacher = True
        count = 0
    if in_teacher:
        for char in line:
            if char == '{': count += 1
            elif char == '}': count -= 1
        
        if "fun AttendanceManagementScreen" in line:
            break
        
        # We know count ends at 2. 
        # Where does it drop below expected?
print(f"Teacher end count: {count}")
