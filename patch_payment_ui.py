import re

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

old_block = '''        var eReceipt by remember { mutableStateOf(original.receiptNo.ifBlank { "REC-${System.currentTimeMillis()}" }) }
        var eDate by remember { mutableStateOf(original.paymentDate.ifBlank { java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH)) }) }
        var eAdmission by remember { mutableStateOf(original.admissionFee.toInt().toString()) }
        var eTuition by remember { mutableStateOf(original.tuitionFee.toInt().toString()) }
        var eGame by remember { mutableStateOf(original.gameFee.toInt().toString()) }
        var eExam by remember { mutableStateOf(original.examFee.toInt().toString()) }
        var eTransport by remember { mutableStateOf(original.transportFee.toInt().toString()) }
        var eLateFee by remember { mutableStateOf(original.lateFee.toInt().toString()) }
        var eConcession by remember { mutableStateOf(original.concession.toInt().toString()) }
        var ePaidAmount by remember { mutableStateOf(original.paidAmount.toInt().toString()) }
        var ePaymentMode by remember { mutableStateOf(original.paymentMode) }
        var eRemarks by remember { mutableStateOf(original.remarks) }
        
        var editError by remember { mutableStateOf<String?>(null) }
        
        AlertDialog(
            onDismissRequest = { selectedEntryForEdit = null },
            title = { Text("Update Ledger Record - ${original.month}", fontWeight = FontWeight.Bold) },
            text = {
                Column(
                    modifier = Modifier.verticalScroll(rememberScrollState()),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    OutlinedTextField(value = eReceipt, onValueChange = { eReceipt = it }, label = { Text("Receipt Number") }, modifier = Modifier.fillMaxWidth())
                    DynamicDatePicker(selectedDate = eDate, onDateSelected = { eDate = it }, label = "Date of Payment")
                    
                    Text("Fee Ledger Components (₹)", fontWeight = FontWeight.SemiBold, fontSize = 11.sp, color = MaterialTheme.colorScheme.primary)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        OutlinedTextField(modifier = Modifier.weight(1f), value = eAdmission, onValueChange = { eAdmission = it }, label = { Text("Admission") })
                        OutlinedTextField(modifier = Modifier.weight(1f), value = eTuition, onValueChange = { eTuition = it }, label = { Text("Tuition") })
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        OutlinedTextField(modifier = Modifier.weight(1f), value = eGame, onValueChange = { eGame = it }, label = { Text("Game") })
                        OutlinedTextField(modifier = Modifier.weight(1f), value = eExam, onValueChange = { eExam = it }, label = { Text("Exam Fee") })
                    }
                    OutlinedTextField(value = eTransport, onValueChange = { eTransport = it }, label = { Text("Transport Fee") }, modifier = Modifier.fillMaxWidth())
                    
                    Text("Manual Adjustments (Late / Concessions)", fontWeight = FontWeight.SemiBold, fontSize = 11.sp, color = Color(0xFFD97706))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        OutlinedTextField(modifier = Modifier.weight(1f), value = eLateFee, onValueChange = { eLateFee = it }, label = { Text("Late Fee") })
                        OutlinedTextField(modifier = Modifier.weight(1f), value = eConcession, onValueChange = { eConcession = it }, label = { Text("Discount Concession") })
                    }
                    OutlinedTextField(value = eRemarks, onValueChange = { eRemarks = it }, label = { Text("Ledger Remarks (Mandatory for Adjustments)") }, modifier = Modifier.fillMaxWidth())
                    OutlinedTextField(value = ePaidAmount, onValueChange = { ePaidAmount = it }, label = { Text("Paid Amount Collection (₹)") }, modifier = Modifier.fillMaxWidth())
                    OutlinedTextField(value = ePaymentMode, onValueChange = { ePaymentMode = it }, label = { Text("Payment Mode (Cash/Online)") }, modifier = Modifier.fillMaxWidth())
                    if (editError != null) {
                        Text(editError!!, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                    }
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        val lateVal = eLateFee.toDoubleOrNull() ?: 0.0
                        val concessionVal = eConcession.toDoubleOrNull() ?: 0.0
                        
                        if ((lateVal > 0.0 || concessionVal > 0.0) && eRemarks.isBlank()) {
                            editError = "Remarks explanation is MANDATORY when introducing Late Fee overrides or Concession Discounts!"
                        } else {
                            val updated = original.copy(
                                receiptNo = eReceipt.trim(),
                                paymentDate = eDate.trim(),
                                admissionFee = eAdmission.toDoubleOrNull() ?: 0.0,
                                tuitionFee = eTuition.toDoubleOrNull() ?: 0.0,
                                gameFee = eGame.toDoubleOrNull() ?: 0.0,
                                examFee = eExam.toDoubleOrNull() ?: 0.0,
                                transportFee = eTransport.toDoubleOrNull() ?: 0.0,
                                lateFee = lateVal,
                                concession = concessionVal,
                                paidAmount = ePaidAmount.toDoubleOrNull() ?: 0.0,
                                remarks = eRemarks.trim(), paymentMode = ePaymentMode.trim()
                            )
                            viewModel.saveFeeLedgerEntry(updated)
                            
                            val studentFeeIndex = viewModel.feesState.value.find { it.studentId == student.studentId }
                            val currentPaidAccumulated = calculatedLedger.sumOf { if (it.month == original.month) updated.paidAmount else it.paidAmount }
                            val currentBilledAccumulated = calculatedLedger.sumOf { 
                                val currentMonthEntry = if (it.month == original.month) updated else it
                                currentMonthEntry.admissionFee + currentMonthEntry.tuitionFee + currentMonthEntry.gameFee + currentMonthEntry.examFee + currentMonthEntry.transportFee + currentMonthEntry.lateFee - currentMonthEntry.concession
                            }
                            
                            val indexToSave = studentFeeIndex ?: Fee(
                                feeId = "F_${student.studentId}",
                                studentId = student.studentId
                            )
                            viewModel.addOrUpdateFee(
                                indexToSave.copy(
                                    totalFee = currentBilledAccumulated,
                                    paidAmount = currentPaidAccumulated,
                                    dueAmount = maxOf(0.0, currentBilledAccumulated - currentPaidAccumulated),
                                    paymentDate = java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))
                                )
                            )
                            
                            selectedEntryForEdit = null
                            Toast.makeText(context, "Ledger adjusted successfully for ${student.name}!", Toast.LENGTH_SHORT).show()
                        }
                    }
                ) {
                    Text("Save Adjustment")
                }
            },
            dismissButton = {
                TextButton(onClick = { selectedEntryForEdit = null }) { Text("Cancel") }
            }
        )'''

