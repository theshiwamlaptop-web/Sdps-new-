import re
with open("app/src/main/java/com/example/ui/SchoolViewModel.kt", "r") as f:
    content = f.read()

t = """    fun promoteToAdmin(teacherId: String, onComplete: (Boolean) -> Unit = {}) {"""
r = """    fun requestDeletion(targetId: String, targetType: String, targetName: String, requesterName: String, requesterId: String) {
        viewModelScope.launch {
            val notifId = "DELREQ_${targetType}_${targetId}_${System.currentTimeMillis()}"
            val message = "Admin:\n$requesterName\n\nRequested deletion of:\n\n$targetType:\n$targetName\n\nID:\n$targetId"
            val notification = com.example.data.model.AppNotification(
                notificationId = notifId,
                userId = "PRINCIPAL",
                title = "Deletion Request",
                message = message,
                timestamp = System.currentTimeMillis(),
                isRead = false,
                type = "DELETE_REQUEST"
            )
            repository.addNotification(notification)
            
            repository.addAuditLog(
                com.example.data.model.AuditLog(
                    logId = java.util.UUID.randomUUID().toString(),
                    timestamp = System.currentTimeMillis(),
                    userId = requesterId,
                    userName = requesterName,
                    action = "DELETE_REQUEST",
                    targetEntity = targetType,
                    targetId = targetId,
                    details = "Requested deletion for $targetName"
                )
            )
        }
    }

    fun approveDeletion(notification: com.example.data.model.AppNotification, principalName: String, principalId: String) {
        viewModelScope.launch {
            val parts = notification.notificationId.split("_")
            if (parts.size >= 3) {
                val targetType = parts[1]
                val targetId = parts[2]
                
                if (targetType == "STUDENT") {
                    deleteStudent(targetId)
                } else if (targetType == "TEACHER") {
                    deleteTeacher(targetId)
                }
                deleteUserAccount(targetId)
                
                repository.addAuditLog(
                    com.example.data.model.AuditLog(
                        logId = java.util.UUID.randomUUID().toString(),
                        timestamp = System.currentTimeMillis(),
                        userId = principalId,
                        userName = principalName,
                        action = "DELETE_APPROVED",
                        targetEntity = targetType,
                        targetId = targetId,
                        details = "Approved deletion requested by Admin"
                    )
                )
            }
            
            val updated = notification.copy(type = "APPROVED", title = "Deletion Approved", isRead = true)
            repository.addNotification(updated)
        }
    }

    fun rejectDeletion(notification: com.example.data.model.AppNotification, principalName: String, principalId: String) {
        viewModelScope.launch {
            val parts = notification.notificationId.split("_")
            if (parts.size >= 3) {
                val targetType = parts[1]
                val targetId = parts[2]
                
                repository.addAuditLog(
                    com.example.data.model.AuditLog(
                        logId = java.util.UUID.randomUUID().toString(),
                        timestamp = System.currentTimeMillis(),
                        userId = principalId,
                        userName = principalName,
                        action = "DELETE_REJECTED",
                        targetEntity = targetType,
                        targetId = targetId,
                        details = "Rejected deletion request"
                    )
                )
            }
            
            val updated = notification.copy(type = "REJECTED", title = "Deletion Rejected", isRead = true)
            repository.addNotification(updated)
        }
    }

    fun promoteToAdmin(teacherId: String, onComplete: (Boolean) -> Unit = {}) {"""
content = content.replace(t, r)
with open("app/src/main/java/com/example/ui/SchoolViewModel.kt", "w") as f:
    f.write(content)
