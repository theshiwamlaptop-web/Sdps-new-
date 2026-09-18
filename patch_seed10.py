import re

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    content = f.read()

content = content.replace(
"""        try {
            val fs = firestore ?: return Result.failure(Exception("Firestore not initialized"))
            val batch = fs.batch()""",
"""        try {
            val fs = firestore ?: return Result.failure(Exception("Firestore not initialized"))
            val authOk = firebaseAuth?.currentUser != null
            val batch = if (authOk) fs.batch() else null""")

content = content.replace(
"""                    db.studentDao().insertStudent(student)
                    batch.set(fs.collection("students").document(sId), student)""",
"""                    db.studentDao().insertStudent(student)
                    batch?.set(fs.collection("students").document(sId), student)""")

content = content.replace(
"""                    db.userDao().insertUser(user)
                    batch.set(fs.collection("users").document(sId), user)""",
"""                    db.userDao().insertUser(user)
                    batch?.set(fs.collection("users").document(sId), user)""")

content = content.replace(
"""            batch.commit().await()""",
"""            batch?.commit()?.await()""")

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write(content)
