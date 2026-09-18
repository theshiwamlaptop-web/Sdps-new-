import re

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

fake_header_regex = r'// App Top Bar / Header\s*Row\(\s*modifier = Modifier\.fillMaxWidth\(\),\s*horizontalArrangement = Arrangement\.SpaceBetween,\s*verticalAlignment = Alignment\.CenterVertically\s*\)\s*\{\s*Row\(verticalAlignment = Alignment\.CenterVertically\)\s*\{\s*Image\([\s\S]*?\}\s*\}\s*Spacer\(modifier = Modifier\.height\(16\.dp\)\)'

content = re.sub(fake_header_regex, '', content)

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
    f.write(content)

