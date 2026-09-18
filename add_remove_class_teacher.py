import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

# Interface
content = content.replace(
    'suspend fun assignClassTeacher(teacherBId: String, className: String, actionUserId: String, actionUserName: String): Result<Unit>',
    'suspend fun assignClassTeacher(teacherBId: String, className: String, actionUserId: String, actionUserName: String): Result<Unit>\n    suspend fun removeClassTeacher(teacherId: String, actionUserId: String, actionUserName: String): Result<Unit>'
)

# Implementation
impl = """
    override suspend fun removeClassTeacher(teacherId: String, actionUserId: String, actionUserName: String): Result<Unit> {
        return try {
            val fs = firestore
            if (fs != null) {
                fs.runTransaction { transaction ->
                    val teacherRef = fs.collection("teachers").document(teacherId)
                    transaction.update(teacherRef, "classTeacherOf", "", "classesAssigned", "")
                    
                    val userRef = fs.collection("users").document(teacherId)
                    transaction.update(userRef, "role", "TEACHER", "className", "")
                }.await()
            }
            
            // Sync to local
            val teacher = db.teacherDao().getTeacherById(teacherId)
            if (teacher != null) {
                val updated = teacher.copy(classTeacherOf = "", classesAssigned = "")
                db.teacherDao().insertTeacher(updated)
            }
            
            val user = db.userDao().getUser(teacherId)
            if (user != null) {
                db.userDao().insertUser(user.copy(role = "TEACHER", className = ""))
            }
            
            val logId = "AL_${System.currentTimeMillis()}"
            val auditLog = AuditLog(
                logId = logId,
                timestamp = System.currentTimeMillis(),
                userId = actionUserId,
                userName = actionUserName,
                action = "Removed Class Teacher designation from $teacherId",
                oldValue = "Class Teacher",
                newValue = "Teacher"
            )
            db.auditLogDao().insertAuditLog(auditLog)
            firestore?.collection("audit_logs")?.document(logId)?.set(auditLog)
            
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
"""

content = content.replace(
    'override suspend fun assignClassTeacher',
    impl + '\n    override suspend fun assignClassTeacher'
)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    vm_content = f.read()

vm_impl = """
    fun removeClassTeacher(teacherId: String, onComplete: (Boolean) -> Unit = {}) {
        val user = _currentUser.value
        val userId = user?.userId ?: "System"
        val userName = user?.name ?: "System"
        viewModelScope.launch {
            val res = repository.removeClassTeacher(teacherId, userId, userName)
            onComplete(res.isSuccess)
        }
    }
"""
vm_content = vm_content.replace(
    'fun assignClassTeacher',
    vm_impl + '\n    fun assignClassTeacher'
)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(vm_content)
