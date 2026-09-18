with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

target = """    // Calendar events
    private val _calendarEvents = MutableStateFlow(
        listOf(
            CalendarEvent("2026-05-28", "Inter-School Science Fair 2026", "Event"),
            CalendarEvent("2026-06-01", "Summer Vacation Starts", "Holiday"),
            CalendarEvent("2026-07-01", "School Reopens", "Notification"),
            CalendarEvent("2026-05-25", "Fee Submission Deadline", "Exam/Submission")
        )
    )
    val calendarEvents = _calendarEvents.asStateFlow()"""

replacement = """    // Calendar events connected to Room + Firestore repository
    val calendarEvents: StateFlow<List<CalendarEvent>> = repository.getAllCalendarEvents()
        .flowOn(kotlinx.coroutines.Dispatchers.Default)
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun saveCalendarEvent(event: CalendarEvent) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized: Only school management can add or update calendar events."
                return@launch
            }
            if (event.title.isBlank()) {
                _toastMessage.value = "Event title cannot be empty."
                return@launch
            }
            val eventToSave = if (event.id.isBlank()) event.copy(id = "CAL_" + java.util.UUID.randomUUID().toString().take(8)) else event
            val result = repository.saveCalendarEvent(eventToSave)
            if (result.isSuccess) {
                _toastMessage.value = "Calendar event saved successfully!"
                logAudit("SAVE_CALENDAR_EVENT", eventToSave.id, "Saved event: ${eventToSave.title}")
            } else {
                _toastMessage.value = "Failed to save calendar event: ${result.exceptionOrNull()?.message}"
            }
        }
    }

    fun deleteCalendarEvent(eventId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized: Only school management can delete calendar events."
                return@launch
            }
            val result = repository.deleteCalendarEvent(eventId)
            if (result.isSuccess) {
                _toastMessage.value = "Calendar event deleted."
                logAudit("DELETE_CALENDAR_EVENT", eventId, "Deleted calendar event")
            } else {
                _toastMessage.value = "Failed to delete calendar event: ${result.exceptionOrNull()?.message}"
            }
        }
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
        f.write(content)
    print("SchoolViewModel.kt patched successfully")
else:
    print("Target not found in SchoolViewModel.kt")
