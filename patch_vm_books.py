import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_add_book = """    fun addOrUpdateClassBook(book: ClassBook) {
        viewModelScope.launch {
            repository.addClassBook(book)
        }
    }"""

new_add_book = """    fun addOrUpdateClassBook(book: ClassBook) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") return@launch
            repository.addClassBook(book)
        }
    }"""

content = content.replace(old_add_book, new_add_book)

old_delete_book = """    fun deleteClassBook(bookId: String) {
        viewModelScope.launch {
            repository.deleteClassBook(bookId)
        }
    }"""

new_delete_book = """    fun deleteClassBook(bookId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") return@launch
            repository.deleteClassBook(bookId)
        }
    }"""

content = content.replace(old_delete_book, new_delete_book)

old_issue = """    fun issueBook(issuedBook: IssuedBook) {
        viewModelScope.launch {
            repository.addIssuedBook(issuedBook)
        }
    }"""

new_issue = """    fun issueBook(issuedBook: IssuedBook) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") return@launch
            repository.addIssuedBook(issuedBook)
        }
    }"""

content = content.replace(old_issue, new_issue)

old_delete_issue = """    fun deleteIssuedBook(issueId: String) {
        viewModelScope.launch {
            repository.deleteIssuedBook(issueId)
        }
    }"""

new_delete_issue = """    fun deleteIssuedBook(issueId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") return@launch
            repository.deleteIssuedBook(issueId)
        }
    }"""

content = content.replace(old_delete_issue, new_delete_issue)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
