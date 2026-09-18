import re

filepath = 'app/src/main/java/com/example/ui/screens/AddStudentScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

target_adm = """                var showAdmDatePicker by remember { mutableStateOf(false) }
                if (showAdmDatePicker) {
                    val datePickerState = rememberDatePickerState()
                    DatePickerDialog(
                        onDismissRequest = { showAdmDatePicker = false },
                        confirmButton = {
                            TextButton(onClick = {
                                datePickerState.selectedDateMillis?.let { millis ->
                                    val date = java.time.Instant.ofEpochMilli(millis).atZone(java.time.ZoneId.of("UTC")).toLocalDate()
                                    sAdmissionDate = date.toString()
                                }
                                showAdmDatePicker = false
                            }) { Text("OK") }
                        },
                        dismissButton = {
                            TextButton(onClick = { showAdmDatePicker = false }) { Text("Cancel") }
                        }
                    ) {
                        DatePicker(state = datePickerState)
                    }
                }
                
                OutlinedTextField(
                    value = sAdmissionDate,
                    onValueChange = { sAdmissionDate = it },
                    label = { Text("Admission Date") },
                    readOnly = true,
                    trailingIcon = {
                        IconButton(onClick = { showAdmDatePicker = true }) {
                            Icon(Icons.Filled.DateRange, contentDescription = "Select Date")
                        }
                    },
                    modifier = Modifier.fillMaxWidth().clickable { showAdmDatePicker = true }
                )"""

replacement_adm = """                DynamicDatePicker(selectedDate = sAdmissionDate, onDateSelected = { sAdmissionDate = it }, label = "Admission Date")"""

content = content.replace(target_adm, replacement_adm)

target_father = """                OutlinedTextField(value = sFather, onValueChange = { sFather = it }, label = { Text("Father's Name") }, modifier = Modifier.fillMaxWidth())"""
replacement_father = """                DynamicDatePicker(selectedDate = sDOB, onDateSelected = { sDOB = it }, label = "Date of Birth")
                OutlinedTextField(value = sFather, onValueChange = { sFather = it }, label = { Text("Father's Name") }, modifier = Modifier.fillMaxWidth())"""
content = content.replace(target_father, replacement_father)

with open(filepath, 'w') as f:
    f.write(content)
