with open("app/src/main/java/com/example/data/local/DatabaseAndDaos.kt", "r") as f:
    lines = f.readlines()

new_dao = """
@Dao
interface LeaveRequestDao {
    @Query("SELECT * FROM leave_requests ORDER BY timestamp DESC")
    fun getAllLeaveRequestsFlow(): Flow<List<LeaveRequest>>
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLeaveRequest(leaveRequest: LeaveRequest)
    @Query("DELETE FROM leave_requests WHERE requestId = :requestId")
    suspend fun deleteLeaveRequestById(requestId: String)
}
"""
lines.append(new_dao)

with open("app/src/main/java/com/example/data/local/DatabaseAndDaos.kt", "w") as f:
    for line in lines:
        if "version = 7" in line:
            f.write(line.replace("version = 7", "version = 8"))
        elif "IssuedBook::class" in line:
            f.write("        IssuedBook::class,\n        LeaveRequest::class\n")
        elif "abstract fun issuedBookDao(): IssuedBookDao" in line:
            f.write(line)
            f.write("    abstract fun leaveRequestDao(): LeaveRequestDao\n")
        else:
            f.write(line)

