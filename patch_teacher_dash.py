import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

start_idx = content.find("fun TeacherDashboardTab(")
if start_idx != -1:
    brace_count = 0
    end_idx = -1
    in_function = False
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
            in_function = True
        elif content[i] == '}':
            brace_count -= 1
        
        if in_function and brace_count == 0:
            end_idx = i
            break
    
    if end_idx != -1:
        new_tab = """fun TeacherDashboardTab(
    viewModel: SchoolViewModel,
    totalStudentsCount: Int,
    todayAttendanceText: String,
    lastNotice: String,
    onNavigate: (AppScreen) -> Unit
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Quick Overview Header
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Class Overview", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground))
            Text("View All", style = MaterialTheme.typography.labelMedium.copy(color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold), modifier = Modifier.clickable { onNavigate(AppScreen.STUDENTS) })
        }

        // Quick Overview Stats Row
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            DashboardStatCard(
                modifier = Modifier.weight(1f),
                icon = Icons.Filled.People,
                iconTint = Color(0xFF00E5FF),
                value = "$totalStudentsCount",
                label = "My Students",
                subLabel = "Total Enrolled",
                subLabelColor = Color(0xFF10B981)
            )
            DashboardStatCard(
                modifier = Modifier.weight(1f),
                icon = Icons.Filled.FactCheck,
                iconTint = Color(0xFF8B5CF6),
                value = todayAttendanceText,
                label = "Today's Attendance",
                subLabel = "In your class",
                subLabelColor = Color(0xFF10B981)
            )
        }

        // Quick Actions Header
        Text("Quick Actions", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground))

        // Quick Actions Grid
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                QuickActionItem(modifier = Modifier.weight(1f), icon = Icons.Filled.HowToReg, label = "Attendance", tint = Color(0xFF3B82F6), onClick = { onNavigate(AppScreen.ATTENDANCE) })
                QuickActionItem(modifier = Modifier.weight(1f), icon = Icons.Filled.MenuBook, label = "Homework", tint = Color(0xFFEC4899), onClick = { onNavigate(AppScreen.HOMEWORK) })
                QuickActionItem(modifier = Modifier.weight(1f), icon = Icons.Filled.Group, label = "Students", tint = Color(0xFF10B981), onClick = { onNavigate(AppScreen.STUDENTS) })
            }
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                QuickActionItem(modifier = Modifier.weight(1f), icon = Icons.Filled.Campaign, label = "Notices", tint = Color(0xFFEF4444), onClick = { onNavigate(AppScreen.NOTICES) })
                QuickActionItem(modifier = Modifier.weight(1f), icon = Icons.Filled.EventNote, label = "Timetable", tint = Color(0xFF00E5FF), onClick = { onNavigate(AppScreen.TIMETABLE) })
                QuickActionItem(modifier = Modifier.weight(1f), icon = Icons.Filled.CalendarMonth, label = "Calendar", tint = Color(0xFF3B82F6), onClick = { onNavigate(AppScreen.CALENDAR) })
            }
        }

        // Recent Notices
        Text("Recent Notices", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground))
        ElevatedCard(
            onClick = { onNavigate(AppScreen.NOTICES) },
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
            shape = RoundedCornerShape(12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier.size(48.dp).background(Color(0xFFF59E0B).copy(alpha=0.2f), RoundedCornerShape(12.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Filled.Campaign, null, tint = Color(0xFFF59E0B))
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(lastNotice, style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface), maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("Just updated", style = MaterialTheme.typography.bodySmall.copy(color = MaterialTheme.colorScheme.onSurfaceVariant))
                }
            }
        }
        Spacer(modifier = Modifier.height(20.dp))
    }
}"""
        
        content = content[:start_idx] + new_tab + content[end_idx+1:]
        with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
            f.write(content)
        print("Patched TeacherDashboardTab successfully")
    else:
        print("End index not found for TeacherDashboardTab")
else:
    print("Function TeacherDashboardTab not found")
