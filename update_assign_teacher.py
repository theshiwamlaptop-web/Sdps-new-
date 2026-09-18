import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

# Update interface
content = content.replace(
    'suspend fun assignClassTeacher(teacherBId: String, className: String): Result<Unit>',
    'suspend fun assignClassTeacher(teacherBId: String, className: String, actionUserId: String, actionUserName: String): Result<Unit>'
)

# Update implementation signature
content = content.replace(
    'override suspend fun assignClassTeacher(teacherBId: String, className: String): Result<Unit> {',
    'override suspend fun assignClassTeacher(teacherBId: String, className: String, actionUserId: String, actionUserName: String): Result<Unit> {'
)

# Insert the AuditLog insertion right before return Result.success(Unit) inside the implementation
old_return = """            return Result.success(Unit)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Error assignClassTeacher: ${e.message}", e)"""

new_return = """            
            val logId = "AL_${System.currentTimeMillis()}"
            val auditLog = AuditLog(
                logId = logId,
                timestamp = System.currentTimeMillis(),
                userId = actionUserId,
                userName = actionUserName,
                action = "Assigned Teacher $teacherBId as Class Teacher of $className",
                oldValue = "Unknown",
                newValue = className
            )
            db.auditLogDao().insertAuditLog(auditLog)
            firestore?.collection("audit_logs")?.document(logId)?.set(auditLog)

            return Result.success(Unit)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Error assignClassTeacher: ${e.message}", e)"""

content = content.replace(old_return, new_return)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
