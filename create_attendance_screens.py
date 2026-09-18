import sys
content = """package com.example.ui.screens

import android.widget.Toast
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.rounded.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.example.data.model.*
import com.example.ui.SchoolViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AttendanceManagementScreen(viewModel: SchoolViewModel) {
    val students by viewModel.studentsState.collectAsStateWithLifecycle()
    val allAttendance by viewModel.attendanceState.collectAsStateWithLifecycle()
    val attendanceRecords by viewModel.currentClassAttendance.collectAsStateWithLifecycle()
    val leaveRequests by viewModel.leaveRequestsState.collectAsStateWithLifecycle()

    val currentUser by viewModel.currentUser.collectAsStateWithLifecycle()
    val roleStr = currentUser?.role?.uppercase()?.trim() ?: ""
    val isStudent = roleStr == "STUDENT"
    val isTeacher = roleStr == "TEACHER" || roleStr == "CLASS_TEACHER"
    val isManagement = roleStr == "ADMIN" || roleStr == "HEAD_ADMIN" || roleStr == "PRINCIPAL"
    val isPrincipal = roleStr == "PRINCIPAL"

    val teacherClass = getTeacherAssignedClass(viewModel)
    val flowPrefillClass by viewModel.selectedClassForAttendance.collectAsStateWithLifecycle()
    var selectedClass by rememberSaveable { mutableStateOf(flowPrefillClass) }

    if (isTeacher && selectedClass != teacherClass) {
        selectedClass = teacherClass
    }

    var selectedDate by rememberSaveable { mutableStateOf(SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).format(Date())) }
    
    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior(
        state = rememberTopAppBarState(),
        snapAnimationSpec = spring(stiffness = Spring.StiffnessMediumLow),
        flingAnimationSpec = decayAnimationSpec()
    )

    var currentTab by rememberSaveable { mutableStateOf(if (isStudent) "HISTORY" else "MARK") } 

    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        delay(800)
        isLoading = false
    }

    val context = LocalContext.current
    val haptic = LocalHapticFeedback.current

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            LargeTopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Rounded.School,
                            contentDescription = null,
                            modifier = Modifier.size(32.dp).padding(end = 8.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                        Column {
                            Text("Attendance", fontWeight = FontWeight.ExtraBold)
                            Text(
                                text = SimpleDateFormat("EEEE, dd MMM yyyy", Locale.ENGLISH).format(SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).parse(selectedDate) ?: Date()),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                },
                actions = {
                    if (isManagement || isTeacher) {
                        var expanded by remember { mutableStateOf(false) }
                        TextButton(onClick = { expanded = true }) {
                            Text(selectedClass, fontWeight = FontWeight.Bold)
                            Icon(Icons.Default.ArrowDropDown, contentDescription = null)
                        }
                        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                            SchoolClassesList.forEach { cl ->
                                DropdownMenuItem(
                                    text = { Text(cl) },
                                    onClick = { 
                                        selectedClass = cl
                                        expanded = false
                                    }
                                )
                            }
                        }
                    }
                    IconButton(onClick = { /* Profile actions */ }) {
                        AsyncImage(
                            model = "https://ui-avatars.com/api/?name=${currentUser?.name}&background=random",
                            contentDescription = "Profile",
                            modifier = Modifier.size(32.dp).clip(CircleShape)
                        )
                    }
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.largeTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    scrolledContainerColor = MaterialTheme.colorScheme.surfaceColorAtElevation(3.dp)
                )
            )
        },
        bottomBar = {
            NavigationBar {
                if (!isStudent) {
                    NavigationBarItem(
                        selected = currentTab == "MARK",
                        onClick = { currentTab = "MARK"; haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove) },
                        icon = { Icon(if (currentTab == "MARK") Icons.Filled.CheckCircle else Icons.Outlined.CheckCircleOutline, contentDescription = "Mark") },
                        label = { Text("Mark") },
                        alwaysShowLabel = false
                    )
                }
                NavigationBarItem(
                    selected = currentTab == "HISTORY",
                    onClick = { currentTab = "HISTORY"; haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove) },
                    icon = { Icon(if (currentTab == "HISTORY") Icons.Filled.History else Icons.Outlined.History, contentDescription = "History") },
                    label = { Text("History") },
                    alwaysShowLabel = false
                )
                NavigationBarItem(
                    selected = currentTab == "LEAVE",
                    onClick = { currentTab = "LEAVE"; haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove) },
                    icon = { Icon(if (currentTab == "LEAVE") Icons.Filled.EventBusy else Icons.Outlined.EventBusy, contentDescription = "Leave") },
                    label = { Text("Leave") },
                    alwaysShowLabel = false
                )
                if (!isStudent) {
                    NavigationBarItem(
                        selected = currentTab == "ANALYTICS",
                        onClick = { currentTab = "ANALYTICS"; haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove) },
                        icon = { Icon(if (currentTab == "ANALYTICS") Icons.Filled.Analytics else Icons.Outlined.Analytics, contentDescription = "Analytics") },
                        label = { Text("Analytics") },
                        alwaysShowLabel = false
                    )
                }
            }
        }
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            if (isLoading) {
                AttendanceShimmerLoading(currentTab)
            } else {
                AnimatedContent(
                    targetState = currentTab,
                    transitionSpec = {
                        (fadeIn(animationSpec = tween(220, delayMillis = 90)) +
                                scaleIn(initialScale = 0.92f, animationSpec = tween(220, delayMillis = 90)))
                            .togetherWith(fadeOut(animationSpec = tween(90)))
                    },
                    label = "tab_transition"
                ) { tab ->
                    when (tab) {
                        "MARK" -> {
                            TakeAttendanceScreen(
                                students = students,
                                selectedClass = selectedClass,
                                selectedDate = selectedDate,
                                attendanceRecords = attendanceRecords,
                                onSaveAttendance = { records ->
                                    viewModel.saveAttendance(records)
                                    haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                    Toast.makeText(context, "Attendance Marked", Toast.LENGTH_SHORT).show()
                                }
                            )
                        }
                        "HISTORY" -> {
                            StudentAttendanceHistoryScreen(
                                isStudent = isStudent,
                                currentUser = currentUser,
                                students = students,
                                allAttendance = allAttendance,
                                selectedClass = selectedClass
                            )
                        }
                        "LEAVE" -> {
                            LeaveRequestScreen(
                                leaveRequests = leaveRequests,
                                currentUser = currentUser,
                                isStudent = isStudent,
                                isPrincipal = isPrincipal,
                                isManagement = isManagement,
                                students = students,
                                onSaveLeave = { req -> 
                                    viewModel.saveLeaveRequest(req)
                                    haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                },
                                onDeleteLeave = { id -> viewModel.deleteLeaveRequest(id) }
                            )
                        }
                        "ANALYTICS" -> {
                            AttendanceAnalyticsScreen(
                                allAttendance = allAttendance,
                                students = students,
                                selectedClass = selectedClass
                            )
                        }
                    }
                }
            }
        }
    }
}

fun decayAnimationSpec() = androidx.compose.animation.core.exponentialDecay<Float>()

@Composable
fun AttendanceShimmerLoading(tab: String) {
    val transition = rememberInfiniteTransition(label = "shimmer")
    val alpha by transition.animateFloat(
        initialValue = 0.3f,
        targetValue = 0.7f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "shimmer_alpha"
    )
    val color = Color.LightGray.copy(alpha = alpha)

    Column(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        if (tab == "MARK" || tab == "HISTORY") {
            Box(modifier = Modifier.fillMaxWidth().height(56.dp).clip(RoundedCornerShape(28.dp)).background(color))
            repeat(6) {
                Box(modifier = Modifier.fillMaxWidth().height(84.dp).clip(RoundedCornerShape(16.dp)).background(color))
            }
        } else if (tab == "ANALYTICS") {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Box(modifier = Modifier.weight(1f).height(120.dp).clip(RoundedCornerShape(16.dp)).background(color))
                Box(modifier = Modifier.weight(1f).height(120.dp).clip(RoundedCornerShape(16.dp)).background(color))
            }
            Box(modifier = Modifier.fillMaxWidth().height(200.dp).clip(RoundedCornerShape(16.dp)).background(color))
            Box(modifier = Modifier.fillMaxWidth().height(200.dp).clip(RoundedCornerShape(16.dp)).background(color))
        } else {
            repeat(4) {
                Box(modifier = Modifier.fillMaxWidth().height(120.dp).clip(RoundedCornerShape(16.dp)).background(color))
            }
        }
    }
}

// ---------------------------------------------------------------------------
// MARK ATTENDANCE
// ---------------------------------------------------------------------------

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun TakeAttendanceScreen(
    students: List<Student>,
    selectedClass: String,
    selectedDate: String,
    attendanceRecords: List<Attendance>,
    onSaveAttendance: (List<Attendance>) -> Unit
) {
    var searchQuery by rememberSaveable { mutableStateOf("") }
    var activeSearch by rememberSaveable { mutableStateOf(false) }
    val haptic = LocalHapticFeedback.current
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()

    val debouncedSearch = remember { mutableStateOf(searchQuery) }
    LaunchedEffect(searchQuery) {
        delay(300)
        debouncedSearch.value = searchQuery
    }

    val classStudents by remember(students, selectedClass, debouncedSearch.value) {
        derivedStateOf {
            students.filter { 
                it.className == selectedClass &&
                (debouncedSearch.value.isBlank() || 
                 it.name.contains(debouncedSearch.value, ignoreCase = true) || 
                 it.rollNo.contains(debouncedSearch.value, ignoreCase = true))
            }.sortedBy { it.rollNo.toIntOrNull() ?: 999 }
        }
    }

    val localStatusMap = remember { mutableStateMapOf<String, String>() }
    
    LaunchedEffect(classStudents, attendanceRecords) {
        if (classStudents.isNotEmpty()) {
            classStudents.forEach { s ->
                if (!localStatusMap.containsKey(s.studentId)) {
                    val existing = attendanceRecords.find { it.studentId == s.studentId }
                    localStatusMap[s.studentId] = existing?.status ?: "Present"
                }
            }
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        SearchBar(
            query = searchQuery,
            onQueryChange = { searchQuery = it },
            onSearch = { activeSearch = false },
            active = activeSearch,
            onActiveChange = { activeSearch = it },
            placeholder = { Text("Search by name or roll...") },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
            trailingIcon = {
                if (activeSearch || searchQuery.isNotEmpty()) {
                    IconButton(onClick = { searchQuery = ""; activeSearch = false }) {
                        Icon(Icons.Default.Close, contentDescription = "Clear")
                    }
                }
            },
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)
        ) {
            // Can add search history here
        }

        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                "Students (${classStudents.size})",
                fontWeight = FontWeight.Bold,
                style = MaterialTheme.typography.titleMedium
            )
            FilledTonalButton(
                onClick = {
                    val recordsToSave = classStudents.map { s ->
                        Attendance(
                            attendanceId = UUID.randomUUID().toString(),
                            studentId = s.studentId,
                            studentName = s.name,
                            className = s.className,
                            date = selectedDate,
                            timestamp = System.currentTimeMillis(),
                            status = localStatusMap[s.studentId] ?: "Present"
                        )
                    }
                    onSaveAttendance(recordsToSave)
                }
            ) {
                Icon(Icons.Default.Save, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Save All")
            }
        }
        
        LazyColumn(
            state = listState,
            contentPadding = PaddingValues(bottom = 88.dp, top = 8.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(classStudents, key = { it.studentId }) { student ->
                val currentStatus = localStatusMap[student.studentId] ?: "Present"
                Box(modifier = Modifier.animateItem(
                    fadeInSpec = null, fadeOutSpec = null, placementSpec = spring(stiffness = Spring.StiffnessMediumLow)
                )) {
                    StudentAttendanceCard(
                        student = student,
                        status = currentStatus,
                        onStatusChange = { newStatus ->
                            if (localStatusMap[student.studentId] != newStatus) {
                                localStatusMap[student.studentId] = newStatus
                                haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                            }
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun StudentAttendanceCard(
    student: Student,
    status: String,
    onStatusChange: (String) -> Unit
) {
    var showMenu by remember { mutableStateOf(false) }
    
    val backgroundColor by animateColorAsState(
        when (status) {
            "Present" -> Color(0xFFE8F5E9)
            "Absent" -> Color(0xFFFFEBEE)
            "Leave" -> Color(0xFFE3F2FD)
            "Late" -> Color(0xFFFFF8E1)
            else -> MaterialTheme.colorScheme.surface
        }, label = "bg_color"
    )

    ElevatedCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp)
            .pointerInput(Unit) {
                detectTapGestures(
                    onLongPress = { showMenu = true }
                )
            },
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.elevatedCardColors(containerColor = backgroundColor)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                AsyncImage(
                    model = "https://ui-avatars.com/api/?name=${student.name.replace(" ", "+")}&background=random",
                    contentDescription = "Profile Photo",
                    modifier = Modifier.size(48.dp).clip(CircleShape),
                    contentScale = ContentScale.Crop
                )
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(student.name, fontWeight = FontWeight.Bold, fontSize = 16.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("Roll: ${student.rollNo}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                }
                
                // Extra Badges could go here (e.g. Transport, Fee Due)
                if (student.fatherName == "FeeDue") {
                    Badge(containerColor = MaterialTheme.colorScheme.error) { Text("Fee Due") }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                AttendanceChip("Present", status == "Present", Color(0xFF10B981)) { onStatusChange("Present") }
                AttendanceChip("Absent", status == "Absent", Color(0xFFEF4444)) { onStatusChange("Absent") }
                AttendanceChip("Late", status == "Late", Color(0xFFF59E0B)) { onStatusChange("Late") }
                AttendanceChip("Leave", status == "Leave", Color(0xFF3B82F6)) { onStatusChange("Leave") }
            }

            DropdownMenu(expanded = showMenu, onDismissRequest = { showMenu = false }) {
                DropdownMenuItem(text = { Text("View Profile") }, onClick = { showMenu = false })
                DropdownMenuItem(text = { Text("Call Parent") }, onClick = { showMenu = false })
                DropdownMenuItem(text = { Text("Message Student") }, onClick = { showMenu = false })
            }
        }
    }
}

@Composable
fun AttendanceChip(label: String, selected: Boolean, activeColor: Color, onClick: () -> Unit) {
    val scale by animateFloatAsState(if (selected) 1.05f else 1f, spring(dampingRatio = Spring.DampingRatioMediumBouncy), label = "scale")
    
    FilterChip(
        selected = selected,
        onClick = onClick,
        label = { Text(label, fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal) },
        colors = FilterChipDefaults.filterChipColors(
            selectedContainerColor = activeColor,
            selectedLabelColor = Color.White
        ),
        border = FilterChipDefaults.filterChipBorder(
            enabled = true,
            selected = selected,
            borderColor = activeColor,
            selectedBorderColor = activeColor
        ),
        modifier = Modifier.scale(scale)
    )
}

// ---------------------------------------------------------------------------
// HISTORY / CALENDAR
// ---------------------------------------------------------------------------

@Composable
fun StudentAttendanceHistoryScreen(
    isStudent: Boolean,
    currentUser: User?,
    students: List<Student>,
    allAttendance: List<Attendance>,
    selectedClass: String
) {
    val context = LocalContext.current
    var currentMonth by rememberSaveable { mutableStateOf(Calendar.getInstance()) }
    
    val targetStudent = if (isStudent) {
        students.find { it.studentId == currentUser?.userId }
    } else {
        students.find { it.className == selectedClass } // just pick first for demo
    }

    if (targetStudent == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("No student data available", color = Color.Gray)
        }
        return
    }

    val studentAttendance by remember(allAttendance, targetStudent, currentMonth) {
        derivedStateOf {
            val format = SimpleDateFormat("yyyy-MM", Locale.ENGLISH)
            val monthStr = format.format(currentMonth.time)
            allAttendance.filter { it.studentId == targetStudent.studentId && it.date.startsWith(monthStr) }
        }
    }

    Column(modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
        if (!isStudent) {
            Text("Showing for: ${targetStudent.name}", modifier = Modifier.padding(16.dp), fontWeight = FontWeight.Bold)
        }

        // Calendar Header
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = { 
                currentMonth = (currentMonth.clone() as Calendar).apply { add(Calendar.MONTH, -1) }
            }) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Previous")
            }
            AnimatedContent(
                targetState = currentMonth,
                transitionSpec = {
                    if (targetState.after(initialState)) {
                        slideInHorizontally { width -> width } + fadeIn() togetherWith slideOutHorizontally { width -> -width } + fadeOut()
                    } else {
                        slideInHorizontally { width -> -width } + fadeIn() togetherWith slideOutHorizontally { width -> width } + fadeOut()
                    }
                }, label = "month_anim"
            ) { month ->
                Text(
                    SimpleDateFormat("MMMM yyyy", Locale.ENGLISH).format(month.time),
                    fontWeight = FontWeight.Bold,
                    fontSize = 18.sp
                )
            }
            IconButton(onClick = { 
                currentMonth = (currentMonth.clone() as Calendar).apply { add(Calendar.MONTH, 1) }
            }) {
                Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Next")
            }
        }

        MonthlyCalendarGrid(currentMonth, studentAttendance)
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Monthly Summary
        AttendanceSummaryCard(studentAttendance)
    }
}

@Composable
fun MonthlyCalendarGrid(month: Calendar, records: List<Attendance>) {
    val daysInMonth = month.getActualMaximum(Calendar.DAY_OF_MONTH)
    val firstDayOfWeek = (month.clone() as Calendar).apply { set(Calendar.DAY_OF_MONTH, 1) }.get(Calendar.DAY_OF_WEEK)
    
    val days = listOf("S", "M", "T", "W", "T", "F", "S")
    
    ElevatedCard(
        modifier = Modifier.fillMaxWidth().padding(16.dp),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) {
                days.forEach { day ->
                    Text(day, fontWeight = FontWeight.Bold, color = Color.Gray, modifier = Modifier.weight(1f), textAlign = TextAlign.Center)
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
            
            var dayCounter = 1
            for (row in 0..5) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) {
                    for (col in 0..6) {
                        if (row == 0 && col < firstDayOfWeek - 1 || dayCounter > daysInMonth) {
                            Box(modifier = Modifier.weight(1f).aspectRatio(1f))
                        } else {
                            val currentDay = dayCounter
                            val dateStr = SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).format((month.clone() as Calendar).apply { set(Calendar.DAY_OF_MONTH, currentDay) }.time)
                            val record = records.find { it.date == dateStr }
                            
                            val bgColor = when (record?.status) {
                                "Present" -> Color(0xFF10B981)
                                "Absent" -> Color(0xFFEF4444)
                                "Late" -> Color(0xFFF59E0B)
                                "Leave" -> Color(0xFF3B82F6)
                                else -> Color.Transparent
                            }
                            val textColor = if (bgColor != Color.Transparent) Color.White else MaterialTheme.colorScheme.onSurface
                            
                            Box(
                                modifier = Modifier
                                    .weight(1f)
                                    .aspectRatio(1f)
                                    .padding(4.dp)
                                    .clip(CircleShape)
                                    .background(bgColor),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(currentDay.toString(), color = textColor, fontSize = 14.sp)
                            }
                            dayCounter++
                        }
                    }
                }
                if (dayCounter > daysInMonth) break
            }
        }
    }
}

@Composable
fun AttendanceSummaryCard(records: List<Attendance>) {
    val present = records.count { it.status == "Present" }
    val absent = records.count { it.status == "Absent" }
    val late = records.count { it.status == "Late" }
    val leave = records.count { it.status == "Leave" }
    
    val total = records.size
    val percentage = if (total > 0) (present.toFloat() / total) * 100 else 0f
    
    val animatedPercent by animateFloatAsState(targetValue = percentage, animationSpec = tween(1000, easing = FastOutSlowInEasing), label = "percent")

    ElevatedCard(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Monthly Summary", fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Spacer(modifier = Modifier.height(16.dp))
            Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Box(contentAlignment = Alignment.Center, modifier = Modifier.size(80.dp)) {
                    CircularProgressIndicator(
                        progress = { 1f },
                        modifier = Modifier.fillMaxSize(),
                        color = Color.LightGray.copy(alpha = 0.3f),
                        strokeWidth = 8.dp,
                        strokeCap = StrokeCap.Round,
                    )
                    CircularProgressIndicator(
                        progress = { animatedPercent / 100f },
                        modifier = Modifier.fillMaxSize(),
                        color = MaterialTheme.colorScheme.primary,
                        strokeWidth = 8.dp,
                        strokeCap = StrokeCap.Round,
                    )
                    Text("${animatedPercent.toInt()}%", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                }
                Spacer(modifier = Modifier.width(24.dp))
                Column {
                    SummaryRow("Present", present, Color(0xFF10B981))
                    SummaryRow("Absent", absent, Color(0xFFEF4444))
                    SummaryRow("Late", late, Color(0xFFF59E0B))
                    SummaryRow("Leave", leave, Color(0xFF3B82F6))
                }
            }
        }
    }
}

@Composable
fun SummaryRow(label: String, count: Int, color: Color) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 2.dp)) {
        Box(modifier = Modifier.size(12.dp).clip(CircleShape).background(color))
        Spacer(modifier = Modifier.width(8.dp))
        Text(label, fontSize = 14.sp, modifier = Modifier.width(60.dp))
        Text(count.toString(), fontWeight = FontWeight.Bold, fontSize = 14.sp)
    }
}

// ---------------------------------------------------------------------------
// LEAVE REQUESTS
// ---------------------------------------------------------------------------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LeaveRequestScreen(
    leaveRequests: List<LeaveRequest>,
    currentUser: User?,
    isStudent: Boolean,
    isPrincipal: Boolean,
    isManagement: Boolean,
    students: List<Student>,
    onSaveLeave: (LeaveRequest) -> Unit,
    onDeleteLeave: (String) -> Unit
) {
    var showApplySheet by rememberSaveable { mutableStateOf(false) }
    
    val myLeaves by remember(leaveRequests, currentUser) {
        derivedStateOf {
            if (isStudent) leaveRequests.filter { it.studentId == currentUser?.userId }.sortedByDescending { it.timestamp }
            else leaveRequests.sortedByDescending { it.timestamp }
        }
    }

    Scaffold(
        floatingActionButton = {
            if (isStudent) {
                FloatingActionButton(onClick = { showApplySheet = true }) {
                    Icon(Icons.Default.Add, contentDescription = "Apply Leave")
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (myLeaves.isEmpty()) {
                item {
                    Text("No leave requests found.", color = Color.Gray, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Center)
                }
            }
            items(myLeaves, key = { it.requestId }) { req ->
                LeaveRequestCard(
                    request = req,
                    isManagement = isManagement || isPrincipal,
                    onStatusChange = { newStatus ->
                        onSaveLeave(req.copy(status = newStatus, reviewedBy = currentUser?.name ?: "Admin"))
                    }
                )
            }
        }
    }

    if (showApplySheet && isStudent) {
        val me = students.find { it.studentId == currentUser?.userId }
        if (me != null) {
            ApplyLeaveBottomSheet(
                student = me,
                onDismiss = { showApplySheet = false },
                onSubmit = { req ->
                    onSaveLeave(req)
                    showApplySheet = false
                }
            )
        }
    }
}

@Composable
fun LeaveRequestCard(request: LeaveRequest, isManagement: Boolean, onStatusChange: (String) -> Unit) {
    ElevatedCard(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(request.studentName, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                val statusColor = when(request.status) {
                    "Approved" -> Color(0xFF10B981)
                    "Rejected" -> Color(0xFFEF4444)
                    else -> Color(0xFFF59E0B)
                }
                Surface(color = statusColor.copy(alpha = 0.2f), shape = RoundedCornerShape(8.dp)) {
                    Text(request.status, color = statusColor, modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text("Date: ${request.startDate} to ${request.endDate}", fontSize = 14.sp)
            Text("Reason: ${request.reason}", fontSize = 14.sp, color = Color.Gray)
            
            if (isManagement && request.status == "Pending") {
                Spacer(modifier = Modifier.height(12.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                    TextButton(onClick = { onStatusChange("Rejected") }, colors = ButtonDefaults.textButtonColors(contentColor = Color.Red)) {
                        Text("Reject")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(onClick = { onStatusChange("Approved") }, colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981))) {
                        Text("Approve")
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ApplyLeaveBottomSheet(student: Student, onDismiss: () -> Unit, onSubmit: (LeaveRequest) -> Unit) {
    var startDate by remember { mutableStateOf("") }
    var endDate by remember { mutableStateOf("") }
    var reason by remember { mutableStateOf("") }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(modifier = Modifier.padding(16.dp).padding(bottom = 32.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Apply for Leave", fontWeight = FontWeight.Bold, fontSize = 20.sp)
            OutlinedTextField(value = startDate, onValueChange = { startDate = it }, label = { Text("Start Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())
            OutlinedTextField(value = endDate, onValueChange = { endDate = it }, label = { Text("End Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())
            OutlinedTextField(value = reason, onValueChange = { reason = it }, label = { Text("Reason") }, modifier = Modifier.fillMaxWidth(), minLines = 3)
            
            Button(
                onClick = {
                    if (startDate.isNotBlank() && reason.isNotBlank()) {
                        onSubmit(LeaveRequest(
                            requestId = UUID.randomUUID().toString(),
                            studentId = student.studentId,
                            studentName = student.name,
                            className = student.className,
                            startDate = startDate,
                            endDate = endDate.ifBlank { startDate },
                            reason = reason,
                            status = "Pending",
                            timestamp = System.currentTimeMillis()
                        ))
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Submit Request")
            }
        }
    }
}

// ---------------------------------------------------------------------------
// ANALYTICS
// ---------------------------------------------------------------------------

@Composable
fun AttendanceAnalyticsScreen(
    allAttendance: List<Attendance>,
    students: List<Student>,
    selectedClass: String
) {
    val classAttendance by remember(allAttendance, selectedClass) {
        derivedStateOf { allAttendance.filter { it.className == selectedClass } }
    }

    val present = classAttendance.count { it.status == "Present" }
    val absent = classAttendance.count { it.status == "Absent" }
    val late = classAttendance.count { it.status == "Late" }
    val total = classAttendance.size

    val attendanceRate = if (total > 0) (present.toFloat() / total) * 100 else 0f

    Column(modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Text("Class Analytics: $selectedClass", fontWeight = FontWeight.Bold, fontSize = 18.sp)
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            AnalyticsStatCard("Attendance Rate", "${"%.1f".format(attendanceRate)}%", Color(0xFF10B981), Modifier.weight(1f))
            AnalyticsStatCard("Total Records", total.toString(), MaterialTheme.colorScheme.primary, Modifier.weight(1f))
        }

        ElevatedCard(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp)) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Status Distribution", fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                
                val max = maxOf(present, absent, late, 1)
                
                DistributionBar("Present", present, max, Color(0xFF10B981))
                DistributionBar("Absent", absent, max, Color(0xFFEF4444))
                DistributionBar("Late", late, max, Color(0xFFF59E0B))
            }
        }
        
        // Add more premium charts here using canvas if needed, simplified for brevity
    }
}

@Composable
fun AnalyticsStatCard(title: String, value: String, color: Color, modifier: Modifier = Modifier) {
    ElevatedCard(modifier = modifier, shape = RoundedCornerShape(16.dp)) {
        Column(modifier = Modifier.padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(title, fontSize = 14.sp, color = Color.Gray)
            Spacer(modifier = Modifier.height(8.dp))
            Text(value, fontWeight = FontWeight.Bold, fontSize = 24.sp, color = color)
        }
    }
}

@Composable
fun DistributionBar(label: String, value: Int, max: Int, color: Color) {
    val animatedProgress by animateFloatAsState(targetValue = value.toFloat() / max, animationSpec = tween(1000), label = "bar_anim")
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 6.dp).fillMaxWidth()) {
        Text(label, modifier = Modifier.width(60.dp), fontSize = 12.sp)
        Box(modifier = Modifier.weight(1f).height(12.dp).clip(RoundedCornerShape(6.dp)).background(Color.LightGray.copy(alpha = 0.3f))) {
            Box(modifier = Modifier.fillMaxWidth(animatedProgress).fillMaxHeight().clip(RoundedCornerShape(6.dp)).background(color))
        }
        Text(value.toString(), modifier = Modifier.width(40.dp), textAlign = TextAlign.End, fontSize = 12.sp, fontWeight = FontWeight.Bold)
    }
}
"""
with open("app/src/main/java/com/example/ui/screens/AttendanceScreens.kt", "w") as f:
    f.write(content)
