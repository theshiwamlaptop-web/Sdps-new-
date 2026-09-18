import re

filepath = 'app/src/main/java/com/example/data/repository/SchoolRepository.kt'
with open(filepath, 'r') as f:
    content = f.read()

target = """        // 13. Payrolls Synchronization Listeners
        try {
            val listener = fs.collection("payrolls").addSnapshotListener { snapshot, error ->
                if (error != null) {
                    Log.e("SchoolRepository", "Firestore Synclist Error [payrolls]: ${error.message}", error)
                    return@addSnapshotListener
                }
                snapshot?.documentChanges?.forEach { change ->
                    val payroll = change.document.toObject(Payroll::class.java)
                    scope.launch {
                        if (change.type != com.google.firebase.firestore.DocumentChange.Type.REMOVED) {
                            db.payrollDao().insertPayroll(payroll)
                        }
                    }
                }
            }
            snapshotListeners.add(listener)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Failed to register payrolls listener", e)
        }"""
        
replacement = target + """

        // 14. Notifications Synchronization Listeners
        try {
            val listener = fs.collection("notifications").addSnapshotListener { snapshot, error ->
                if (error != null) {
                    Log.e("SchoolRepository", "Firestore Synclist Error [notifications]: ${error.message}", error)
                    return@addSnapshotListener
                }
                snapshot?.documentChanges?.forEach { change ->
                    val notification = change.document.toObject(AppNotification::class.java)
                    scope.launch {
                        if (change.type != com.google.firebase.firestore.DocumentChange.Type.REMOVED) {
                            db.notificationDao().insertNotification(notification)
                        }
                    }
                }
            }
            snapshotListeners.add(listener)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Failed to register notifications listener", e)
        }"""
        
content = content.replace(target, replacement)

with open(filepath, 'w') as f:
    f.write(content)

