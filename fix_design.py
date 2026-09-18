import os

filepath = "app/src/main/java/com/example/ui/screens/PremiumLoginScreen.kt"
with open(filepath, "r") as f:
    content = f.read()

target = """            Surface(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .wrapContentHeight()
                    .padding(vertical = 16.dp),
                shape = RoundedCornerShape(24.dp),
                color = MaterialTheme.colorScheme.surface.copy(alpha = 0.85f), // Translucent glass effect
                shadowElevation = 12.dp
            ) {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {"""

replacement = """            ElevatedCard(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .wrapContentHeight()
                    .padding(vertical = 16.dp),
                shape = RoundedCornerShape(32.dp),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 20.dp),
                colors = CardDefaults.elevatedCardColors(
                    containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.96f)
                )
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 32.dp, vertical = 32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {"""

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, "w") as f:
        f.write(content)
    print("Success")
else:
    print("Target not found")
