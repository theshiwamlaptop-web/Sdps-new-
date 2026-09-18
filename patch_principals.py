import re
import os

def replace_in_file(filename, old_str, new_str):
    if not os.path.exists(filename): return
    with open(filename, 'r') as f:
        content = f.read()
    content = content.replace(old_str, new_str)
    with open(filename, 'w') as f:
        f.write(content)

replace_in_file('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 
    'if (user.role.uppercase() == "PRINCIPAL") {', 
    'if (user.role.uppercase() == "PRINCIPAL" || user.role.uppercase() == "HEAD_ADMIN") {')

replace_in_file('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 
    'if (currentUser?.role == "PRINCIPAL") {', 
    'if (currentUser?.role == "PRINCIPAL" || currentUser?.role == "HEAD_ADMIN") {')

replace_in_file('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 
    'if (userRole == "PRINCIPAL") {', 
    'if (userRole == "PRINCIPAL" || userRole == "HEAD_ADMIN") {')

replace_in_file('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 
    'notif.userId == "PRINCIPAL"', 
    '(notif.userId == "PRINCIPAL" || notif.userId == "HEAD_ADMIN")')

replace_in_file('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 
    'val isAdminOrPrincipal = currentUserRole == "ADMIN" || currentUserRole == "PRINCIPAL"', 
    'val isAdminOrPrincipal = currentUserRole == "ADMIN" || currentUserRole == "PRINCIPAL" || currentUserRole == "HEAD_ADMIN"')

