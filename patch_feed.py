import re
with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

t = """                        val icon = when (alert.type) {
                            "APPROVAL_PENDING" -> Icons.Filled.HourglassEmpty
                            "APPROVED" -> Icons.Filled.CheckCircle
                            "REJECTED" -> Icons.Filled.Close
                            else -> Icons.Filled.Info
                        }"""
r = """                        val icon = when (alert.type) {
                            "APPROVAL_PENDING", "DELETE_REQUEST" -> Icons.Filled.HourglassEmpty
                            "APPROVED" -> Icons.Filled.CheckCircle
                            "REJECTED" -> Icons.Filled.Close
                            else -> Icons.Filled.Info
                        }"""
content = content.replace(t, r)

t2 = """                        val tint = when (alert.type) {
                            "APPROVAL_PENDING" -> Color(0xFFD97706)
                            "APPROVED" -> Color(0xFF10B981)
                            "REJECTED" -> Color(0xFFEF4444)
                            else -> MaterialTheme.colorScheme.primary
                        }"""
r2 = """                        val tint = when (alert.type) {
                            "APPROVAL_PENDING", "DELETE_REQUEST" -> Color(0xFFD97706)
                            "APPROVED" -> Color(0xFF10B981)
                            "REJECTED" -> Color(0xFFEF4444)
                            else -> MaterialTheme.colorScheme.primary
                        }"""
content = content.replace(t2, r2)

t3 = """                            Text(
                                text = alert.message,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }"""
r3 = """                            Text(
                                text = alert.message,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            if (alert.type == "DELETE_REQUEST" && userRole == "PRINCIPAL") {
                                Spacer(modifier = Modifier.height(8.dp))
                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    Button(
                                        onClick = { viewModel.approveDeletion(alert, currentUser?.name ?: "Principal", userId) },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981))
                                    ) { Text("APPROVE") }
                                    Button(
                                        onClick = { viewModel.rejectDeletion(alert, currentUser?.name ?: "Principal", userId) },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFEF4444))
                                    ) { Text("REJECT") }
                                }
                            }
                        }
                    }"""
content = content.replace(t3, r3)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
