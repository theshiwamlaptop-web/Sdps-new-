import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_del = """    fun deleteClassBook(bookId: String) {
        viewModelScope.launch {
            repository.deleteClassBook(bookId)
            logAudit("DELETE_CLASS_BOOK", bookId, "Deleted book")
        }
    }"""
new_del = """    fun deleteClassBook(bookId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role == "STUDENT" || role == "PARENT") {
                _toastMessage.value = "Unauthorized"
                return@launch
            }
            repository.deleteClassBook(bookId)
            logAudit("DELETE_CLASS_BOOK", bookId, "Deleted book")
        }
    }"""
content = content.replace(old_del, new_del)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
