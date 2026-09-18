import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

bad_att = '''    fun saveAttendance(attendanceList: List<Attendance>) {
        viewModelScope.launch {
            repository.markAttendance(attendanceList)
        }
    }'''

good_att = '''    fun saveAttendance(attendanceList: List<Attendance>) {
        viewModelScope.launch {
            val result = repository.markAttendance(attendanceList)
            if (result.isFailure) {
                _toastMessage.value = "Failed to sync attendance to cloud: ${result.exceptionOrNull()?.message}"
            }
        }
    }'''

content = content.replace(bad_att, good_att)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
print("Patched SchoolViewModel.")
