import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

# Replace the AttendanceManagementScreen function with nothing
# It starts with @Composable\nfun AttendanceManagementScreen
# And ends before fun FeeComponentRow

start_idx = content.find("fun AttendanceManagementScreen")
# Need to go back to find @Composable if it exists
composable_idx = content.rfind("@Composable", 0, start_idx)

end_idx = content.find("fun FeeComponentRow", start_idx)
# Need to go back to previous @Composable
end_composable_idx = content.rfind("@Composable", start_idx, end_idx)

if composable_idx != -1 and end_composable_idx != -1:
    content = content[:composable_idx] + content[end_composable_idx:]
    with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Could not find bounds")

