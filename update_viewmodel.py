import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_vm = """    fun assignClassTeacher(teacherBId: String, className: String, onComplete: (Boolean) -> Unit = {}) {
        viewModelScope.launch {
            val res = repository.assignClassTeacher(teacherBId, className)
            onComplete(res.isSuccess)
        }
    }"""

new_vm = """    fun assignClassTeacher(teacherBId: String, className: String, onComplete: (Boolean) -> Unit = {}) {
        val user = _currentUser.value
        val userId = user?.userId ?: "System"
        val userName = user?.name ?: "System"
        viewModelScope.launch {
            val res = repository.assignClassTeacher(teacherBId, className, userId, userName)
            onComplete(res.isSuccess)
        }
    }"""

content = content.replace(old_vm, new_vm)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
