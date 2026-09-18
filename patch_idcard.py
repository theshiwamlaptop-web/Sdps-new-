import re

filepath = 'app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

target = """fun StudentIdentityBadge(student: Student, modifier: Modifier = Modifier, showUserId: Boolean = false) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .wrapContentHeight(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF0F172A)) // Deep Slate
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Card Header
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Filled.School, null, tint = Color(0xFFF59E0B), modifier = Modifier.size(24.dp))"""

replacement = """fun StudentIdentityBadge(student: Student, modifier: Modifier = Modifier, showUserId: Boolean = false) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .wrapContentHeight(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF0F172A)), // Deep Slate
        border = androidx.compose.foundation.BorderStroke(2.dp, Color(0xFFFFB703)) // Golden border
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Card Header
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Image(
                    painter = painterResource(id = R.drawable.logo_sdps),
                    contentDescription = "School Logo",
                    contentScale = ContentScale.Fit,
                    modifier = Modifier.size(32.dp)
                )"""

content = content.replace(target, replacement)
with open(filepath, 'w') as f:
    f.write(content)

