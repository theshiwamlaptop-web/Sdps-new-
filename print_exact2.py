with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()
for i in range(725, 745):
    print(f"{i+1}: {repr(lines[i])}")
