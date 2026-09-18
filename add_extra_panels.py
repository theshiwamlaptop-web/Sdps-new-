import re

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

extra_panels = """@Composable
fun StudentHomeworkPanel(student: Student, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Recent Homework & Assignments",
                style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold),
                color = MaterialTheme.colorScheme.primary
            )
            Divider()
            Text("Navigate to Academics > Homework module to view all assignments for ${student.className}.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
fun StudentNoticesPanel(student: Student, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Official Notices & Alerts",
                style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold),
                color = MaterialTheme.colorScheme.primary
            )
            Divider()
            Text("No urgent personalized notices for ${student.name}. General class notices are available in the Communication Hub.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}
"""

if "fun StudentHomeworkPanel" not in content:
    content = content.replace("fun StudentFullDetailsPanel", extra_panels + "\nfun StudentFullDetailsPanel")

old_dialog_content1 = """                            StudentFullDetailsPanel(student = student)
                            StudentFeePanel(fee = fee)
                            StudentAttendancePanel(attendance = attendance)
                        }"""

new_dialog_content1 = """                            StudentFullDetailsPanel(student = student)
                            StudentFeePanel(fee = fee)
                            StudentAttendancePanel(attendance = attendance)
                            StudentHomeworkPanel(student = student)
                            StudentNoticesPanel(student = student)
                        }"""

old_dialog_content2 = """                        StudentFullDetailsPanel(student = student)
                        StudentFeePanel(fee = fee)
                        StudentAttendancePanel(attendance = attendance)
                    }"""

new_dialog_content2 = """                        StudentFullDetailsPanel(student = student)
                        StudentFeePanel(fee = fee)
                        StudentAttendancePanel(attendance = attendance)
                        StudentHomeworkPanel(student = student)
                        StudentNoticesPanel(student = student)
                    }"""

content = content.replace(old_dialog_content1, new_dialog_content1)
content = content.replace(old_dialog_content2, new_dialog_content2)

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
    f.write(content)
