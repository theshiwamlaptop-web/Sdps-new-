import re

filepath = 'app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

target = """                StudentDetailDialogLayout(
                    student = currentStudent,
                    fee = studentFee,
                    attendance = studentAttendance,
                    onDismiss = { selectedStudentDialog = null },
                    canEdit = isManagement,
                    onSave = { updated -> viewModel.updateStudent(updated); selectedStudentDialog = updated },
                    onOpenFeeLedger = {"""
                    
replacement = """                StudentDetailDialogLayout(
                    student = currentStudent,
                    fee = studentFee,
                    attendance = studentAttendance,
                    onDismiss = { selectedStudentDialog = null },
                    canEdit = isManagement || (isTeacher && currentStudent.className.equals(teacherClass, ignoreCase = true)),
                    onSave = { updated -> viewModel.updateStudent(updated); selectedStudentDialog = updated },
                    onOpenFeeLedger = {"""
                    
content = content.replace(target, replacement)

with open(filepath, 'w') as f:
    f.write(content)
