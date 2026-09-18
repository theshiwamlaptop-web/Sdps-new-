import re

with open("app/src/main/java/com/example/data/model/Models.kt", "r") as f:
    content = f.read()

content = content.replace(
"""@Entity(tableName = "chats")
data class ChatMessage(
    @PrimaryKey val messageId: String = "",
    val senderId: String = "",
    val receiverId: String = "",
    val message: String = "",
    val timestamp: Long = 0L,
    val isRead: Boolean = false,
    val isDelivered: Boolean = false,
    val attachmentType: String = "" // "image", "pdf", "homework", "notice", ""
)""",
"""@Entity(tableName = "chats")
data class ChatMessage(
    @PrimaryKey val messageId: String = "",
    val senderId: String = "",
    val receiverId: String = "",
    val message: String = "",
    val timestamp: Long = 0L,
    val isRead: Boolean = false,
    val isDelivered: Boolean = false,
    val attachmentType: String = "", // "image", "pdf", "homework", "notice", ""
    val status: String = "sent", // "pending", "sent", "delivered", "read"
    val replyToMessageId: String = "",
    val reactions: String = ""
)""")

with open("app/src/main/java/com/example/data/model/Models.kt", "w") as f:
    f.write(content)
