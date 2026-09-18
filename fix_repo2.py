with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    text = f.read()

lines = text.split("\n")
out = []
i = 0
while i < len(lines):
    line = lines[i]
    if "scope.launch {" in line and ("db.noticeDao().insertNotice" in "".join(lines[i:i+10]) or "db.attendanceDao().insertAttendance" in "".join(lines[i:i+10]) or "db.classBookDao().insertClassBook" in "".join(lines[i:i+10]) or "db.issuedBookDao().insertIssuedBook" in "".join(lines[i:i+10]) or "db.routineDao().insertRoutine" in "".join(lines[i:i+10]) or "db.examDao().insertExam" in "".join(lines[i:i+10]) or "db.homeworkDao().insertHomework" in "".join(lines[i:i+10]) or "db.staffDao().insertStaff" in "".join(lines[i:i+10]) or "db.subjectDao().insertSubject" in "".join(lines[i:i+10]) or "db.payrollDao().insertPayroll" in "".join(lines[i:i+10]) or "db.teacherAttendanceDao().insertTeacherAttendance" in "".join(lines[i:i+10]) or "db.auditLogDao().insertAuditLog" in "".join(lines[i:i+10]) or "db.notificationDao().insertNotification" in "".join(lines[i:i+10]) or "db.feeDao().insertFee" in "".join(lines[i:i+10])):
        
        # We need to ensure it's not the outer scope.launch
        if "db.withTransaction" not in line and "db.withTransaction" not in "".join(lines[i:i+3]):
            i += 1
            # find corresponding close brace
            j = i
            brace_count = 1
            while j < len(lines):
                if "{" in lines[j]:
                    brace_count += lines[j].count("{")
                if "}" in lines[j]:
                    brace_count -= lines[j].count("}")
                if brace_count == 0:
                    lines[j] = lines[j].replace("}", "", 1)
                    break
                j += 1
            continue
    out.append(line)
    i += 1

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write("\n".join(out))

