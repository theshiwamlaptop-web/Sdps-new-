import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

# Replace amountPaid with paidAmount
content = content.replace("feesList.sumOf { it.amountPaid }", "feesList.sumOf { it.paidAmount }")

# Replace photoUrl with avatarUrl for currentUser
content = content.replace("currentUser?.photoUrl", "currentUser?.avatarUrl")

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
print("Fixed variable names")
