import re
import os

filepath = 'app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Replace DynamicDatePicker
new_picker = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DynamicDatePicker(
    selectedDate: String,
    onDateSelected: (String) -> Unit,
    isReadOnly: Boolean = false,
    label: String = "Selected Date",
    disableFutureDates: Boolean = false
) {
    var showDialog by remember { mutableStateOf(false) }
    
    val formatter = remember { java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH) }
    
    val initialDateMillis = try {
        java.time.LocalDate.parse(selectedDate, formatter).atStartOfDay(java.time.ZoneOffset.UTC).toInstant().toEpochMilli()
    } catch (e: Exception) {
        try {
            java.time.LocalDate.parse(selectedDate).atStartOfDay(java.time.ZoneOffset.UTC).toInstant().toEpochMilli()
        } catch (e2: Exception) {
            System.currentTimeMillis()
        }
    }

    val datePickerState = rememberDatePickerState(
        initialSelectedDateMillis = initialDateMillis,
        selectableDates = object : SelectableDates {
            override fun isSelectableDate(utcTimeMillis: Long): Boolean {
                if (isReadOnly) return true
                if (disableFutureDates) return utcTimeMillis <= System.currentTimeMillis()
                return true
            }
            override fun isSelectableYear(year: Int): Boolean {
                return year in 1900..2100
            }
        }
    )

    val displayDate = try {
        java.time.LocalDate.parse(selectedDate, formatter).format(formatter)
    } catch (e: Exception) {
        try {
            java.time.LocalDate.parse(selectedDate).format(formatter)
        } catch (e2: Exception) {
            selectedDate.ifBlank { java.time.LocalDate.now().format(formatter) }
        }
    }

    Card(
        modifier = Modifier.fillMaxWidth().clickable(enabled = !isReadOnly) { showDialog = true },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp).fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(label, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(displayDate, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
            }
            if (!isReadOnly) {
                Icon(Icons.Filled.CalendarMonth, contentDescription = "Change Date", tint = MaterialTheme.colorScheme.primary)
            }
        }
    }

    if (showDialog) {
        DatePickerDialog(
            onDismissRequest = { showDialog = false },
            confirmButton = {
                TextButton(onClick = {
                    datePickerState.selectedDateMillis?.let { millis ->
                        val date = java.time.Instant.ofEpochMilli(millis).atZone(java.time.ZoneOffset.UTC).toLocalDate()
                        onDateSelected(date.format(formatter))
                    }
                    showDialog = false
                }) {
                    Text("OK")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) {
                    Text("Cancel")
                }
            }
        ) {
            DatePicker(state = datePickerState)
        }
    }
}
"""

old_picker_regex = re.compile(r'@Composable\nfun DynamicDatePicker\(.*?if \(showDialog\) \{.*?DatePicker\(state = datePickerState\)\n        }\n    }\n}', re.DOTALL)
content = old_picker_regex.sub(new_picker, content)

# 2. Replace selectedDate state init for Attendance
content = content.replace(
    'var selectedDate by remember { mutableStateOf(java.time.LocalDate.now().toString()) }',
    'var selectedDate by remember { mutableStateOf(java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))) }'
)
content = content.replace(
    'val todayStr = java.time.LocalDate.now().toString()',
    'val todayStr = java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))'
)
content = content.replace(
    'selectedDate == java.time.LocalDate.now().toString()',
    'selectedDate == java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))'
)

# 3. Replace tJoiningDate TextField
t_joining = """OutlinedTextField(
                                    value = tJoiningDate,
                                    onValueChange = { tJoiningDate = it },
                                    label = { Text("Joining Date") },
                                    leadingIcon = { Icon(Icons.Filled.DateRange, null) },
                                    modifier = Modifier.weight(1f)
                                )"""
t_joining_new = """Box(modifier = Modifier.weight(1f)) {
                                    DynamicDatePicker(
                                        selectedDate = tJoiningDate,
                                        onDateSelected = { tJoiningDate = it },
                                        label = "Joining Date"
                                    )
                                }"""
content = content.replace(t_joining, t_joining_new)

# 4. hDue TextField
h_due = """OutlinedTextField(value = hDue, onValueChange = { hDue = it }, label = { Text("Due Deadline (YYYY-MM-DD)") })"""
h_due_new = """DynamicDatePicker(selectedDate = hDue, onDateSelected = { hDue = it }, label = "Due Deadline")"""
content = content.replace(h_due, h_due_new)

# 5. editDOB and editDateOfAdmission
edit_dob = """OutlinedTextField(value = editDOB, onValueChange = { editDOB = it }, label = { Text("Date of Birth (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())"""
edit_dob_new = """DynamicDatePicker(selectedDate = editDOB, onDateSelected = { editDOB = it }, label = "Date of Birth")"""
content = content.replace(edit_dob, edit_dob_new)

edit_doa = """OutlinedTextField(value = editDateOfAdmission, onValueChange = { editDateOfAdmission = it }, label = { Text("Date of Admission") }, modifier = Modifier.fillMaxWidth())"""
edit_doa_new = """DynamicDatePicker(selectedDate = editDateOfAdmission, onDateSelected = { editDateOfAdmission = it }, label = "Date of Admission")"""
content = content.replace(edit_doa, edit_doa_new)

# 6. eDate
e_date = """OutlinedTextField(value = eDate, onValueChange = { eDate = it }, label = { Text("Date of Payment (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())"""
e_date_new = """DynamicDatePicker(selectedDate = eDate, onDateSelected = { eDate = it }, label = "Date of Payment")"""
content = content.replace(e_date, e_date_new)

# eDate initialization
e_date_init = """var eDate by remember { mutableStateOf(original.paymentDate.ifBlank { SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date()) }) }"""
e_date_init_new = """var eDate by remember { mutableStateOf(original.paymentDate.ifBlank { java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH)) }) }"""
content = content.replace(e_date_init, e_date_init_new)
content = content.replace(
    'paymentDate = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())',
    'paymentDate = java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))'
)

# 7. tJoiningDate initialization
t_joining_init = """var tJoiningDate by remember { mutableStateOf("2026-04-01") }"""
t_joining_init_new = """var tJoiningDate by remember { mutableStateOf(java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))) }"""
content = content.replace(t_joining_init, t_joining_init_new)

# admissionDate initialization
adm_date_init = """var admissionDate by remember { mutableStateOf(java.time.LocalDate.now().toString()) }"""
adm_date_init_new = """var admissionDate by remember { mutableStateOf(java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))) }"""
content = content.replace(adm_date_init, adm_date_init_new)

# notice date formatting
notice_date = """date = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date()),"""
notice_date_new = """date = java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH)),"""
content = content.replace(notice_date, notice_date_new)


with open(filepath, 'w') as f:
    f.write(content)

print("Dates patched.")
