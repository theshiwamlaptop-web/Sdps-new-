import re

with open("app/src/main/java/com/example/ui/navigation/NavHost.kt", "r") as f:
    content = f.read()

content = content.replace("LoginScreen(viewModel = viewModel)", "PremiumLoginScreen(viewModel = viewModel)")
content = content.replace("import com.example.ui.screens.LoginScreen", "import com.example.ui.screens.PremiumLoginScreen")

with open("app/src/main/java/com/example/ui/navigation/NavHost.kt", "w") as f:
    f.write(content)
