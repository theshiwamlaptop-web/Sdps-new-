import re

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

old_button = """                                Spacer(modifier = Modifier.height(4.dp))

                                Button(
                                    onClick = {"""

new_button = """                                Spacer(modifier = Modifier.height(4.dp))
                                if (isPrincipal) {
                                Button(
                                    onClick = {"""

content = content.replace(old_button, new_button)

old_button_end = """                                    Icon(Icons.Filled.EditNote, null, modifier = Modifier.size(16.dp))
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Text("Manage Salary Ledger", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                }"""

new_button_end = """                                    Icon(Icons.Filled.EditNote, null, modifier = Modifier.size(16.dp))
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Text("Manage Salary Ledger", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                }
                                }"""

content = content.replace(old_button_end, new_button_end)

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
    f.write(content)
