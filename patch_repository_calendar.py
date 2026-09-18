with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

# 1. Add interface methods
target_interface = "    // Leave Requests\n    fun getAllLeaveRequests(): Flow<List<LeaveRequest>>"
replacement_interface = """    // School Calendar
    fun getAllCalendarEvents(): Flow<List<CalendarEvent>>
    suspend fun saveCalendarEvent(event: CalendarEvent): Result<Unit>
    suspend fun deleteCalendarEvent(eventId: String): Result<Unit>

    // Leave Requests
    fun getAllLeaveRequests(): Flow<List<LeaveRequest>>"""

content = content.replace(target_interface, replacement_interface)

# 2. Add implementation methods at bottom before closing brace
target_impl_end = """    override suspend fun deleteIssuedBook(issueId: String): Result<Unit> {
        return try {
            db.issuedBookDao().deleteIssuedBookById(issueId)
            firestore?.collection("issued_books")?.document(issueId)?.delete()
            Result.success(Unit)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Error deleting issued book", e)
            Result.failure(e)
        }
    }
}"""

replacement_impl_end = """    override suspend fun deleteIssuedBook(issueId: String): Result<Unit> {
        return try {
            db.issuedBookDao().deleteIssuedBookById(issueId)
            firestore?.collection("issued_books")?.document(issueId)?.delete()
            Result.success(Unit)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Error deleting issued book", e)
            Result.failure(e)
        }
    }

    // SCHOOL CALENDAR IMPLEMENTATION
    override fun getAllCalendarEvents(): Flow<List<CalendarEvent>> {
        return db.calendarEventDao().getAllCalendarEventsFlow()
    }

    override suspend fun saveCalendarEvent(event: CalendarEvent): Result<Unit> {
        return try {
            db.calendarEventDao().insertCalendarEvent(event)
            firestore?.collection("calendar_events")?.document(event.id)?.set(event)
            Result.success(Unit)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Error saving calendar event", e)
            Result.failure(e)
        }
    }

    override suspend fun deleteCalendarEvent(eventId: String): Result<Unit> {
        return try {
            db.calendarEventDao().deleteCalendarEventById(eventId)
            firestore?.collection("calendar_events")?.document(eventId)?.delete()
            Result.success(Unit)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Error deleting calendar event", e)
            Result.failure(e)
        }
    }
}"""

content = content.replace(target_impl_end, replacement_impl_end)

# 3. Add Firestore listener in setupFirestoreSync
target_sync = """        // 7. Timetable Synchronization Listeners"""
replacement_sync = """        // Calendar Events Synchronization Listener
        try {
            val listener = fs.collection("calendar_events").addSnapshotListener { snapshot, error ->
                if (error != null) {
                    Log.e("SchoolRepository", "Firestore Synclist Error [calendar_events]: ${error.message}", error)
                    return@addSnapshotListener
                }
                scope.launch {
                    db.withTransaction {
                        snapshot?.documentChanges?.forEach { change ->
                            var ev = change.document.toObject(CalendarEvent::class.java)
                            if (ev != null && ev.id.isBlank()) {
                                ev = ev.copy(id = change.document.id)
                            }
                            if (change.type != com.google.firebase.firestore.DocumentChange.Type.REMOVED) {
                                if (ev != null) db.calendarEventDao().insertCalendarEvent(ev)
                            } else {
                                db.calendarEventDao().deleteCalendarEventById(change.document.id)
                            }
                        }
                    }
                }
            }
            snapshotListeners.add(listener)
        } catch (e: Exception) {
            Log.e("SchoolRepository", "Failed to register calendar events listener", e)
        }

        // 7. Timetable Synchronization Listeners"""

content = content.replace(target_sync, replacement_sync)

# 4. Add seed events in initial database population
target_seed_list = """        val timetableList = listOf("""
replacement_seed_list = """        val calendarEventList = listOf(
            CalendarEvent(id = "CAL_1", date = "2026-05-28", title = "Inter-School Science Fair 2026", description = "Annual science exhibition for senior classes.", type = "School Event", time = "09:00 AM", targetClass = "All", createdBy = "Principal"),
            CalendarEvent(id = "CAL_2", date = "2026-06-01", title = "Summer Vacation Starts", description = "School closed for summer break.", type = "Holiday", time = "All Day", targetClass = "All", createdBy = "Management"),
            CalendarEvent(id = "CAL_3", date = "2026-07-01", title = "School Reopens", description = "Classes resume after summer break.", type = "School Event", time = "08:00 AM", targetClass = "All", createdBy = "Management"),
            CalendarEvent(id = "CAL_4", date = "2026-05-25", title = "Fee Submission Deadline", description = "Last date for Q1 fee submission.", type = "Fee Deadline", time = "05:00 PM", targetClass = "All", createdBy = "Finance Office"),
            CalendarEvent(id = "CAL_5", date = "2026-08-15", title = "Independence Day Celebration", description = "Flag hoisting ceremony and cultural performance.", type = "Holiday", time = "08:30 AM", targetClass = "All", createdBy = "Principal"),
            CalendarEvent(id = "CAL_6", date = "2026-09-10", title = "Mid-Term Examinations", description = "Half-yearly term exams start.", type = "Exam", time = "09:00 AM", targetClass = "All", createdBy = "Exam Dept")
        )

        val timetableList = listOf("""

content = content.replace(target_seed_list, replacement_seed_list)

target_seed_insert = """            timetableList.forEach { 
                db.timetableDao().insertTimetable(it)
                if (authOk) firestore?.collection("timetable")?.document(it.timetableId)?.set(it)
            }"""

replacement_seed_insert = """            timetableList.forEach { 
                db.timetableDao().insertTimetable(it)
                if (authOk) firestore?.collection("timetable")?.document(it.timetableId)?.set(it)
            }
            calendarEventList.forEach {
                db.calendarEventDao().insertCalendarEvent(it)
                if (authOk) firestore?.collection("calendar_events")?.document(it.id)?.set(it)
            }"""

content = content.replace(target_seed_insert, replacement_seed_insert)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)

print("SchoolRepository.kt patched successfully")
