import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_delete_teacher = """    fun deleteTeacher(teacherId: String) {
        viewModelScope.launch {
            repository.deleteTeacher(teacherId)
        }
    }"""

new_delete_teacher = """    fun deleteTeacher(teacherId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN") {
                _toastMessage.value = "Unauthorized: Only Principal/Head Admin can delete teachers."
                return@launch
            }
            repository.deleteTeacher(teacherId)
        }
    }"""

content = content.replace(old_delete_teacher, new_delete_teacher)

old_add_teacher = """    fun addOrUpdateTeacher(teacher: Teacher) {
        viewModelScope.launch {
            repository.addTeacher(teacher)
        }
    }"""

new_add_teacher = """    fun addOrUpdateTeacher(teacher: Teacher) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized: Only management can modify teachers."
                return@launch
            }
            repository.addTeacher(teacher)
        }
    }"""

content = content.replace(old_add_teacher, new_add_teacher)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
