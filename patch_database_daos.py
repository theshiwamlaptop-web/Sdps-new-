with open('app/src/main/java/com/example/data/local/DatabaseAndDaos.kt', 'r') as f:
    content = f.read()

# 1. Add CalendarEvent::class to entities
old_entities = "LeaveRequest::class\n    ],"
new_entities = "LeaveRequest::class,\n        CalendarEvent::class\n    ],"
content = content.replace(old_entities, new_entities)

# 2. Bump version = 11 to version = 12
content = content.replace("version = 11,", "version = 12,")

# 3. Add abstract fun calendarEventDao(): CalendarEventDao
old_db_methods = "abstract fun leaveRequestDao(): LeaveRequestDao\n}"
new_db_methods = "abstract fun leaveRequestDao(): LeaveRequestDao\n    abstract fun calendarEventDao(): CalendarEventDao\n}"
content = content.replace(old_db_methods, new_db_methods)

# 4. Add CalendarEventDao interface at bottom
dao_code = """

@Dao
interface CalendarEventDao {
    @Query("SELECT * FROM calendar_events ORDER BY date ASC, createdAt DESC")
    fun getAllCalendarEventsFlow(): Flow<List<CalendarEvent>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCalendarEvent(event: CalendarEvent)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCalendarEvents(events: List<CalendarEvent>)

    @Query("DELETE FROM calendar_events WHERE id = :eventId")
    suspend fun deleteCalendarEventById(eventId: String)

    @Query("SELECT * FROM calendar_events WHERE id = :eventId LIMIT 1")
    suspend fun getCalendarEventById(eventId: String): CalendarEvent?
}
"""

content += dao_code

with open('app/src/main/java/com/example/data/local/DatabaseAndDaos.kt', 'w') as f:
    f.write(content)

print("DatabaseAndDaos.kt patched successfully")
