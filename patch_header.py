import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

target = """                            Text(
                                text = "Enterprise Finance & Revenue Module",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }"""

replacement = """                            Text(
                                text = "Enterprise Finance & Revenue Module",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            if (currentUser?.role != "STUDENT" && currentUser?.role != "TEACHER" && currentUser?.role != "CLASS_TEACHER") {
                                Row(modifier = Modifier.padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    Button(onClick = { Toast.makeText(context, "Exporting Due Students List to Excel...", Toast.LENGTH_SHORT).show() }, modifier = Modifier.height(32.dp), contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp)) { Text("Export Excel", fontSize = 11.sp) }
                                    Button(onClick = { Toast.makeText(context, "Exporting Monthly Revenue Report to PDF...", Toast.LENGTH_SHORT).show() }, modifier = Modifier.height(32.dp), contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp), colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFDC2626))) { Text("Export PDF", fontSize = 11.sp) }
                                }
                            }
                        }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
