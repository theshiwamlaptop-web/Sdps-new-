import re
with open("app/src/main/java/com/example/ui/screens/PremiumLoginScreen.kt", "r") as f:
    text = f.read()

print(re.search(r"import androidx.compose.foundation.interaction", text))
