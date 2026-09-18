cat << 'INNER_EOF' >> app/src/main/java/com/example/data/model/Models.kt

@Entity(tableName = "leave_requests")
data class LeaveRequest(
    @PrimaryKey val requestId: String = "",
    val studentId: String = "",
    val studentName: String = "",
    val className: String = "",
    val startDate: String = "", // YYYY-MM-DD
    val endDate: String = "",
    val reason: String = "",
    val status: String = "", // Pending, Approved, Rejected
    val timestamp: Long = 0L,
    val reviewedBy: String = ""
)
INNER_EOF
