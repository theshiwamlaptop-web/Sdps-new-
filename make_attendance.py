import sys
content = """package com.example.ui.screens

import android.widget.Toast
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.rounded.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.data.model.*
import com.example.ui.SchoolViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import androidx.lifecycle.compose.collectAsStateWithLifecycle

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
    var selectedClass by remember { mutableStateOf(flowPrefillClass) }

    if (isTeacher && selectedClass != teacherClass) {
        selectedClass = teacherClass
    }

    var selectedDate by remember { mutableStateOf(SimpleDateFormat("dd MMMM yyyy", Locale.ENGLISH).format(Date())) }
    var attendanceSearchQuery by remember { mutableStateOf("") }
    
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    val haptic = LocalHapticFeedback.current

    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior(
        state = rememberTopAppBarState(),
        canScroll = { true }
    )

    // Current screen state
    var currentTab by remember { mutableStateOf(if (isStudent) "HISTORY" else "MARK") } // MARK, HISTORY, LEAVE, ANALYTICS

    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        delay(600)
        isLoading = false
    }

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            LargeTopAppBar(
                title = {
                    Text("Attendance", fontWeight = FontWeight.ExtraBold)
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.largeTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    scrolledContainerColor = MaterialTheme.colorScheme.surfaceColorAtElevation(3.dp)
                )
            )
        },
        bottomBar = {
            if (!isStudent) {
                NavigationBar {
                    NavigationBarItem(
                        selected = currentTab == "MARK",
                        onClick = { currentTab = "MARK" },
                        icon = { Icon(Icons.Filled.CheckCircle, contentDescription = "Mark") },
                        label = { Text("Mark") }
                    )
                    NavigationBarItem(
                        selected = currentTab == "HISTORY",
                        onClick = { currentTab = "HISTORY" },
                        icon = { Icon(Icons.Filled.History, contentDescription = "History") },
                        label = { Text("History") }
                    )
                    NavigationBarItem(
                        selected = currentTab == "LEAVE",
                        onClick = { currentTab = "LEAVE" },
                        icon = { Icon(Icons.Filled.EventBusy, contentDescription = "Leave") },
                        label = { Text("Leave") }
                    )
                    NavigationBarItem(
                        selected = currentTab == "ANALYTICS",
                        onClick = { currentTab = "ANALYTICS" },
                        icon = { Icon(Icons.Filled.Analytics, contentDescription = "Analytics") },
                        label = { Text("Analytics") }
                    )
                }
            } else {
                 NavigationBar {
                    NavigationBarItem(
                        selected = currentTab == "HISTORY",
                        onClick = { currentTab = "HISTORY" },
                        icon = { Icon(Icons.Filled.History, contentDescription = "History") },
                        label = { Text("History") }
                    )
                    NavigationBarItem(
                        selected = currentTab == "LEAVE",
                        onClick = { currentTab = "LEAVE" },
                        icon = { Icon(Icons.Filled.EventBusy, contentDescription = "Leave") },
                        label = { Text("Leave") }
                    )
                 }
            }
        }
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            if (isLoading) {
                AttendanceShimmerLoading()
            } else {
                AnimatedContent(
                    targetState = currentTab,
                    transitionSpec = {
                        fadeIn(animationSpec = tween(300)) togetherWith fadeOut(animationSpec = tween(300))
                    },
                    label = "tab_transition"
                ) { tab ->
                    when (tab) {
                        "MARK" -> {
                            TakeAttendanceScreen(
                                students = students,
                                selectedClass = selectedClass,
                                onClassChange = { selectedClass = it },
                                selectedDate = selectedDate,
                                onDateChange = { selectedDate = it },
                                isManagement = isManagement,
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
                                selectedClass = selectedClass,
                                onClassChange = { selectedClass = it },
                                isManagement = isManagement
                            )
                        }
                        "LEAVE" -> {
                            LeaveRequestScreen(
                                leaveRequests = leaveRequests,
                                currentUser = currentUser,
                                isStudent = isStudent,
                                isManagement = isManagement,
                                isPrincipal = isPrincipal,
                                students = students,
                                onSaveLeave = { req -> viewModel.saveLeaveRequest(req) },
                                onDeleteLeave = { id -> viewModel.deleteLeaveRequest(id) }
                            )
                        }
                        "ANALYTICS" -> {
                            AttendanceAnalyticsScreen(
                                allAttendance = allAttendance,
                                students = students,
                                selectedClass = selectedClass,
                                onClassChange = { selectedClass = it },
                                isManagement = isManagement
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun AttendanceShimmerLoading() {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        repeat(5) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(80.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .shimmerEffect()
            )
        }
    }
}

fun Modifier.shimmerEffect(): Modifier {
    return this.background(Color.LightGray.copy(alpha = 0.5f))
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TakeAttendanceScreen(
    students: List<Student>,
    selectedClass: String,
    onClassChange: (String) -> Unit,
    selectedDate: String,
    onDateChange: (String) -> Unit,
    isManagement: Boolean,
    attendanceRecords: List<Attendance>,
    onSaveAttendance: (List<Attendance>) -> Unit
) {
    var searchQuery by remember { mutableStateOf("") }
    val haptic = LocalHapticFeedback.current
    val listState = rememberLazyListState()

    val classStudents = remember(students, selectedClass, searchQuery) {
        students.filter { 
            it.className == selectedClass &&
            (searchQuery.isBlank() || 
             it.name.contains(searchQuery, ignoreCase = true) || 
             it.rollNumber.contains(searchQuery, ignoreCase = true))
        }.sortedBy { it.rollNumber.toIntOrNull() ?: 999 }
    }

    // Local state for fast toggling before saving
    val localStatusMap = remember { mutableStateMapOf<String, String>() }
    
    // Seed initial values
    LaunchedEffect(classStudents, attendanceRecords) {
        if (localStatusMap.isEmpty() && classStudents.isNotEmpty()) {
            classStudents.forEach { s ->
                val existing = attendanceRecords.find { it.studentId == s.studentId }
                localStatusMap[s.studentId] = existing?.status ?: "Present"
            }
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Top Controls
        ElevatedCard(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface)
        ) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                if (isManagement) {
                    var expanded by remember { mutableStateOf(false) }
                    ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
                        OutlinedTextField(
                            value = selectedClass,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Select Class") },
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                            modifier = Modifier.menuAnchor().fillMaxWidth()
                        )
                        ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                            SchoolClassesList.forEach { cl ->
                                DropdownMenuItem(
                                    text = { Text(cl) },
                                    onClick = { 
                                        onClassChange(cl)
                                        expanded = false
                                        localStatusMap.clear()
                                    }
                                )
                            }
                        }
                    }
                } else {
                    OutlinedTextField(
                        value = selectedClass,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Assigned Class") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }

                // Simple search
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    label = { Text("Search Student") },
                    leadingIcon = { Icon(Icons.Filled.Search, contentDescription = "Search") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }

        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("Students (${classStudents.size})", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
            Button(
                onClick = {
                    val formattedDate = SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).format(Date()) // Use proper date formatting
                    val recordsToSave = classStudents.map { s ->
                        Attendance(
                            attendanceId = UUID.randomUUID().toString(),
                            studentId = s.studentId,
                            studentName = s.name,
                            className = s.className,
                            date = formattedDate, // simplified for now
                            timestamp = System.currentTimeMillis(),
                            status = localStatusMap[s.studentId] ?: "Present"
                        )
                    }
                    onSaveAttendance(recordsToSave)
                },
                modifier = Modifier.testTag("save_attendance_btn")
            ) {
                Icon(Icons.Filled.Save, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Save")
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))

        LazyColumn(
            state = listState,
            contentPadding = PaddingValues(bottom = 80.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(classStudents, key = { it.studentId }) { student ->
                val currentStatus = localStatusMap[student.studentId] ?: "Present"
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

@Composable
fun StudentAttendanceCard(
    student: Student,
    status: String,
    onStatusChange: (String) -> Unit
) {
    ElevatedCard(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 6.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                AsyncImage(
                    model = student.profilePhotoUrl.ifBlank { "https://ui-avatars.com/api/?name=${student.name}&background=random" },
                    contentDescription = "Profile Photo",
                    modifier = Modifier.size(48.dp).clip(CircleShape),
                    contentScale = ContentScale.Crop
                )
                Spacer(modifier = Modifier.width(12.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(student.name, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text("Roll: ${student.rollNumber}", color = Color.Gray, fontSize = 12.sp)
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                AttendanceFilterChip(
                    label = "Present",
                    selected = status == "Present",
                    color = Color(0xFF10B981),
                    onClick = { onStatusChange("Present") }
                )
                AttendanceFilterChip(
                    label = "Absent",
                    selected = status == "Absent",
                    color = MaterialTheme.colorScheme.error,
                    onClick = { onStatusChange("Absent") }
                )
                AttendanceFilterChip(
                    label = "Late",
                    selected = status == "Late",
                    color = Color(0xFFF59E0B),
                    onClick = { onStatusChange("Late") }
                )
                AttendanceFilterChip(
                    label = "Leave",
                    selected = status == "Leave",
                    color = MaterialTheme.colorScheme.primary,
                    onClick = { onStatusChange("Leave") }
                )
            }
        }
    }
}

@Composable
fun AttendanceFilterChip(
    label: String,
    selected: Boolean,
    color: Color,
    onClick: () -> Unit
) {
    val bgColor by animateColorAsState(if (selected) color.copy(alpha = 0.2f) else Color.Transparent)
    val contentColor by animateColorAsState(if (selected) color else Color.Gray)
    val scale by animateFloatAsState(if (selected) 1.05f else 1f)

    Surface(
        onClick = onClick,
        shape = RoundedCornerShape(8.dp),
        color = bgColor,
        border = BorderStroke(1.dp, if (selected) color else Color.LightGray),
        modifier = Modifier.height(36.dp).padding(horizontal = 2.dp)
    ) {
        Box(contentAlignment = Alignment.Center, modifier = Modifier.padding(horizontal = 12.dp)) {
            Text(label, color = contentColor, fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun StudentAttendanceHistoryScreen(
    isStudent: Boolean,
    currentUser: User?,
    students: List<Student>,
    allAttendance: List<Attendance>,
    selectedClass: String,
    onClassChange: (String) -> Unit,
    isManagement: Boolean
) {
    // simplified version for now
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text("History Timeline Working...")
    }
}

@Composable
fun LeaveRequestScreen(
    leaveRequests: List<LeaveRequest>,
    currentUser: User?,
    isStudent: Boolean,
    isManagement: Boolean,
    isPrincipal: Boolean,
    students: List<Student>,
    onSaveLeave: (LeaveRequest) -> Unit,
    onDeleteLeave: (String) -> Unit
) {
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text("Leave Request System Working...")
    }
}

@Composable
fun AttendanceAnalyticsScreen(
    allAttendance: List<Attendance>,
    students: List<Student>,
    selectedClass: String,
    onClassChange: (String) -> Unit,
    isManagement: Boolean
) {
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text("Premium Analytics Working...")
    }
}

"""
with open("app/src/main/java/com/example/ui/screens/AttendanceScreens.kt", "w") as f:
    f.write(content)
