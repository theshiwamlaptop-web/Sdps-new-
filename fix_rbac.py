import os

files = [
    'app/src/main/java/com/example/ui/screens/StudentManagementScreen.kt',
    'app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt',
    'app/src/main/java/com/example/ui/screens/AttendanceScreens.kt',
    'app/src/main/java/com/example/ui/screens/NoticeHubScreen.kt',
    'app/src/main/java/com/example/ui/screens/SettingsScreen.kt'
]

for file in files:
    if os.path.exists(file):
        with open(file, 'r') as f:
            content = f.read()
        
        # We want to make sure HEAD_ADMIN is treated equivalently to PRINCIPAL everywhere it makes sense
        # specifically where `isPrincipal = roleStr == "PRINCIPAL"`
        content = content.replace('val isPrincipal = roleStr == "PRINCIPAL"\n', 'val isPrincipal = roleStr == "PRINCIPAL" || roleStr == "HEAD_ADMIN"\n')
        content = content.replace('val isPrincipal = currentUserRole == "PRINCIPAL"\n', 'val isPrincipal = currentUserRole == "PRINCIPAL" || currentUserRole == "HEAD_ADMIN"\n')
        content = content.replace('val isPrincipal = currentUser?.role == "PRINCIPAL"\n', 'val isPrincipal = currentUser?.role == "PRINCIPAL" || currentUser?.role == "HEAD_ADMIN"\n')
        
        with open(file, 'w') as f:
            f.write(content)
