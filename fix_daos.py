import re

with open("app/src/main/java/com/example/data/local/DatabaseAndDaos.kt", "r") as f:
    content = f.read()

def add_list_insert(content, single_func, model_name):
    # e.g. suspend fun insertStudent(student: Student)
    replacement = single_func + f"\n\n    @Insert(onConflict = OnConflictStrategy.REPLACE)\n    suspend fun insert{model_name}s(items: List<{model_name}>)"
    return content.replace(single_func, replacement)

content = add_list_insert(content, "suspend fun insertStudent(student: Student)", "Student")
content = add_list_insert(content, "suspend fun insertTeacher(teacher: Teacher)", "Teacher")
content = add_list_insert(content, "suspend fun insertFee(fee: Fee)", "Fee")
content = add_list_insert(content, "suspend fun insertHomework(homework: Homework)", "Homework")
content = add_list_insert(content, "suspend fun insertNotice(notice: Notice)", "Notice")
content = add_list_insert(content, "suspend fun insertMessage(message: ChatMessage)", "ChatMessage")
content = add_list_insert(content, "suspend fun insertTimetable(timetable: Timetable)", "Timetable")

with open("app/src/main/java/com/example/data/local/DatabaseAndDaos.kt", "w") as f:
    f.write(content)

