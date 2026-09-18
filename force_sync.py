import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

target = """    init {
        // Automatically checks if DB seeding is required and starts Real-time background sync
        scope.launch {
            checkFirebaseConnectivityAndLog()
            seedInitialDataIfNeeded()
            startBackgroundFirebaseSync()
        }"""

replacement = """    init {
        // Automatically checks if DB seeding is required and starts Real-time background sync
        scope.launch {
            checkFirebaseConnectivityAndLog()
            seedInitialDataIfNeeded()
            startBackgroundFirebaseSync()
            
            // ONE-TIME FORCE SYNC FOR THE USER
            val fs = firestore
            if (fs != null) {
                try {
                    val students = fs.collection("students").get().await()
                    students.documents.forEach { doc ->
                        val s = doc.toObject(Student::class.java)
                        if (s != null) db.studentDao().insertStudent(s)
                    }
                    val users = fs.collection("users").get().await()
                    users.documents.forEach { doc ->
                        val u = doc.toObject(User::class.java)
                        if (u != null) db.userDao().insertUser(u)
                    }
                    val teachers = fs.collection("teachers").get().await()
                    teachers.documents.forEach { doc ->
                        val t = doc.toObject(Teacher::class.java)
                        if (t != null) db.teacherDao().insertTeacher(t)
                    }
                    android.util.Log.d("SchoolRepository", "Force sync completed from Firebase.")
                } catch (e: Exception) {
                    android.util.Log.e("SchoolRepository", "Force sync failed", e)
                }
            }
        }"""

if target in content:
    content = content.replace(target, replacement)
    print("Added Force Sync")

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)

