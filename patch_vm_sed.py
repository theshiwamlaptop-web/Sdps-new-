import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    if "fun saveClassBook(" in line or "fun deleteClassBook(" in line or "fun issueBook(" in line:
        # It's followed by viewModelScope.launch {
        new_lines.append(lines[i+1])
        new_lines.append('            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""\n')
        new_lines.append('            if (role == "STUDENT") { _toastMessage.value = "Unauthorized"; return@launch }\n')
        i += 1
    i += 1

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.writelines(new_lines)
