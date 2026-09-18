import re

filepath = 'app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

# I will find the OutlinedTextField for sPhone in StudentAdmissionScreen and insert dob and admissionDate after it
target = """                OutlinedTextField(
                    value = sPhone,
                    onValueChange = { sPhone = it },
                    label = { Text("Contact Phone") },
                    modifier = Modifier.fillMaxWidth().testTag("student_phone_input")
                )"""

replacement = """                OutlinedTextField(
                    value = sPhone,
                    onValueChange = { sPhone = it },
                    label = { Text("Contact Phone") },
                    modifier = Modifier.fillMaxWidth().testTag("student_phone_input")
                )
                DynamicDatePicker(selectedDate = dob, onDateSelected = { dob = it }, label = "Date of Birth")
                DynamicDatePicker(selectedDate = admissionDate, onDateSelected = { admissionDate = it }, label = "Date of Admission")
"""

content = content.replace(target, replacement)

# We should also ensure dob and admissionDate are saved when newStudent is created
student_creation = """                        val newStudent = Student(
                            studentId = cleanId,
                            id = cleanId,
                            name = name,
                            className = selectedClass,
                            rollNo = rollNoVal,
                            fatherName = sFather,
                            motherName = "Co-Guardian",
                            phone = sPhone,
                            address = "Residential Area",
                            admissionNo = "ADM_${cleanId}",
                            rollNumber = cleanRoll,
                            attendanceStatus = "Present",
                            feeStatus = "Pending",
                            role = "STUDENT"
                        )"""
student_creation_replacement = """                        val newStudent = Student(
                            studentId = cleanId,
                            id = cleanId,
                            name = name,
                            className = selectedClass,
                            rollNo = rollNoVal,
                            DOB = dob,
                            dateOfAdmission = admissionDate,
                            fatherName = sFather,
                            motherName = "Co-Guardian",
                            phone = sPhone,
                            address = "Residential Area",
                            admissionNo = "ADM_${cleanId}",
                            rollNumber = cleanRoll,
                            attendanceStatus = "Present",
                            feeStatus = "Pending",
                            role = "STUDENT"
                        )"""
content = content.replace(student_creation, student_creation_replacement)

with open(filepath, 'w') as f:
    f.write(content)
