with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

# Add rememberSaveable import if missing
if "import androidx.compose.runtime.saveable.rememberSaveable" not in content:
    content = "import androidx.compose.runtime.saveable.rememberSaveable\n" + content

# Replace rememberSaveable on displayedMonth with remember
target_dm = "var displayedMonth by rememberSaveable { mutableStateOf(Calendar.getInstance()) }"
repl_dm = "var displayedMonth by remember { mutableStateOf(Calendar.getInstance()) }"

content = content.replace(target_dm, repl_dm)

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
    f.write(content)

print("Imports and displayedMonth updated")
