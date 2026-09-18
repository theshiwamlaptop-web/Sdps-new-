import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_delete_leave = """    fun deleteLeaveRequest(requestId: String) {
        viewModelScope.launch {
            repository.deleteLeaveRequest(requestId)
        }
    }"""

new_delete_leave = """    fun deleteLeaveRequest(requestId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            // Simple security: only management can delete leave requests completely
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized."
                return@launch
            }
            repository.deleteLeaveRequest(requestId)
        }
    }"""

content = content.replace(old_delete_leave, new_delete_leave)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
