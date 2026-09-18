import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

# Add to interface
old_interface = "suspend fun addStudent(student: Student): Result<Unit>"
new_interface = "suspend fun checkStudentExists(studentId: String): Boolean\n    suspend fun addStudent(student: Student): Result<Unit>"
content = content.replace(old_interface, new_interface)

# Implement in OfflineSchoolRepository
old_impl = "override suspend fun addStudent(student: Student): Result<Unit> {"
new_impl = """override suspend fun checkStudentExists(studentId: String): Boolean {
        return try {
            val localExists = db.studentDao().getStudentById(studentId) != null
            if (localExists) return true
            val fs = firestore
            if (fs != null) {
                val doc = fs.collection("students").document(studentId).get().await()
                return doc.exists()
            }
            return false
        } catch (e: Exception) {
            false
        }
    }

    override suspend fun addStudent(student: Student): Result<Unit> {"""

content = content.replace(old_impl, new_impl)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