new_block = '''        var eReceipt by remember { mutableStateOf(original.receiptNo.ifBlank { "REC-${System.currentTimeMillis()}" }) }
        var eDate by remember { mutableStateOf(original.paymentDate.ifBlank { java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH)) }) }
        var eAdmission by remember { mutableStateOf(original.admissionFee.toInt().toString()) }
        var eTuition by remember { mutableStateOf(original.tuitionFee.toInt().toString()) }
        var eGame by remember { mutableStateOf(original.gameFee.toInt().toString()) }
        var eExam by remember { mutableStateOf(original.examFee.toInt().toString()) }
        var eTransport by remember { mutableStateOf(original.transportFee.toInt().toString()) }
        var eLateFee by remember { mutableStateOf(original.lateFee.toInt().toString()) }
        var eConcession by remember { mutableStateOf(original.concession.toInt().toString()) }
        var ePaidAmount by remember { mutableStateOf(original.paidAmount.toInt().toString()) }
        var ePaymentMode by remember { mutableStateOf(original.paymentMode) }
        var eRemarks by remember { mutableStateOf(original.remarks) }
        
        var editError by remember { mutableStateOf<String?>(null) }
        var isSaving by remember { mutableStateOf(false) }
        
        val admVal = eAdmission.toDoubleOrNull() ?: 0.0
        val tuiVal = eTuition.toDoubleOrNull() ?: 0.0
        val gameVal = eGame.toDoubleOrNull() ?: 0.0
        val examVal = eExam.toDoubleOrNull() ?: 0.0
        val transVal = eTransport.toDoubleOrNull() ?: 0.0
        val lateVal = eLateFee.toDoubleOrNull() ?: 0.0
        val concessionVal = eConcession.toDoubleOrNull() ?: 0.0
        val paidVal = ePaidAmount.toDoubleOrNull() ?: 0.0
        
        val totalFee = admVal + tuiVal + gameVal + examVal + transVal + lateVal - concessionVal
        val remainingBalance = totalFee - paidVal

        Dialog(
            onDismissRequest = { if(!isSaving) selectedEntryForEdit = null },
            properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)
        ) {
            Surface(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(12.dp)
                    .clip(RoundedCornerShape(24.dp)),
                color = MaterialTheme.colorScheme.background,
                tonalElevation = 6.dp
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    // Header
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(MaterialTheme.colorScheme.primaryContainer)
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("Process Payment - ${original.month}", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onPrimaryContainer, fontWeight = FontWeight.Bold)
                        IconButton(onClick = { if(!isSaving) selectedEntryForEdit = null }) {
                            Icon(Icons.Filled.Close, "Close", tint = MaterialTheme.colorScheme.onPrimaryContainer)
                        }
                    }
                    
                    Column(
                        modifier = Modifier
                            .weight(1f)
                            .padding(horizontal = 16.dp)
                            .verticalScroll(rememberScrollState()),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        // Student Profile Card
                        ElevatedCard(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),
                            elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
                        ) {
                            Row(modifier = Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .size(56.dp)
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Filled.Person, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                                }
                                Spacer(modifier = Modifier.width(16.dp))
                                Column {
                                    Text(student.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                                    Text("Class: ${student.className} | Roll No: ${student.rollNo}", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    Text("Admission No: ${student.admissionNo}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                            }
                        }

                        // Payment Details Grid
                        Text("Fee Components", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        
                        // Using custom layout for chips/cards for fees
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            OutlinedTextField(value = eAdmission, onValueChange = { eAdmission = it }, label = { Text("Admission") }, modifier = Modifier.weight(1f), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                            OutlinedTextField(value = eTuition, onValueChange = { eTuition = it }, label = { Text("Tuition") }, modifier = Modifier.weight(1f), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                        }
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            OutlinedTextField(value = eExam, onValueChange = { eExam = it }, label = { Text("Exam Fee") }, modifier = Modifier.weight(1f), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                            OutlinedTextField(value = eGame, onValueChange = { eGame = it }, label = { Text("Game") }, modifier = Modifier.weight(1f), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                        }
                        
                        OutlinedTextField(value = eTransport, onValueChange = { eTransport = it }, label = { Text("Transport Fee") }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                        
                        HorizontalDivider(modifier = Modifier.padding(vertical = 4.dp))
                        
                        Text("Adjustments & Concessions", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = Color(0xFFD97706))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            OutlinedTextField(value = eLateFee, onValueChange = { eLateFee = it }, label = { Text("Late Fee") }, modifier = Modifier.weight(1f), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                            OutlinedTextField(value = eConcession, onValueChange = { eConcession = it }, label = { Text("Discount") }, modifier = Modifier.weight(1f), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                        }
                        OutlinedTextField(value = eRemarks, onValueChange = { eRemarks = it }, label = { Text("Remarks (Mandatory if adjustments made)") }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp))
                        
                        HorizontalDivider(modifier = Modifier.padding(vertical = 4.dp))
                        
                        Text("Payment Collection", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        OutlinedTextField(value = ePaidAmount, onValueChange = { ePaidAmount = it }, label = { Text("Amount Paid Now") }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp), leadingIcon = { Text("₹", modifier = Modifier.padding(start=12.dp)) })
                        OutlinedTextField(value = ePaymentMode, onValueChange = { ePaymentMode = it }, label = { Text("Mode (Cash/UPI/Bank)") }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp), leadingIcon = { Icon(Icons.Filled.AccountBalanceWallet, null) })
                        OutlinedTextField(value = eReceipt, onValueChange = { eReceipt = it }, label = { Text("Receipt No.") }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp))
                        
                        if (editError != null) {
                            Surface(color = MaterialTheme.colorScheme.errorContainer, shape = RoundedCornerShape(8.dp), modifier = Modifier.fillMaxWidth()) {
                                Text(editError!!, color = MaterialTheme.colorScheme.onErrorContainer, modifier = Modifier.padding(12.dp), style = MaterialTheme.typography.bodySmall)
                            }
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                    }
                    
                    // Footer (Totals & Action)
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = MaterialTheme.colorScheme.surfaceVariant,
                        shadowElevation = 8.dp
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Total Fee", style = MaterialTheme.typography.bodyMedium)
                                Text("₹${"%,.0f".format(totalFee)}", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                            }
                            Spacer(modifier = Modifier.height(4.dp))
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Paid Amount", style = MaterialTheme.typography.bodyMedium)
                                Text("- ₹${"%,.0f".format(paidVal)}", style = MaterialTheme.typography.bodyLarge, color = Color(0xFF10B981), fontWeight = FontWeight.Bold)
                            }
                            HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Remaining Balance", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                                Text("₹${"%,.0f".format(remainingBalance)}", style = MaterialTheme.typography.titleLarge, color = if(remainingBalance > 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary, fontWeight = FontWeight.ExtraBold)
                            }
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            Button(
                                onClick = {
                                    if ((lateVal > 0.0 || concessionVal > 0.0) && eRemarks.isBlank()) {
                                        editError = "Remarks explanation is MANDATORY when introducing Late Fee overrides or Concession Discounts!"
                                    } else {
                                        isSaving = true
                                        val updated = original.copy(
                                            receiptNo = eReceipt.trim(),
                                            paymentDate = eDate.trim(),
                                            admissionFee = admVal,
                                            tuitionFee = tuiVal,
                                            gameFee = gameVal,
                                            examFee = examVal,
                                            transportFee = transVal,
                                            lateFee = lateVal,
                                            concession = concessionVal,
                                            paidAmount = paidVal,
                                            remarks = eRemarks.trim(), paymentMode = ePaymentMode.trim()
                                        )
                                        viewModel.saveFeeLedgerEntry(updated)
                                        
                                        val studentFeeIndex = viewModel.feesState.value.find { it.studentId == student.studentId }
                                        val currentPaidAccumulated = calculatedLedger.sumOf { if (it.month == original.month) updated.paidAmount else it.paidAmount }
                                        val currentBilledAccumulated = calculatedLedger.sumOf { 
                                            val currentMonthEntry = if (it.month == original.month) updated else it
                                            currentMonthEntry.admissionFee + currentMonthEntry.tuitionFee + currentMonthEntry.gameFee + currentMonthEntry.examFee + currentMonthEntry.transportFee + currentMonthEntry.lateFee - currentMonthEntry.concession
                                        }
                                        
                                        val indexToSave = studentFeeIndex ?: Fee(
                                            feeId = "F_${student.studentId}",
                                            studentId = student.studentId
                                        )
                                        viewModel.addOrUpdateFee(
                                            indexToSave.copy(
                                                totalFee = currentBilledAccumulated,
                                                paidAmount = currentPaidAccumulated,
                                                dueAmount = maxOf(0.0, currentBilledAccumulated - currentPaidAccumulated),
                                                paymentDate = java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("dd MMMM yyyy", java.util.Locale.ENGLISH))
                                            )
                                        )
                                        
                                        selectedEntryForEdit = null
                                        Toast.makeText(context, "Payment Processed Successfully!", Toast.LENGTH_SHORT).show()
                                    }
                                },
                                modifier = Modifier.fillMaxWidth().height(56.dp),
                                shape = RoundedCornerShape(16.dp),
                                enabled = !isSaving
                            ) {
                                if (isSaving) {
                                    CircularProgressIndicator(color = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(24.dp))
                                } else {
                                    Icon(Icons.Filled.CheckCircle, "Save")
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("Confirm Payment", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }
            }
        }'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Block not found!")
