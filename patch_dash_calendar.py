with open('app/src/main/java/com/example/ui/screens/DashboardScreen.kt', 'r') as f:
    content = f.read()

target_p = """                                Triple("Notices", Icons.Filled.Campaign, AppScreen.NOTICES)"""
repl_p = """                                Triple("Notices", Icons.Filled.Campaign, AppScreen.NOTICES),
                                Triple("Calendar", Icons.Filled.Event, AppScreen.CALENDAR)"""

target_t = """                                Triple("Timetable", Icons.Filled.Schedule, AppScreen.TIMETABLE)"""
repl_t = """                                Triple("Timetable", Icons.Filled.Schedule, AppScreen.TIMETABLE),
                                Triple("Calendar", Icons.Filled.Event, AppScreen.CALENDAR)"""

target_s = """                                Triple("Timetable", Icons.Filled.Schedule, AppScreen.TIMETABLE)"""
repl_s = """                                Triple("Timetable", Icons.Filled.Schedule, AppScreen.TIMETABLE),
                                Triple("Calendar", Icons.Filled.Event, AppScreen.CALENDAR)"""

content = content.replace(target_p, repl_p, 1)
content = content.replace(target_t, repl_t, 1)
content = content.replace(target_s, repl_s, 1)

with open('app/src/main/java/com/example/ui/screens/DashboardScreen.kt', 'w') as f:
    f.write(content)

print("DashboardScreen.kt patched with Calendar action")
