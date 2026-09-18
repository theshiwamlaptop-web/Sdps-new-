with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

to_delete = 0
for i in range(1, len(lines)):
    if lines[i] in ["                }\n", "                }"]:
        prev = lines[i-1]
        if '}' in prev:
            spaces = len(prev) - len(prev.lstrip(' '))
            if spaces > 16:
                to_delete += 1

print(to_delete)
