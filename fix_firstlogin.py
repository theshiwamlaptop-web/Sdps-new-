import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

# Replace FirstLoginPasswordChangeDialog
content = content.replace("var newPassword by remember { mutableStateOf(\"\") }", "var oldPassword by remember { mutableStateOf(\"\") }\n    var newPassword by remember { mutableStateOf(\"\") }")

old_pass_ui = """                    OutlinedTextField(
                        value = oldPassword,
                        onValueChange = { oldPassword = it },
                        label = { Text("Current Password") },
                        visualTransformation = PasswordVisualTransformation(),
                        singleLine = true,
                        modifier = Modifier
                            .fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = newPassword,"""
content = content.replace("                    OutlinedTextField(\n                        value = newPassword,", old_pass_ui)

content = content.replace("viewModel.changePassword(\n                                    userId = userId,\n                                    newPassword = trimmedNew,", 
                          "viewModel.changePassword(\n                                    userId = userId,\n                                    oldPassword = oldPassword,\n                                    newPassword = trimmedNew,")

content = content.replace("viewModel.changePassword(\n                                userId = userId,\n                                newPassword = trimmedNew,",
                          "viewModel.changePassword(\n                                userId = userId,\n                                oldPassword = oldPassword,\n                                newPassword = trimmedNew,")

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    settings = f.read()

settings = settings.replace(
    "viewModel.changePassword(\n                                userId = currentUser.userId,\n                                newPassword = newPass",
    "viewModel.changePassword(\n                                userId = currentUser.userId,\n                                oldPassword = null,\n                                newPassword = newPass"
)
settings = settings.replace(
    "viewModel.changePassword(\n                                                    userId = userToReset.userId,\n                                                    newPassword = newPass",
    "viewModel.changePassword(\n                                                    userId = userToReset.userId,\n                                                    oldPassword = null,\n                                                    newPassword = newPass"
)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(settings)

print("Done fixing UI")
