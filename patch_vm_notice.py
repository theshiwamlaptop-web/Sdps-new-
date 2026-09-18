import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_add_notice = """    fun addNotice(notice: Notice) {
        viewModelScope.launch {
            repository.addNotice(notice)
        }
    }"""

new_add_notice = """    fun addNotice(notice: Notice) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role == "STUDENT") {
                _toastMessage.value = "Unauthorized: Students cannot post notices."
                return@launch
            }
            repository.addNotice(notice)
        }
    }"""

content = content.replace(old_add_notice, new_add_notice)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
