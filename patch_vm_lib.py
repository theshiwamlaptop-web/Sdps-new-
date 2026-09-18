import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_lib = """    fun addOrUpdateClassBook(book: ClassBook) {
        viewModelScope.launch {
            repository.addClassBook(book)
            logAudit("ADD_UPDATE_CLASS_BOOK", book.bookId, "Added/Updated book: ${book.title}")
        }
    }

    fun deleteClassBook(bookId: String) {
        viewModelScope.launch {
            repository.deleteClassBook(bookId)
            logAudit("DELETE_CLASS_BOOK", bookId, "Deleted book")
        }
    }"""

new_lib = """    fun addOrUpdateClassBook(book: ClassBook) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN" && role != "LIBRARIAN") {
                _toastMessage.value = "Unauthorized"
                return@launch
            }
            repository.addClassBook(book)
            logAudit("ADD_UPDATE_CLASS_BOOK", book.bookId, "Added/Updated book: ${book.title}")
        }
    }

    fun deleteClassBook(bookId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN" && role != "LIBRARIAN") {
                _toastMessage.value = "Unauthorized"
                return@launch
            }
            repository.deleteClassBook(bookId)
            logAudit("DELETE_CLASS_BOOK", bookId, "Deleted book")
        }
    }"""

content = content.replace(old_lib, new_lib)

old_issue = """    fun issueBook(issuedBook: IssuedBook) {
        viewModelScope.launch {
            repository.issueBook(issuedBook)
            logAudit("ISSUE_BOOK", issuedBook.issueId, "Issued book to student: ${issuedBook.studentId}")
        }
    }

    fun deleteIssuedBook(issueId: String) {
        viewModelScope.launch {
            repository.deleteIssuedBook(issueId)
            logAudit("RETURN_BOOK", issueId, "Deleted issued book record")
        }
    }"""

new_issue = """    fun issueBook(issuedBook: IssuedBook) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN" && role != "LIBRARIAN") {
                _toastMessage.value = "Unauthorized"
                return@launch
            }
            repository.issueBook(issuedBook)
            logAudit("ISSUE_BOOK", issuedBook.issueId, "Issued book to student: ${issuedBook.studentId}")
        }
    }

    fun deleteIssuedBook(issueId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN" && role != "LIBRARIAN") {
                _toastMessage.value = "Unauthorized"
                return@launch
            }
            repository.deleteIssuedBook(issueId)
            logAudit("RETURN_BOOK", issueId, "Deleted issued book record")
        }
    }"""

content = content.replace(old_issue, new_issue)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
