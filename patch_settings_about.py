import re

filepath = 'app/src/main/java/com/example/ui/screens/SettingsScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

target = """            Button(
                onClick = { viewModel.logout() },
                modifier = Modifier.fillMaxWidth().testTag("logout_button"),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
            ) {
                Icon(imageVector = Icons.Filled.Logout, contentDescription = "Logout")
                Spacer(modifier = Modifier.width(8.dp))
                Text("Logout Securely")
            }
        }
    }
}"""

replacement = """            Button(
                onClick = { viewModel.logout() },
                modifier = Modifier.fillMaxWidth().testTag("logout_button"),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
            ) {
                Icon(imageVector = Icons.Filled.Logout, contentDescription = "Logout")
                Spacer(modifier = Modifier.width(8.dp))
                Text("Logout Securely")
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // About School Card
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Image(
                        painter = painterResource(id = R.drawable.logo_sdps),
                        contentDescription = "School Logo",
                        contentScale = ContentScale.Fit,
                        modifier = Modifier.size(100.dp).padding(bottom = 8.dp)
                    )
                    Text("S.D. Public School", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                    Text("KNOWLEDGE IS POWER", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("App Version 1.0.0", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}"""

content = content.replace(target, replacement)
with open(filepath, 'w') as f:
    f.write(content)

