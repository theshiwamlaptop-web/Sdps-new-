with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

start_marker = "// 12. SCHOOL CALENDAR EVENTS & HOLIDAYS"
end_marker = "// EXTRA FEATURE COMPONENT PLATES"

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

if start_pos != -1 and end_pos != -1:
    new_code = """// 12. SCHOOL CALENDAR EVENTS & HOLIDAYS
// ==========================================
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SchoolCalendarScreen(viewModel: SchoolViewModel) {
    val events by viewModel.calendarEvents.collectAsState()
    val currentUser by viewModel.currentUser.collectAsState()
    val role = currentUser?.role?.uppercase()?.trim() ?: ""
    val isManagement = role == "PRINCIPAL" || role == "ADMIN" || role == "HEAD_ADMIN"

    // Calendar state
    val todayCalendar = remember { Calendar.getInstance() }
    val todayDateStr = remember { SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).format(todayCalendar.time) }

    var displayedMonth by rememberSaveable { mutableStateOf(Calendar.getInstance()) }
    var selectedDate by rememberSaveable { mutableStateOf(todayDateStr) }
    var selectedCategoryFilter by rememberSaveable { mutableStateOf("All") }
    var showOnlySelectedDateEvents by rememberSaveable { mutableStateOf(false) }

    // Dialog state for Add/Edit event
    var showAddEditDialog by remember { mutableStateOf(false) }
    var editingEvent by remember { mutableStateOf<CalendarEvent?>(null) }

    // Delete confirmation dialog state
    var eventToDelete by remember { mutableStateOf<CalendarEvent?>(null) }

    // Helper formatting
    val monthYearFormat = remember { SimpleDateFormat("MMMM yyyy", Locale.ENGLISH) }
    val dayMonthYearFormat = remember { SimpleDateFormat("dd MMM yyyy", Locale.ENGLISH) }
    val currentMonthStr = remember(displayedMonth) { SimpleDateFormat("yyyy-MM", Locale.ENGLISH).format(displayedMonth.time) }

    // Events filtered for current month or selected date
    val monthEvents = remember(events, currentMonthStr) {
        events.filter { it.date.startsWith(currentMonthStr) }
    }

    val filteredEvents = remember(events, selectedDate, selectedCategoryFilter, showOnlySelectedDateEvents, currentMonthStr) {
        events.filter { ev ->
            val dateMatches = if (showOnlySelectedDateEvents) ev.date == selectedDate else ev.date.startsWith(currentMonthStr)
            val categoryMatches = if (selectedCategoryFilter == "All") true else ev.type.equals(selectedCategoryFilter, ignoreCase = true)
            dateMatches && categoryMatches
        }.sortedWith(compareBy({ it.date }, { it.time }))
    }

    Scaffold(
        topBar = {},
        floatingActionButton = {
            if (isManagement) {
                FloatingActionButton(
                    onClick = {
                        editingEvent = null
                        showAddEditDialog = true
                    },
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary,
                    modifier = Modifier.testTag("add_calendar_event_fab")
                ) {
                    Icon(Icons.Filled.Add, contentDescription = "Add Calendar Event")
                }
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(innerPadding)
                .padding(16.dp)
        ) {
            // Header Title Card
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "School Calendar & Agenda",
                        style = MaterialTheme.typography.headlineSmall.copy(fontWeight = FontWeight.Bold),
                        color = MaterialTheme.colorScheme.onBackground
                    )
                    Text(
                        text = "Holidays, exams, deadlines & academic schedules",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                if (isManagement) {
                    Button(
                        onClick = {
                            editingEvent = null
                            showAddEditDialog = true
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primaryContainer, contentColor = MaterialTheme.colorScheme.onPrimaryContainer),
                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(Icons.Filled.Add, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Add Event", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Month Navigation Card
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    // Month & Year Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(onClick = {
                            displayedMonth = (displayedMonth.clone() as Calendar).apply { add(Calendar.MONTH, -1) }
                        }) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Previous Month")
                        }

                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = monthYearFormat.format(displayedMonth.time),
                                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            AssistChip(
                                onClick = {
                                    displayedMonth = Calendar.getInstance()
                                    selectedDate = todayDateStr
                                },
                                label = { Text("Today", fontSize = 11.sp, fontWeight = FontWeight.SemiBold) },
                                leadingIcon = { Icon(Icons.Filled.Today, contentDescription = null, modifier = Modifier.size(14.dp)) },
                                shape = RoundedCornerShape(8.dp)
                            )
                        }

                        IconButton(onClick = {
                            displayedMonth = (displayedMonth.clone() as Calendar).apply { add(Calendar.MONTH, 1) }
                        }) {
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Next Month")
                        }
                    }

                    Spacer(modifier = Modifier.height(8.dp))

                    // Calendar Day Header (Sun..Sat)
                    val dayNames = listOf("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceAround
                    ) {
                        dayNames.forEach { dayName ->
                            Text(
                                text = dayName,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.weight(1f),
                                textAlign = TextAlign.Center
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(6.dp))

                    // Calendar Month Days Grid
                    val daysInMonth = displayedMonth.getActualMaximum(Calendar.DAY_OF_MONTH)
                    val firstDayOfWeek = (displayedMonth.clone() as Calendar).apply { set(Calendar.DAY_OF_MONTH, 1) }.get(Calendar.DAY_OF_WEEK) // 1 = Sunday

                    var dayCounter = 1
                    for (row in 0..5) {
                        if (dayCounter > daysInMonth) break
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceAround
                        ) {
                            for (col in 0..6) {
                                if ((row == 0 && col < firstDayOfWeek - 1) || dayCounter > daysInMonth) {
                                    Box(modifier = Modifier.weight(1f).aspectRatio(1.1f))
                                } else {
                                    val currentDay = dayCounter
                                    val cellDateCal = (displayedMonth.clone() as Calendar).apply { set(Calendar.DAY_OF_MONTH, currentDay) }
                                    val cellDateStr = SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).format(cellDateCal.time)
                                    val isSelected = cellDateStr == selectedDate
                                    val isToday = cellDateStr == todayDateStr
                                    
                                    val eventsOnDate = monthEvents.filter { it.date == cellDateStr }
                                    val hasEvent = eventsOnDate.isNotEmpty()
                                    val hasHoliday = eventsOnDate.any { it.type.equals("Holiday", ignoreCase = true) }
                                    val hasExam = eventsOnDate.any { it.type.equals("Exam", ignoreCase = true) }

                                    Box(
                                        modifier = Modifier
                                            .weight(1f)
                                            .aspectRatio(1.1f)
                                            .padding(2.dp)
                                            .clip(RoundedCornerShape(8.dp))
                                            .background(
                                                when {
                                                    isSelected -> MaterialTheme.colorScheme.primary
                                                    isToday -> MaterialTheme.colorScheme.primaryContainer
                                                    else -> Color.Transparent
                                                }
                                            )
                                            .border(
                                                width = if (isToday && !isSelected) 1.5.dp else 0.dp,
                                                color = if (isToday && !isSelected) MaterialTheme.colorScheme.primary else Color.Transparent,
                                                shape = RoundedCornerShape(8.dp)
                                            )
                                            .clickable {
                                                selectedDate = cellDateStr
                                                showOnlySelectedDateEvents = true
                                            },
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Column(
                                            horizontalAlignment = Alignment.CenterHorizontally,
                                            verticalArrangement = Arrangement.Center
                                        ) {
                                            Text(
                                                text = currentDay.toString(),
                                                fontSize = 12.sp,
                                                fontWeight = if (isSelected || isToday) FontWeight.ExtraBold else FontWeight.Normal,
                                                color = when {
                                                    isSelected -> MaterialTheme.colorScheme.onPrimary
                                                    isToday -> MaterialTheme.colorScheme.onPrimaryContainer
                                                    else -> MaterialTheme.colorScheme.onSurface
                                                }
                                            )
                                            if (hasEvent) {
                                                Row(
                                                    horizontalArrangement = Arrangement.Center,
                                                    verticalAlignment = Alignment.CenterVertically,
                                                    modifier = Modifier.padding(top = 2.dp)
                                                ) {
                                                    val dotColor = when {
                                                        hasHoliday -> Color(0xFFEF4444)
                                                        hasExam -> Color(0xFFF59E0B)
                                                        else -> Color(0xFF10B981)
                                                    }
                                                    Box(
                                                        modifier = Modifier
                                                            .size(5.dp)
                                                            .clip(CircleShape)
                                                            .background(if (isSelected) MaterialTheme.colorScheme.onPrimary else dotColor)
                                                    )
                                                }
                                            }
                                        }
                                    }
                                    dayCounter++
                                }
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Category Filter Row
            LazyRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                val categories = listOf("All", "Holiday", "Exam", "School Event", "Fee Deadline", "Meeting", "Activity")
                items(categories) { category ->
                    FilterChip(
                        selected = selectedCategoryFilter == category,
                        onClick = { selectedCategoryFilter = category },
                        label = { Text(category, fontSize = 12.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary,
                            selectedLabelColor = MaterialTheme.colorScheme.onPrimary
                        )
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Events List Header
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                val headerText = if (showOnlySelectedDateEvents) {
                    try {
                        val parsed = SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).parse(selectedDate)
                        if (parsed != null) "Events on ${dayMonthYearFormat.format(parsed)}" else "Events on $selectedDate"
                    } catch (e: Exception) {
                        "Events on $selectedDate"
                    }
                } else {
                    "All Agenda for ${monthYearFormat.format(displayedMonth.time)}"
                }

                Text(
                    text = headerText,
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onBackground
                )

                if (showOnlySelectedDateEvents) {
                    TextButton(onClick = { showOnlySelectedDateEvents = false }) {
                        Text("Show Full Month", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Events List
            if (filteredEvents.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f))
                        .padding(24.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            imageVector = Icons.Filled.EventAvailable,
                            contentDescription = null,
                            modifier = Modifier.size(48.dp),
                            tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f)
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = if (showOnlySelectedDateEvents) "No events scheduled for $selectedDate" else "No events found for this filter in ${monthYearFormat.format(displayedMonth.time)}",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            textAlign = TextAlign.Center
                        )
                        if (isManagement) {
                            Spacer(modifier = Modifier.height(12.dp))
                            OutlinedButton(
                                onClick = {
                                    editingEvent = null
                                    showAddEditDialog = true
                                },
                                shape = RoundedCornerShape(10.dp)
                            ) {
                                Icon(Icons.Filled.Add, contentDescription = null, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("Add Event for Date")
                            }
                        }
                    }
                }
            } else {
                LazyColumn(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    items(filteredEvents, key = { it.id }) { ev ->
                        val categoryColor = when (ev.type.lowercase()) {
                            "holiday" -> Color(0xFFEF4444)
                            "exam" -> Color(0xFFF59E0B)
                            "school event" -> Color(0xFF10B981)
                            "fee deadline" -> Color(0xFF8B5CF6)
                            "meeting" -> Color(0xFF3B82F6)
                            "activity" -> Color(0xFFEC4899)
                            else -> MaterialTheme.colorScheme.primary
                        }

                        ElevatedCard(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(14.dp),
                            colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface)
                        ) {
                            Column(modifier = Modifier.padding(14.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(
                                            modifier = Modifier
                                                .clip(RoundedCornerShape(8.dp))
                                                .background(categoryColor.copy(alpha = 0.15f))
                                                .padding(horizontal = 8.dp, vertical = 4.dp)
                                        ) {
                                            Text(
                                                text = ev.type,
                                                fontSize = 11.sp,
                                                fontWeight = FontWeight.Bold,
                                                color = categoryColor
                                            )
                                        }
                                        if (ev.time.isNotBlank()) {
                                            Spacer(modifier = Modifier.width(8.dp))
                                            Text(
                                                text = ev.time,
                                                fontSize = 11.sp,
                                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                                fontWeight = FontWeight.Medium
                                            )
                                        }
                                    }

                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Text(
                                            text = ev.date,
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.SemiBold,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant
                                        )

                                        if (isManagement) {
                                            Spacer(modifier = Modifier.width(4.dp))
                                            IconButton(
                                                onClick = {
                                                    editingEvent = ev
                                                    showAddEditDialog = true
                                                },
                                                modifier = Modifier.size(28.dp)
                                            ) {
                                                Icon(Icons.Filled.Edit, contentDescription = "Edit Event", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                                            }
                                            IconButton(
                                                onClick = { eventToDelete = ev },
                                                modifier = Modifier.size(28.dp)
                                            ) {
                                                Icon(Icons.Filled.Delete, contentDescription = "Delete Event", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.error)
                                            }
                                        }
                                    }
                                }

                                Spacer(modifier = Modifier.height(8.dp))

                                Text(
                                    text = ev.title,
                                    style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold),
                                    color = MaterialTheme.colorScheme.onSurface
                                )

                                if (ev.description.isNotBlank()) {
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = ev.description,
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }

                                Spacer(modifier = Modifier.height(8.dp))

                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = "Audience: ${ev.targetClass}",
                                        fontSize = 10.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    if (ev.createdBy.isNotBlank()) {
                                        Text(
                                            text = "By: ${ev.createdBy}",
                                            fontSize = 10.sp,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Add/Edit Event Dialog
    if (showAddEditDialog) {
        var titleInput by remember { mutableStateOf(editingEvent?.title ?: "") }
        var descInput by remember { mutableStateOf(editingEvent?.description ?: "") }
        var dateInput by remember { mutableStateOf(editingEvent?.date ?: selectedDate) }
        var timeInput by remember { mutableStateOf(editingEvent?.time ?: "All Day") }
        var typeInput by remember { mutableStateOf(editingEvent?.type ?: "School Event") }
        var targetClassInput by remember { mutableStateOf(editingEvent?.targetClass ?: "All") }

        val typeOptions = listOf("School Event", "Holiday", "Exam", "Fee Deadline", "Meeting", "Activity", "Other")

        AlertDialog(
            onDismissRequest = { showAddEditDialog = false },
            title = {
                Text(if (editingEvent == null) "Create Calendar Event" else "Edit Calendar Event")
            },
            text = {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState()),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    OutlinedTextField(
                        value = titleInput,
                        onValueChange = { titleInput = it },
                        label = { Text("Event Title *") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )

                    OutlinedTextField(
                        value = descInput,
                        onValueChange = { descInput = it },
                        label = { Text("Description") },
                        modifier = Modifier.fillMaxWidth(),
                        maxLines = 3
                    )

                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = dateInput,
                            onValueChange = { dateInput = it },
                            label = { Text("Date (yyyy-MM-dd)") },
                            modifier = Modifier.weight(1f),
                            singleLine = true
                        )
                        OutlinedTextField(
                            value = timeInput,
                            onValueChange = { timeInput = it },
                            label = { Text("Time (e.g. 09:00 AM)") },
                            modifier = Modifier.weight(1f),
                            singleLine = true
                        )
                    }

                    Text("Category:", style = MaterialTheme.typography.labelMedium)
                    LazyRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        items(typeOptions) { option ->
                            FilterChip(
                                selected = typeInput.equals(option, ignoreCase = true),
                                onClick = { typeInput = option },
                                label = { Text(option, fontSize = 11.sp) }
                            )
                        }
                    }

                    OutlinedTextField(
                        value = targetClassInput,
                        onValueChange = { targetClassInput = it },
                        label = { Text("Target Class (e.g. All, Class 10)") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        val eventToSave = CalendarEvent(
                            id = editingEvent?.id ?: "",
                            date = dateInput.trim(),
                            title = titleInput.trim(),
                            description = descInput.trim(),
                            type = typeInput.trim(),
                            time = timeInput.trim(),
                            targetClass = targetClassInput.trim().ifEmpty { "All" },
                            createdBy = editingEvent?.createdBy ?: (currentUser?.name ?: "Management"),
                            createdAt = editingEvent?.createdAt ?: System.currentTimeMillis()
                        )
                        viewModel.saveCalendarEvent(eventToSave)
                        showAddEditDialog = false
                    },
                    enabled = titleInput.isNotBlank() && dateInput.isNotBlank()
                ) {
                    Text("Save Event")
                }
            },
            dismissButton = {
                TextButton(onClick = { showAddEditDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    // Delete Confirmation Dialog
    if (eventToDelete != null) {
        AlertDialog(
            onDismissRequest = { eventToDelete = null },
            title = { Text("Delete Event") },
            text = { Text("Are you sure you want to delete '${eventToDelete?.title}'? This action cannot be undone.") },
            confirmButton = {
                Button(
                    onClick = {
                        eventToDelete?.let { viewModel.deleteCalendarEvent(it.id) }
                        eventToDelete = null
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                ) {
                    Text("Delete")
                }
            },
            dismissButton = {
                TextButton(onClick = { eventToDelete = null }) {
                    Text("Cancel")
                }
            }
        )
    }
}

"""
    content = content[:start_pos] + new_code + content[end_pos:]
    with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
        f.write(content)
    print("SchoolCalendarScreen replaced successfully!")
else:
    print(f"Markers not found: start={start_pos}, end={end_pos}")
