import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_promote = """    fun promoteToAdmin(teacherId: String, onComplete: (Boolean) -> Unit = {}) {
        viewModelScope.launch {
            val res = repository.promoteToAdmin(teacherId)
            if (res.isSuccess) {
                logAudit("ROLE_CHANGED", "TEACHER", "Promoted $teacherId to ADMIN")
            }
            onComplete(res.isSuccess)
        }
    }"""

new_promote = """    fun promoteToAdmin(teacherId: String, onComplete: (Boolean) -> Unit = {}) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN") {
                _toastMessage.value = "Unauthorized."
                onComplete(False)
                return@launch
            }
            val res = repository.promoteToAdmin(teacherId)
            if (res.isSuccess) {
                logAudit("ROLE_CHANGED", "TEACHER", "Promoted $teacherId to ADMIN")
            }
            onComplete(res.isSuccess)
        }
    }"""

content = content.replace(old_promote, new_promote)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
