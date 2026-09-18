with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    text = f.read()

print("Occurrences of 'if (isPrincipal) {':", text.count('if (isPrincipal) {'))
print("Occurrences of 'editBasicSalary = activePayroll':", text.count('editBasicSalary = activePayroll'))
