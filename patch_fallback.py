import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

bad_insert = '''                                scope.launch { db.studentDao().insertStudent(fallbackStudent) }'''
good_insert = '''                                scope.launch {
                                    if (change.type != com.google.firebase.firestore.DocumentChange.Type.REMOVED) {
                                        db.studentDao().insertStudent(fallbackStudent)
                                    } else {
                                        val existing = db.studentDao().getStudentById(fallbackStudent.studentId)
                                        if (existing != null) {
                                            db.studentDao().insertStudent(existing.copy(isDeleted = true, status = "DELETED"))
                                        }
                                    }
                                }'''

content = content.replace(bad_insert, good_insert)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)

print("Patched fallback parser inserts.")
