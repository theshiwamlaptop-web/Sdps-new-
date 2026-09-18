import re

filepath = 'app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

target = """        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = { Text("Reset Password") },
            text = {"""

replacement = """        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .background(
                                brush = androidx.compose.ui.graphics.Brush.radialGradient(
                                    colors = listOf(Color(0xFFFFB703).copy(alpha = 0.3f), Color.Transparent),
                                    radius = 120f
                                ),
                                shape = CircleShape
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Image(
                            painter = painterResource(id = R.drawable.logo_sdps),
                            contentDescription = "School Logo",
                            contentScale = ContentScale.Fit,
                            modifier = Modifier.size(64.dp)
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("Reset Password")
                }
            },
            text = {"""

content = content.replace(target, replacement)
with open(filepath, 'w') as f:
    f.write(content)

