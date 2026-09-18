import os

filepath = "app/src/main/java/com/example/ui/screens/PremiumLoginScreen.kt"
with open(filepath, "r") as f:
    content = f.read()

# Fix spacing around fields
content = content.replace("Spacer(modifier = Modifier.height(12.dp))", "Spacer(modifier = Modifier.height(16.dp))")

# Better typography for titles
content = content.replace(
    'style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.ExtraBold, letterSpacing = (-0.5).sp)',
    'style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp)'
)
content = content.replace(
    'style = MaterialTheme.typography.bodyMedium,\n                        color = MaterialTheme.colorScheme.onSurfaceVariant',
    'style = MaterialTheme.typography.bodyLarge,\n                        color = MaterialTheme.colorScheme.onSurfaceVariant'
)

# Fix ExposedDropdownMenuBox warning
content = content.replace('.menuAnchor()', '.menuAnchor(MenuAnchorType.PrimaryNotEditable)')

with open(filepath, "w") as f:
    f.write(content)
print("Success")
