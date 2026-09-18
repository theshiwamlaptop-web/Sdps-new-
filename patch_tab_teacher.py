import re
with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

t1 = """    // Form inputs state
    var tName by remember { mutableStateOf("") }"""
r1 = """    // Form inputs state
    var tName by remember { mutableStateOf("") }
    var tGender by remember { mutableStateOf("") }
    var isTGenderExpanded by remember { mutableStateOf(false) }"""
content = content.replace(t1, r1)

gender_ui = """                @OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
                androidx.compose.material3.ExposedDropdownMenuBox(
                    expanded = isTGenderExpanded,
                    onExpandedChange = { isTGenderExpanded = it },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    OutlinedTextField(
                        value = tGender,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Gender") },
                        trailingIcon = { androidx.compose.material3.ExposedDropdownMenuDefaults.TrailingIcon(expanded = isTGenderExpanded) },
                        colors = androidx.compose.material3.ExposedDropdownMenuDefaults.outlinedTextFieldColors(),
                        modifier = Modifier.menuAnchor().fillMaxWidth()
                    )
                    androidx.compose.material3.ExposedDropdownMenu(
                        expanded = isTGenderExpanded,
                        onDismissRequest = { isTGenderExpanded = false }
                    ) {
                        listOf("Male", "Female", "Other").forEach { g ->
                            androidx.compose.material3.DropdownMenuItem(
                                text = { Text(g) },
                                onClick = { 
                                    tGender = g
                                    isTGenderExpanded = false 
                                }
                            )
                        }
                    }
                }"""

t2 = """                // Name Input
                OutlinedTextField(
                    value = tName,
                    onValueChange = { tName = it.uppercase() },
                    label = { Text("Teacher Name") },
                    leadingIcon = { Icon(Icons.Filled.Person, "Name") },
                    modifier = Modifier.fillMaxWidth().testTag("teacher_name_input")
                )"""
r2 = t2 + "\n" + gender_ui
content = content.replace(t2, r2)

t3 = """                        val t = Teacher(
                            teacherId = tId,
                            name = tName,
                            subject = primarySubject,"""
r3 = """                        if (tGender.isBlank() || tGender == "Select Gender") {
                            Toast.makeText(context, "Error: Please select a gender", Toast.LENGTH_SHORT).show()
                            return@Button
                        }
                        val t = Teacher(
                            teacherId = tId,
                            name = tName,
                            gender = tGender,
                            subject = primarySubject,"""
content = content.replace(t3, r3)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)
