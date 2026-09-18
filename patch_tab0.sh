#!/bin/bash
# Patch Tab 0 in SchoolAppScreens.kt to include MonthlyFeeEngine and the detailed table

sed -i '/0 -> {/,/1 -> {/c\
                0 -> {\
                    ElevatedCard(\
                        colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),\
                        shape = RoundedCornerShape(12.dp),\
                        modifier = Modifier.fillMaxWidth()\
                    ) {\
                        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {\
                            Text("Monthly Fee Engine", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)\
                            MonthlyFeeEngine(\
                                academicMonths = academicMonths,\
                                calculatedLedger = calculatedLedger,\
                                selectedMonths = selectedMonths,\
                                onMonthSelected = { month ->\
                                    selectedMonths = if (selectedMonths.contains(month)) selectedMonths - month else selectedMonths + month\
                                }\
                            )\
                            if (selectedMonths.isNotEmpty() && !isReadOnly) {\
                                Button(\
                                    onClick = { showMultiMonthCollectionDialog = true },\
                                    modifier = Modifier.fillMaxWidth().height(50.dp),\
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)\
                                ) {\
                                    Icon(Icons.Filled.Payment, "Proceed to Payment")\
                                    Spacer(modifier = Modifier.width(8.dp))\
                                    Text("Proceed to Collect ${selectedMonths.size} Month(s)", fontWeight = FontWeight.Bold, fontSize = 15.sp)\
                                }\
                            }\
                            \
                            Divider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.outlineVariant)\
                            \
                            Text(\
                                text = "Detailed Ledger Sheet (Swipe horizontally)",\
                                fontSize = 12.sp,\
                                color = Color.Gray,\
                                fontWeight = FontWeight.SemiBold\
                            )\
                            Box(\
                                modifier = Modifier\
                                    .fillMaxWidth()\
                                    .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(8.dp))\
                                    .clip(RoundedCornerShape(8.dp))\
                            ) {\
                                Box(modifier = Modifier.horizontalScroll(rememberScrollState())) {\
                                    Column {\
                                        Row(\
                                            modifier = Modifier\
                                                .background(MaterialTheme.colorScheme.primaryContainer)\
                                                .padding(vertical = 10.dp)\
                                        ) {\
                                            TableCell("MONTH", 85, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onPrimaryContainer)\
                                            TableCell("ADMISSION", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("TUITION", 75, fontWeight = FontWeight.Bold)\
                                            TableCell("GAME", 70, fontWeight = FontWeight.Bold)\
                                            TableCell("EXAM", 70, fontWeight = FontWeight.Bold)\
                                            TableCell("TRANSPORT", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("LATE FEE", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("DISCOUNT", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("ARREAR", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("NET PAYABLE", 100, fontWeight = FontWeight.Bold)\
                                            TableCell("PAID", 100, fontWeight = FontWeight.Bold)\
                                            TableCell("BALANCE", 100, fontWeight = FontWeight.Bold)\
                                            TableCell("DATE", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("RECEIPT", 110, fontWeight = FontWeight.Bold)\
                                            TableCell("ACTIONS", 110, fontWeight = FontWeight.Bold)\
                                        }\
                                        calculatedLedger.forEach { entry ->\
                                            val isPaid = entry.paidAmount >= entry.totalPayable && entry.totalPayable > 0\
                                            Row(\
                                                modifier = Modifier\
                                                    .fillMaxWidth()\
                                                    .border(0.5.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))\
                                                    .background(if (isPaid) Color(0xFFF0FDF4) else Color.Transparent)\
                                                    .padding(vertical = 12.dp),\
                                                verticalAlignment = Alignment.CenterVertically\
                                            ) {\
                                                TableCell(entry.month, 85, fontWeight = FontWeight.Bold)\
                                                TableCell("₹${"%.0f".format(entry.admissionFee)}", 80)\
                                                TableCell("₹${"%.0f".format(entry.tuitionFee)}", 75)\
                                                TableCell("₹${"%.0f".format(entry.gameFee)}", 70)\
                                                TableCell("₹${"%.0f".format(entry.examFee)}", 70)\
                                                TableCell("₹${"%.0f".format(entry.transportFee)}", 80)\
                                                TableCell("₹${"%.0f".format(entry.lateFee)}", 80, color = Color(0xFFDC2626))\
                                                TableCell("-₹${"%.0f".format(entry.concession)}", 80, color = Color(0xFFD97706))\
                                                TableCell("₹${"%.0f".format(entry.arrear)}", 80, color = Color(0xFFDC2626))\
                                                TableCell("₹${"%.0f".format(entry.totalPayable)}", 100, fontWeight = FontWeight.ExtraBold, color = MaterialTheme.colorScheme.primary)\
                                                TableCell("₹${"%.0f".format(entry.paidAmount)}", 100, fontWeight = FontWeight.Bold, color = Color(0xFF10B981))\
                                                TableCell("₹${"%.0f".format(entry.balance)}", 100, fontWeight = FontWeight.Bold, color = Color(0xFFEF4444))\
                                                TableCell(entry.paymentDate.ifBlank { "-" }, 80)\
                                                TableCell(entry.receiptNo.ifBlank { "-" }, 110)\
                                                Box(modifier = Modifier.width(110.dp), contentAlignment = Alignment.Center) {\
                                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {\
                                                        if (!isReadOnly && !isPaid) {\
                                                            IconButton(\
                                                                onClick = { selectedEntryForEdit = entry },\
                                                                modifier = Modifier.size(24.dp).background(MaterialTheme.colorScheme.primaryContainer, CircleShape)\
                                                            ) {\
                                                                Icon(Icons.Filled.Edit, "Edit entry", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(14.dp))\
                                                            }\
                                                        }\
                                                        if (entry.paidAmount > 0) {\
                                                            IconButton(\
                                                                onClick = { selectedEntryForReceipt = entry },\
                                                                modifier = Modifier.size(24.dp).background(Color(0xFFD1FAE5), CircleShape)\
                                                            ) {\
                                                                Icon(Icons.Filled.Receipt, "Print PDF receipt", tint = Color(0xFF10B981), modifier = Modifier.size(14.dp))\
                                                            }\
                                                        }\
                                                    }\
                                                }\
                                            }\
                                        }\
                                        val sumAdmission = calculatedLedger.sumOf { it.admissionFee }\
                                        val sumTuition = calculatedLedger.sumOf { it.tuitionFee }\
                                        val sumGame = calculatedLedger.sumOf { it.gameFee }\
                                        val sumExam = calculatedLedger.sumOf { it.examFee }\
                                        val sumTransport = calculatedLedger.sumOf { it.transportFee }\
                                        val sumLate = calculatedLedger.sumOf { it.lateFee }\
                                        val sumConcession = calculatedLedger.sumOf { it.concession }\
                                        val sumPayable = calculatedLedger.sumOf { it.totalPayable }\
                                        val sumPaid = calculatedLedger.sumOf { it.paidAmount }\
                                        val sumBalance = calculatedLedger.sumOf { it.balance }\
                                        Row(\
                                            modifier = Modifier\
                                                .background(MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f))\
                                                .padding(vertical = 10.dp)\
                                        ) {\
                                            TableCell("GRAND TOTAL", 85, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)\
                                            TableCell("₹${sumAdmission.toInt()}", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("₹${sumTuition.toInt()}", 75, fontWeight = FontWeight.Bold)\
                                            TableCell("₹${sumGame.toInt()}", 70, fontWeight = FontWeight.Bold)\
                                            TableCell("₹${sumExam.toInt()}", 70, fontWeight = FontWeight.Bold)\
                                            TableCell("₹${sumTransport.toInt()}", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("₹${sumLate.toInt()}", 80, fontWeight = FontWeight.Bold, color = Color(0xFFDC2626))\
                                            TableCell("-₹${sumConcession.toInt()}", 80, fontWeight = FontWeight.Bold, color = Color(0xFFD97706))\
                                            TableCell("-", 80, fontWeight = FontWeight.Bold)\
                                            TableCell("₹${sumPayable.toInt()}", 100, fontWeight = FontWeight.ExtraBold, color = MaterialTheme.colorScheme.primary)\
                                            TableCell("₹${sumPaid.toInt()}", 100, fontWeight = FontWeight.ExtraBold, color = Color(0xFF10B981))\
                                            TableCell("₹${sumBalance.toInt()}", 100, fontWeight = FontWeight.ExtraBold, color = Color(0xFFEF4444))\
                                            TableCell("-", 80)\
                                            TableCell("VERIFIED", 110, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.secondary)\
                                            TableCell("-", 110)\
                                        }\
                                    }\
                                }\
                            }\
                        }\
                    }\
                }\
                1 -> {' app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt
