import sys

with open("app/src/main/java/com/example/data/model/Models.kt", "r") as f:
    content = f.read()

old_model = """data class ChatMessage(
    @PrimaryKey val messageId: String = "",
    val senderId: String = "",
    val receiverId: String = "",
    val message: String = "",
    val timestamp: Long = 0L
)"""

new_model = """data class ChatMessage(
    @PrimaryKey val messageId: String = "",
    val senderId: String = "",
    val receiverId: String = "",
    val message: String = "",
    val timestamp: Long = 0L,
    val isRead: Boolean = false,
    val isDelivered: Boolean = false,
    val attachmentType: String = "" // "image", "pdf", "homework", "notice", ""
)"""

if old_model in content:
    content = content.replace(old_model, new_model)
    with open("app/src/main/java/com/example/data/model/Models.kt", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find the old model")

