import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_delete_homework = """    fun deleteHomework(homeworkId: String) {
        viewModelScope.launch {
            repository.deleteHomework(homeworkId)
        }
    }"""

new_delete_homework = """    fun deleteHomework(homeworkId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role == "STUDENT") return@launch
            repository.deleteHomework(homeworkId)
        }
    }"""

content = content.replace(old_delete_homework, new_delete_homework)

old_add_homework = """    fun uploadHomework(homework: Homework) {
        viewModelScope.launch {
            repository.addHomework(homework)
        }
    }"""

new_add_homework = """    fun uploadHomework(homework: Homework) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role == "STUDENT") return@launch
            repository.addHomework(homework)
        }
    }"""

content = content.replace(old_add_homework, new_add_homework)

old_delete_notice = """    fun deleteNotice(noticeId: String) {
        viewModelScope.launch {
            repository.deleteNotice(noticeId)
        }
    }"""

new_delete_notice = """    fun deleteNotice(noticeId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role == "STUDENT") return@launch
            repository.deleteNotice(noticeId)
        }
    }"""

content = content.replace(old_delete_notice, new_delete_notice)


old_add_notice = """    fun addNotice(notice: Notice) {
        viewModelScope.launch {
            repository.addNotice(notice)
        }
    }"""

new_add_notice = """    fun addNotice(notice: Notice) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role == "STUDENT") return@launch
            repository.addNotice(notice)
        }
    }"""

content = content.replace(old_add_notice, new_add_notice)


with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
