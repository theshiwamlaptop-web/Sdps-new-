with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

# Remove any import before package declaration
if content.startswith("import androidx.compose.runtime.saveable.rememberSaveable\n"):
    content = content[len("import androidx.compose.runtime.saveable.rememberSaveable\n"):]

# Ensure package com.example.ui.screens is at the top
package_line = "package com.example.ui.screens\n"
if "package com.example.ui.screens" in content:
    # Insert import right after package declaration
    target = package_line
    repl = package_line + "import androidx.compose.runtime.saveable.rememberSaveable\n"
    if "import androidx.compose.runtime.saveable.rememberSaveable" not in content:
        content = content.replace(target, repl, 1)

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
    f.write(content)

print("Package header fixed")
