import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_delete_user = """    fun deleteUserAccount(userId: String, onComplete: (Boolean) -> Unit = {}) {
        viewModelScope.launch {
            val res = repository.deleteUserAccount(userId)
            onComplete(res.isSuccess)
        }
    }"""

new_delete_user = """    fun deleteUserAccount(userId: String, onComplete: (Boolean) -> Unit = {}) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN") {
                _toastMessage.value = "Unauthorized: Only Principal/Head Admin can delete user accounts."
                onComplete(False)
                return@launch
            }
            val res = repository.deleteUserAccount(userId)
            onComplete(res.isSuccess)
        }
    }"""

content = content.replace(old_delete_user, new_delete_user)

old_update_student = """    fun updateStudent(student: Student) {
        viewModelScope.launch {
            repository.updateStudent(student)"""

new_update_student = """    fun updateStudent(student: Student) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                // If it's a teacher updating their own student, let's allow it if it's safe. But wait, updateStudent is generally a management operation in StudentProfileScreen.
                // Let's assume ADMIN, HEAD_ADMIN, PRINCIPAL are fully allowed.
                // If a teacher wants to edit, we should check if they are the class teacher. But it's safer to just let the ViewModel proceed if the UI allowed it, but wait, the prompt says action level!
                // Actually, the teacher is allowed to edit their own students in StudentManagementScreen `canEdit = isManagement || (isTeacher && currentStudent.className.equals(teacherClass, ignoreCase = true))`
                // Let's implement that check.
                if (role == "TEACHER" || role == "CLASS_TEACHER") {
                     val teacherInfo = repository.getAllTeachers().firstOrNull()?.find { it.teacherId == repository.currentUserFlow.value?.userId }
                     val teacherClass = teacherInfo?.classesAssigned ?: ""
                     if (!student.className.equals(teacherClass, ignoreCase = true)) {
                         _toastMessage.value = "Unauthorized: You can only edit your own class students."
                         return@launch
                     }
                } else {
                     _toastMessage.value = "Unauthorized: You do not have permission to edit students."
                     return@launch
                }
            }
            repository.updateStudent(student)"""

content = content.replace(old_update_student, new_update_student)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
