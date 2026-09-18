with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "Conflicting declarations" in line:
        pass # Not a python error, but let's just strip out the duplicated code blocks
        
# Actually, I'll just remove the duplicate lines in SchoolViewModel.kt near 1203
with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    text = f.read()

import re
# Find something like:
#            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
#            if (role == "STUDENT") { _toastMessage.value = "Unauthorized"; return@launch }
#            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
#            if (role == "STUDENT" || role == "PARENT") {

text = re.sub(
    r'val role = repository.currentUserFlow.value\?.role\?.uppercase\(\)\?.trim\(\) \?: ""\n\s*if \(role == "STUDENT"\) \{ _toastMessage.value = "Unauthorized"; return@launch \}\n\s*val role = repository.currentUserFlow.value\?.role\?.uppercase\(\)\?.trim\(\) \?: ""',
    r'val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""\n            if (role == "STUDENT") { _toastMessage.value = "Unauthorized"; return@launch }',
    text
)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(text)
