import re

with open('app/src/main/java/com/example/ui/screens/AddStudentScreen.kt', 'r') as f:
    content = f.read()

# Add states for Gender, Guardian Name, Admission Date, Status, Linked Siblings
new_states = """    var sAddress by remember { mutableStateOf("") }
    
    // New fields requested by user
    var sGender by remember { mutableStateOf("Male") }
    var isSGenderExpanded by remember { mutableStateOf(false) }
    
    var sGuardian by remember { mutableStateOf("") }
    var sAdmissionDate by remember { mutableStateOf(java.time.LocalDate.now().toString()) }
    var sStatus by remember { mutableStateOf("Active") }
    var isSStatusExpanded by remember { mutableStateOf(false) }
    var sLinkedSiblings by remember { mutableStateOf("") }
"""
content = re.sub(r'    var sAddress by remember \{ mutableStateOf\(""\) \}', new_states, content)

# Add UI fields for the new states
new_ui_fields = """                OutlinedTextField(
                    value = sAddress,
                    onValueChange = { sAddress = it },
                    label = { Text("Residence Address") },
                    isError = sAddress.isNotEmpty() && !isSAddressValid,
                    supportingText = { if (sAddress.isNotEmpty() && !isSAddressValid) Text("Address must be at least 3 characters") },
                    modifier = Modifier.fillMaxWidth().testTag("student_address_input")
                )
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Box(modifier = Modifier.weight(1f)) {
                        OutlinedTextField(
                            value = sGender,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Gender") },
                            trailingIcon = { Icon(Icons.Filled.ArrowDropDown, "Select Gender") },
                            modifier = Modifier.fillMaxWidth().clickable { isSGenderExpanded = true }
                        )
                        DropdownMenu(expanded = isSGenderExpanded, onDismissRequest = { isSGenderExpanded = false }) {
                            listOf("Male", "Female", "Other").forEach { g ->
                                DropdownMenuItem(text = { Text(g) }, onClick = { sGender = g; isSGenderExpanded = false })
                            }
                        }
                    }
                    Box(modifier = Modifier.weight(1f)) {
                        OutlinedTextField(
                            value = sStatus,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Status") },
                            trailingIcon = { Icon(Icons.Filled.ArrowDropDown, "Select Status") },
                            modifier = Modifier.fillMaxWidth().clickable { isSStatusExpanded = true }
                        )
                        DropdownMenu(expanded = isSStatusExpanded, onDismissRequest = { isSStatusExpanded = false }) {
                            listOf("Active", "Inactive", "Left School").forEach { s ->
                                DropdownMenuItem(text = { Text(s) }, onClick = { sStatus = s; isSStatusExpanded = false })
                            }
                        }
                    }
                }
                
                OutlinedTextField(value = sGuardian, onValueChange = { sGuardian = it }, label = { Text("Guardian's Name (Optional)") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = sAdmissionDate, onValueChange = { sAdmissionDate = it }, label = { Text("Admission Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = sLinkedSiblings, onValueChange = { sLinkedSiblings = it }, label = { Text("Linked Siblings (Optional)") }, modifier = Modifier.fillMaxWidth())
"""
content = re.sub(r'                OutlinedTextField\([\s\n]*value = sAddress,[^)]+\)[\s\n]*\)', new_ui_fields, content)

# Update Student instantiation
new_student_instantiation = """                        val st = Student(
                            studentId = finalId,
                            name = sName,
                            className = sClass,
                            rollNo = sRoll,
                            DOB = sDOB,
                            fatherName = sFather,
                            motherName = sMother,
                            guardianName = sGuardian,
                            phone = sPhone,
                            address = sAddress,
                            admissionNo = sAdmNo,
                            admissionDate = sAdmissionDate,
                            gender = sGender,
                            status = sStatus,
                            linkedSiblings = sLinkedSiblings,
                            photoUrl = "" // Removed visual unmapped photos
                        )"""
content = re.sub(r'                        val st = Student\([^)]+\)', new_student_instantiation, content)

with open('app/src/main/java/com/example/ui/screens/AddStudentScreen.kt', 'w') as f:
    f.write(content)
