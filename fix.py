with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "if (selectedEntryForReceipt != null) {" in line:
        print(f"Line {i}: {line}")
