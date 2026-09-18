import os

filepath = "app/src/main/java/com/example/ui/screens/PremiumLoginScreen.kt"
with open(filepath, "r") as f:
    content = f.read()

target = """                    Text(
                        text = "Sign in to SDPS",
                        style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Spacer(modifier = Modifier.height(16.dp))"""

replacement = """                    Text(
                        text = "Welcome to SDPS",
                        style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.ExtraBold, letterSpacing = (-0.5).sp),
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = "Sign in to continue",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(24.dp))"""

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, "w") as f:
        f.write(content)
    print("Success")
else:
    print("Target not found")
