import sys

content = """package com.example.ui.screens

import androidx.activity.compose.BackHandler
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
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
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

@Composable
fun ChatScreen(viewModel: SchoolViewModel) {
    val chatsMessages by viewModel.chatsState.collectAsStateWithLifecycle()
    val activeChatRecipientId by viewModel.activeChatUserId.collectAsStateWithLifecycle()
    val teachers by viewModel.teachersState.collectAsStateWithLifecycle()
    val students by viewModel.studentsState.collectAsStateWithLifecycle()
    val users by viewModel.usersState.collectAsStateWithLifecycle()
    val currentUser by viewModel.currentUser.collectAsStateWithLifecycle()

    var isConversationOpen by rememberSaveable { mutableStateOf(false) }

    BackHandler(enabled = isConversationOpen) {
        isConversationOpen = false
        viewModel.setActiveChatRecipient("")
    }

    // Process recent chats
    val recentChats by remember(chatsMessages, currentUser, teachers, students, users) {
        derivedStateOf {
            val myId = currentUser?.userId ?: ""
            val grouped = chatsMessages.filter { it.senderId == myId || it.receiverId == myId }
                .groupBy { if (it.senderId == myId) it.receiverId else it.senderId }
                
            // Include some contacts even if no message exists for teachers/admins
            val combinedUsers = users.map { ChatContactInfo(it.userId, it.name, it.role, "https://ui-avatars.com/api/?name=${it.name}&background=random") }
            val combinedTeachers = teachers.map { ChatContactInfo(it.teacherId, it.name, "Teacher - ${it.subject}", it.profilePhotoUrl.ifBlank { "https://ui-avatars.com/api/?name=${it.name}&background=random" }) }
            val combinedStudents = students.map { ChatContactInfo(it.studentId, it.name, "Student - ${it.className}", it.profilePhotoUrl.ifBlank { "https://ui-avatars.com/api/?name=${it.name}&background=random" }) }
            
            val allContacts = (combinedUsers + combinedTeachers + combinedStudents).associateBy { it.id }
            
            val chatList = grouped.mapValues { entry -> 
                val lastMsg = entry.value.maxByOrNull { msg -> msg.timestamp }
                val unreadCount = entry.value.count { it.receiverId == myId && !it.isRead }
                val contact = allContacts[entry.key] ?: ChatContactInfo(entry.key, "Unknown User", "User", "")
                ChatListItem(contact, lastMsg, unreadCount)
            }.values.filter { it.lastMessage != null }.sortedByDescending { it.lastMessage?.timestamp ?: 0L }
            
            chatList.ifEmpty {
                allContacts.values.take(10).map { ChatListItem(it, null, 0) }
            }
        }
    }

    val activeContactInfo = remember(activeChatRecipientId, teachers, students, users) {
        val t = teachers.find { it.teacherId == activeChatRecipientId }
        val s = students.find { it.studentId == activeChatRecipientId }
        val u = users.find { it.userId == activeChatRecipientId }
        if (t != null) ChatContactInfo(t.teacherId, t.name, "Teacher - ${t.subject}", t.profilePhotoUrl)
        else if (s != null) ChatContactInfo(s.studentId, s.name, "Student - ${s.className}", s.profilePhotoUrl)
        else if (u != null) ChatContactInfo(u.userId, u.name, u.role, "")
        else ChatContactInfo(activeChatRecipientId ?: "", "Unknown User", "User", "")
    }

    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
        val isTablet = maxWidth > 600.dp
        
        if (isTablet) {
            Row(modifier = Modifier.fillMaxSize()) {
                Box(modifier = Modifier.weight(1f).fillMaxHeight()) {
                    ChatListScreen(
                        recentChats = recentChats,
                        currentUser = currentUser,
                        activeChatId = activeChatRecipientId ?: "",
                        onChatSelected = { id ->
                            viewModel.setActiveChatRecipient(id)
                            isConversationOpen = true
                        }
                    )
                }
                VerticalDivider()
                Box(modifier = Modifier.weight(2f).fillMaxHeight()) {
                    if (!activeChatRecipientId.isNullOrBlank()) {
                        ConversationScreen(
                            contactInfo = activeContactInfo,
                            chatsMessages = chatsMessages.filter { 
                                (it.senderId == currentUser?.userId && it.receiverId == activeChatRecipientId) || 
                                (it.senderId == activeChatRecipientId && it.receiverId == currentUser?.userId)
                            }.sortedByDescending { it.timestamp },
                            currentUser = currentUser,
                            onBack = { viewModel.setActiveChatRecipient("") },
                            onSendMessage = { msg -> viewModel.sendChatMessage(msg) },
                            isTablet = true
                        )
                    } else {
                        EmptyChatState()
                    }
                }
            }
        } else {
            AnimatedContent(
                targetState = isConversationOpen && !activeChatRecipientId.isNullOrBlank(),
                transitionSpec = {
                    if (targetState) {
                        slideInHorizontally { width -> width } + fadeIn() togetherWith slideOutHorizontally { width -> -width } + fadeOut()
                    } else {
                        slideInHorizontally { width -> -width } + fadeIn() togetherWith slideOutHorizontally { width -> width } + fadeOut()
                    }
                },
                label = "chat_transition"
            ) { isConversation ->
                if (isConversation) {
                    ConversationScreen(
                        contactInfo = activeContactInfo,
                        chatsMessages = chatsMessages.filter { 
                            (it.senderId == currentUser?.userId && it.receiverId == activeChatRecipientId) || 
                            (it.senderId == activeChatRecipientId && it.receiverId == currentUser?.userId)
                        }.sortedByDescending { it.timestamp },
                        currentUser = currentUser,
                        onBack = { 
                            isConversationOpen = false
                            viewModel.setActiveChatRecipient("")
                        },
                        onSendMessage = { msg -> viewModel.sendChatMessage(msg) },
                        isTablet = false
                    )
                } else {
                    ChatListScreen(
                        recentChats = recentChats,
                        currentUser = currentUser,
                        activeChatId = activeChatRecipientId ?: "",
                        onChatSelected = { id ->
                            viewModel.setActiveChatRecipient(id)
                            isConversationOpen = true
                        }
                    )
                }
            }
        }
    }
}

data class ChatContactInfo(val id: String, val name: String, val role: String, val photoUrl: String)
data class ChatListItem(val contact: ChatContactInfo, val lastMessage: ChatMessage?, val unreadCount: Int)

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun ChatListScreen(
    recentChats: List<ChatListItem>,
    currentUser: User?,
    activeChatId: String,
    onChatSelected: (String) -> Unit
) {
    var searchQuery by rememberSaveable { mutableStateOf("") }
    val haptic = LocalHapticFeedback.current
    var isLoading by remember { mutableStateOf(true) }
    
    LaunchedEffect(Unit) {
        delay(600)
        isLoading = false
    }

    val filteredChats by remember(recentChats, searchQuery) {
        derivedStateOf {
            if (searchQuery.isBlank()) recentChats
            else recentChats.filter { it.contact.name.contains(searchQuery, ignoreCase = true) }
        }
    }

    Scaffold(
        topBar = {
            Column {
                LargeTopAppBar(
                    title = { Text("Messages", fontWeight = FontWeight.ExtraBold) },
                    colors = TopAppBarDefaults.largeTopAppBarColors(
                        containerColor = MaterialTheme.colorScheme.surface,
                    )
                )
                SearchBar(
                    query = searchQuery,
                    onQueryChange = { searchQuery = it },
                    onSearch = { },
                    active = false,
                    onActiveChange = { },
                    placeholder = { Text("Search messages...") },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)
                ) {}
            }
        }
    ) { padding ->
        if (isLoading) {
            ChatListShimmer(padding)
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentPadding = PaddingValues(bottom = 88.dp)
            ) {
                items(filteredChats, key = { it.contact.id }) { item ->
                    Box(modifier = Modifier.animateItem(placementSpec = spring(stiffness = Spring.StiffnessMediumLow))) {
                        ChatListRow(
                            item = item,
                            isSelected = item.contact.id == activeChatId,
                            onClick = { 
                                haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                                onChatSelected(item.contact.id) 
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun ChatListRow(item: ChatListItem, isSelected: Boolean, onClick: () -> Unit) {
    var showMenu by remember { mutableStateOf(false) }
    
    val bgColor by animateColorAsState(
        if (isSelected) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f)
        else MaterialTheme.colorScheme.surface, label = "bg_color"
    )

    Surface(
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick)
            .pointerInput(Unit) { detectTapGestures(onLongPress = { showMenu = true }, onTap = { onClick() }) },
        color = bgColor
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(contentAlignment = Alignment.BottomEnd) {
                AsyncImage(
                    model = item.contact.photoUrl.ifBlank { "https://ui-avatars.com/api/?name=${item.contact.name.replace(" ", "+")}&background=random" },
                    contentDescription = null,
                    modifier = Modifier.size(56.dp).clip(CircleShape),
                    contentScale = ContentScale.Crop
                )
                Box(
                    modifier = Modifier.size(14.dp).clip(CircleShape)
                        .background(Color(0xFF10B981)).border(2.dp, MaterialTheme.colorScheme.surface, CircleShape)
                )
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(item.contact.name, fontWeight = FontWeight.Bold, fontSize = 16.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    val timeStr = if (item.lastMessage != null) {
                        SimpleDateFormat("hh:mm a", Locale.ENGLISH).format(Date(item.lastMessage.timestamp))
                    } else ""
                    Text(timeStr, fontSize = 12.sp, color = if (item.unreadCount > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Spacer(modifier = Modifier.height(4.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = item.lastMessage?.message ?: "Start a conversation",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 14.sp,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        fontWeight = if (item.unreadCount > 0) FontWeight.Bold else FontWeight.Normal,
                        modifier = Modifier.weight(1f)
                    )
                    if (item.unreadCount > 0) {
                        Badge(containerColor = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(start = 8.dp)) {
                            Text(item.unreadCount.toString(), color = MaterialTheme.colorScheme.onPrimary)
                        }
                    }
                }
            }
            
            DropdownMenu(expanded = showMenu, onDismissRequest = { showMenu = false }) {
                DropdownMenuItem(text = { Text("Pin Chat") }, onClick = { showMenu = false })
                DropdownMenuItem(text = { Text("Mute Notifications") }, onClick = { showMenu = false })
                DropdownMenuItem(text = { Text("Archive") }, onClick = { showMenu = false })
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun ConversationScreen(
    contactInfo: ChatContactInfo,
    chatsMessages: List<ChatMessage>,
    currentUser: User?,
    onBack: () -> Unit,
    onSendMessage: (String) -> Unit,
    isTablet: Boolean
) {
    val haptic = LocalHapticFeedback.current
    val listState = rememberLazyListState()
    var messageText by rememberSaveable { mutableStateOf("") }
    
    val scrollBehavior = TopAppBarDefaults.pinnedScrollBehavior(rememberTopAppBarState())
    
    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        AsyncImage(
                            model = contactInfo.photoUrl.ifBlank { "https://ui-avatars.com/api/?name=${contactInfo.name.replace(" ", "+")}&background=random" },
                            contentDescription = null,
                            modifier = Modifier.size(40.dp).clip(CircleShape)
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(contactInfo.name, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Text(contactInfo.role, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                },
                navigationIcon = {
                    if (!isTablet) {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    }
                },
                actions = {
                    IconButton(onClick = { }) { Icon(Icons.Default.Call, contentDescription = "Call") }
                    IconButton(onClick = { }) { Icon(Icons.Default.MoreVert, contentDescription = "More") }
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f),
                )
            )
        },
        bottomBar = {
            MessageComposer(
                text = messageText,
                onTextChange = { messageText = it },
                onSend = {
                    if (messageText.isNotBlank()) {
                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                        onSendMessage(messageText)
                        messageText = ""
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize().padding(padding),
            reverseLayout = true,
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
        ) {
            items(chatsMessages, key = { it.messageId }) { msg ->
                val isMe = msg.senderId == currentUser?.userId
                Box(modifier = Modifier.animateItem(placementSpec = spring(stiffness = Spring.StiffnessMediumLow))) {
                    MessageBubble(message = msg, isMe = isMe)
                }
            }
        }
    }
}

@Composable
fun MessageBubble(message: ChatMessage, isMe: Boolean) {
    val df = SimpleDateFormat("hh:mm a", Locale.ENGLISH)
    val timeString = df.format(Date(message.timestamp))
    
    val shape = if (isMe) {
        RoundedCornerShape(20.dp, 20.dp, 4.dp, 20.dp)
    } else {
        RoundedCornerShape(20.dp, 20.dp, 20.dp, 4.dp)
    }

    val bgColor = if (isMe) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
    val textColor = if (isMe) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant

    Column(
        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
        horizontalAlignment = if (isMe) Alignment.End else Alignment.Start
    ) {
        Surface(
            shape = shape,
            color = bgColor,
            shadowElevation = 1.dp,
            modifier = Modifier.widthIn(max = 280.dp)
        ) {
            Column(modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp)) {
                Text(message.message, color = textColor, fontSize = 15.sp, lineHeight = 20.sp)
                Spacer(modifier = Modifier.height(4.dp))
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.End, modifier = Modifier.align(Alignment.End)) {
                    Text(timeString, color = textColor.copy(alpha = 0.7f), fontSize = 10.sp)
                    if (isMe) {
                        Spacer(modifier = Modifier.width(4.dp))
                        Icon(
                            imageVector = if (message.isRead) Icons.Default.DoneAll else Icons.Default.Check,
                            contentDescription = null,
                            modifier = Modifier.size(14.dp),
                            tint = if (message.isRead) Color(0xFF60A5FA) else textColor.copy(alpha = 0.7f)
                        )
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MessageComposer(text: String, onTextChange: (String) -> Unit, onSend: () -> Unit) {
    Surface(
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 3.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 8.dp).navigationBarsPadding(),
            verticalAlignment = Alignment.Bottom
        ) {
            IconButton(onClick = { }) {
                Icon(Icons.Default.AddCircleOutline, contentDescription = "Attach", tint = MaterialTheme.colorScheme.primary)
            }
            OutlinedTextField(
                value = text,
                onValueChange = onTextChange,
                modifier = Modifier.weight(1f).padding(horizontal = 4.dp),
                placeholder = { Text("Message...") },
                shape = RoundedCornerShape(24.dp),
                colors = TextFieldDefaults.outlinedTextFieldColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                    unfocusedBorderColor = Color.Transparent,
                    focusedBorderColor = MaterialTheme.colorScheme.primary
                ),
                maxLines = 4,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                keyboardActions = KeyboardActions(onSend = { onSend() })
            )
            val isEnabled = text.isNotBlank()
            val buttonColor by animateColorAsState(if (isEnabled) MaterialTheme.colorScheme.primary else Color.Gray)
            
            IconButton(
                onClick = onSend,
                enabled = isEnabled,
                modifier = Modifier.padding(start = 4.dp)
            ) {
                Box(
                    modifier = Modifier.size(40.dp).clip(CircleShape).background(buttonColor),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(20.dp))
                }
            }
        }
    }
}

@Composable
fun EmptyChatState() {
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(Icons.Outlined.Chat, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.LightGray)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Select a conversation to start messaging", color = Color.Gray)
        }
    }
}

@Composable
fun ChatListShimmer(padding: PaddingValues) {
    val transition = rememberInfiniteTransition(label = "shimmer")
    val alpha by transition.animateFloat(
        initialValue = 0.3f, targetValue = 0.7f,
        animationSpec = infiniteRepeatable(animation = tween(1000, easing = LinearEasing), repeatMode = RepeatMode.Reverse),
        label = "shimmer_alpha"
    )
    val color = Color.LightGray.copy(alpha = alpha)

    Column(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        repeat(6) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(56.dp).clip(CircleShape).background(color))
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Box(modifier = Modifier.fillMaxWidth(0.5f).height(16.dp).clip(RoundedCornerShape(8.dp)).background(color))
                    Spacer(modifier = Modifier.height(8.dp))
                    Box(modifier = Modifier.fillMaxWidth(0.8f).height(12.dp).clip(RoundedCornerShape(6.dp)).background(color))
                }
            }
        }
    }
}

"""
with open("app/src/main/java/com/example/ui/screens/ChatScreens.kt", "w") as f:
    f.write(content)
