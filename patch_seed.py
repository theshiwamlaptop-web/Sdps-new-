import re

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    content = f.read()

# Fix seedInitialDataIfNeeded
content = content.replace(
"""    private suspend fun seedInitialDataIfNeeded() {
        if (firebaseAuth?.currentUser == null) {
            android.util.Log.d("SchoolRepository", "Skipping seed Initial Data in Firestore: User is not authenticated.")
            // We can still seed room database if needed, but let's just skip the whole thing to avoid permission denied
            // or we could just let Room seeding happen and skip Firestore
            // Actually, we need to prevent the PERMISSION_DENIED error. 
        }""",
"""    private suspend fun seedInitialDataIfNeeded() {""")

content = content.replace(
"""        if (currentStudents.isEmpty()) {
            studentList.forEach { 
                db.studentDao().insertStudent(it) 
                firestore?.collection("students")?.document(it.studentId)?.set(it)""",
"""        val authOk = firebaseAuth?.currentUser != null
        if (currentStudents.isEmpty()) {
            studentList.forEach { 
                db.studentDao().insertStudent(it)
                if (authOk) firestore?.collection("students")?.document(it.studentId)?.set(it)""")

content = content.replace(
"""                db.userDao().insertUser(user)
                firestore?.collection("users")?.document(it.studentId)?.set(user)
            }
            teacherList.forEach { 
                db.teacherDao().insertTeacher(it)
                firestore?.collection("teachers")?.document(it.teacherId)?.set(it)""",
"""                db.userDao().insertUser(user)
                if (authOk) firestore?.collection("users")?.document(it.studentId)?.set(user)
            }
            teacherList.forEach { 
                db.teacherDao().insertTeacher(it)
                if (authOk) firestore?.collection("teachers")?.document(it.teacherId)?.set(it)""")

content = content.replace(
"""                db.userDao().insertUser(user)
                firestore?.collection("users")?.document(it.teacherId)?.set(user)
            }
            feeList.forEach { 
                db.feeDao().insertFee(it)
                firestore?.collection("fees")?.document(it.feeId)?.set(it)
            }
            homeworkList.forEach { 
                db.homeworkDao().insertHomework(it)
                firestore?.collection("homework")?.document(it.homeworkId)?.set(it)
            }
            noticeList.forEach { 
                db.noticeDao().insertNotice(it)
                firestore?.collection("notices")?.document(it.noticeId)?.set(it)
            }
            timetableList.forEach { 
                db.timetableDao().insertTimetable(it)
                firestore?.collection("timetable")?.document(it.timetableId)?.set(it)
            }
            initialChatMessages.forEach { 
                db.chatDao().insertMessage(it)
                firestore?.collection("chats")?.document(it.messageId)?.set(it)
            }
            db.attendanceDao().insertAttendance(attendanceList)
            attendanceList.forEach {
                firestore?.collection("attendance")?.document(it.attendanceId)?.set(it)
            }""",
"""                db.userDao().insertUser(user)
                if (authOk) firestore?.collection("users")?.document(it.teacherId)?.set(user)
            }
            feeList.forEach { 
                db.feeDao().insertFee(it)
                if (authOk) firestore?.collection("fees")?.document(it.feeId)?.set(it)
            }
            homeworkList.forEach { 
                db.homeworkDao().insertHomework(it)
                if (authOk) firestore?.collection("homework")?.document(it.homeworkId)?.set(it)
            }
            noticeList.forEach { 
                db.noticeDao().insertNotice(it)
                if (authOk) firestore?.collection("notices")?.document(it.noticeId)?.set(it)
            }
            timetableList.forEach { 
                db.timetableDao().insertTimetable(it)
                if (authOk) firestore?.collection("timetable")?.document(it.timetableId)?.set(it)
            }
            initialChatMessages.forEach { 
                db.chatDao().insertMessage(it)
                if (authOk) firestore?.collection("chats")?.document(it.messageId)?.set(it)
            }
            db.attendanceDao().insertAttendance(attendanceList)
            if (authOk) {
                attendanceList.forEach {
                    firestore?.collection("attendance")?.document(it.attendanceId)?.set(it)
                }
            }""")

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write(content)
