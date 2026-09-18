import re
import os

filepath = 'app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update StudentIdentityBadge signature
badge_old_sig = "fun StudentIdentityBadge(student: Student, modifier: Modifier = Modifier) {"
badge_new_sig = "fun StudentIdentityBadge(student: Student, modifier: Modifier = Modifier, showUserId: Boolean = false) {"
content = content.replace(badge_old_sig, badge_new_sig)

# Hide Sch ID
badge_id = 'CardDetailItem("Sch ID", student.studentId)'
badge_id_new = 'if (showUserId) CardDetailItem("Sch ID", student.studentId)'
content = content.replace(badge_id, badge_id_new)

# 2. Update StudentFullDetailsPanel signature
panel_old_sig = "fun StudentFullDetailsPanel(student: Student) {"
panel_new_sig = "fun StudentFullDetailsPanel(student: Student, showUserId: Boolean = false) {"
content = content.replace(panel_old_sig, panel_new_sig)

# Hide Sch ID in Panel (need to check if it's there)
# Let's write the file back and then find where it is.
with open(filepath, 'w') as f:
    f.write(content)
