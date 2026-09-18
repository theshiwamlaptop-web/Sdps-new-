import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_func = """    fun addOrUpdateStudent(student: Student) {
        viewModelScope.launch {
            android.util.Log.d("SchoolViewModel", "Adding student: ${student.name}")
            val user = repository.currentUserFlow.value"""

new_func = """    fun addOrUpdateStudent(student: Student, isEdit: Boolean = false) {
        viewModelScope.launch {
            if (!isEdit) {
                val existsLocally = studentsState.value.any { it.studentId == student.studentId }
                if (existsLocally) {
                    _toastMessage.value = "Duplicate Error: Student ID ${student.studentId} already exists."
                    return@launch
                }
            }
            android.util.Log.d("SchoolViewModel", "Adding student: ${student.name}")
            val user = repository.currentUserFlow.value"""

content = content.replace(old_func, new_func)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
