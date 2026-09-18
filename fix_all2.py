import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

# I need to find all `// Contact details update`, etc and ensure there are exactly the right number of `}` before them.
# The easiest way is to use regex to replace all `}` and whitespace before the comments with the correct number of `}`.

# 1. Contact details update
text = re.sub(r"\}\s*// Contact details update", "}\n                }\n            }\n            // Contact details update", text, count=1)

# 2. Security key updates
text = re.sub(r"\}\s*// Security key updates", "}\n                    }\n                }\n            }\n            // Security key updates", text, count=1)

# 3. Theme Preferences
text = re.sub(r"\}\s*// Theme Preferences", "}\n                        }\n                    }\n                }\n            }\n            // Theme Preferences", text, count=1)

# 4. Alert Toggles
text = re.sub(r"\}\s*// Alert Toggles", "}\n                        }\n                    }\n                }\n            }\n            // Alert Toggles", text, count=1)

# 5. Principal permanent deletion
text = re.sub(r"\}\s*// Principal permanent deletion", "}\n                            }\n                        )\n                    }\n                }\n            }\n        }\n        // Principal permanent deletion", text, count=1)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
