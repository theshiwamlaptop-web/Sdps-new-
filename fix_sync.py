import re

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    content = f.read()

# Replace student sync
student_old = """                snapshot?.documentChanges?.forEach { change ->
                    try {
                        var student = change.document.toObject(Student::class.java)
                        if (student != null && student.studentId.isBlank()) {
                            student = student.copy(studentId = change.document.id)
                        }
                        scope.launch {
                            if (change.type != com.google.firebase.firestore.DocumentChange.Type.REMOVED) {
                                db.studentDao().insertStudent(student)
                            }
                        }
                    } catch (e: Exception) {"""
student_new = """                val studentsToInsert = mutableListOf<Student>()
                snapshot?.documentChanges?.forEach { change ->
                    try {
                        var student = change.document.toObject(Student::class.java)
                        if (student != null && student.studentId.isBlank()) {
                            student = student.copy(studentId = change.document.id)
                        }
                        if (change.type != com.google.firebase.firestore.DocumentChange.Type.REMOVED) {
                            studentsToInsert.add(student)
                        } else {
                            scope.launch { db.studentDao().deleteStudentById(student.studentId) }
                        }
                    } catch (e: Exception) {"""
content = content.replace(student_old, student_new)

# Wait, the fallback mapping also needs to be batched if it's hit, but let's just do a big launch around the loop for all collections.
