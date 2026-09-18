import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_delete_student = """    fun deleteStudent(studentId: String) {
        viewModelScope.launch {
            val user = repository.currentUserFlow.value"""

new_delete_student = """    fun deleteStudent(studentId: String) {
        viewModelScope.launch {
            val user = repository.currentUserFlow.value
            val role = user?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized: Only management can delete students."
                return@launch
            }"""

if old_delete_student in content:
    content = content.replace(old_delete_student, new_delete_student)
else:
    print("Failed to find deleteStudent")

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
