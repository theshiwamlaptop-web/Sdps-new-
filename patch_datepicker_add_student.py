import re

filepath = 'app/src/main/java/com/example/ui/screens/AddStudentScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

dob_target = """                OutlinedTextField(
                    value = sDOB,
                    onValueChange = { sDOB = it },
                    label = { Text("Date of Birth (YYYY-MM-DD)") },
                    isError = sDOB.isNotEmpty() && !isSDOBValid,
                    supportingText = { if (sDOB.isNotEmpty() && !isSDOBValid) Text("Invalid format") },
                    modifier = Modifier.weight(0.8f).testTag("student_dob_input")
                )"""

dob_replacement = """                var showDOBPicker by remember { mutableStateOf(false) }
                if (showDOBPicker) {
                    val datePickerState = rememberDatePickerState()
                    DatePickerDialog(
                        onDismissRequest = { showDOBPicker = false },
                        confirmButton = {
                            TextButton(onClick = {
                                datePickerState.selectedDateMillis?.let { millis ->
                                    val date = java.time.Instant.ofEpochMilli(millis).atZone(java.time.ZoneId.of("UTC")).toLocalDate()
                                    sDOB = date.toString()
                                }
                                showDOBPicker = false
                            }) { Text("OK") }
                        },
                        dismissButton = {
                            TextButton(onClick = { showDOBPicker = false }) { Text("Cancel") }
                        }
                    ) {
                        DatePicker(state = datePickerState)
                    }
                }
                
                OutlinedTextField(
                    value = sDOB,
                    onValueChange = { sDOB = it },
                    label = { Text("Date of Birth") },
                    readOnly = true,
                    isError = sDOB.isNotEmpty() && !isSDOBValid,
                    supportingText = { if (sDOB.isNotEmpty() && !isSDOBValid) Text("Invalid format") },
                    trailingIcon = {
                        IconButton(onClick = { showDOBPicker = true }) {
                            Icon(Icons.Filled.DateRange, contentDescription = "Select Date")
                        }
                    },
                    modifier = Modifier.weight(0.8f).testTag("student_dob_input").clickable { showDOBPicker = true }
                )"""

if dob_target in content:
    content = content.replace(dob_target, dob_replacement)
else:
    print("Could not find dob_target")


adm_date_target = """                OutlinedTextField(value = sAdmissionDate, onValueChange = { sAdmissionDate = it }, label = { Text("Admission Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())"""
adm_date_replacement = """                var showAdmDatePicker by remember { mutableStateOf(false) }
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
                
if adm_date_target in content:
    content = content.replace(adm_date_target, adm_date_replacement)
else:
    print("Could not find adm_date_target")


with open(filepath, 'w') as f:
    f.write(content)
