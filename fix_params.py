import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "r") as f:
    content = f.read()

content = content.replace(
    "viewModel.changePassword(\n                            userId = userId,\n                            newPassword = newPassword,",
    "viewModel.changePassword(\n                            userId = userId,\n                            oldPassword = oldPassword,\n                            newPassword = newPassword,"
)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    settings = f.read()

settings = settings.replace(
    "viewModel.changePassword(\n                                user.userId,\n                                trimmedNew,",
    "viewModel.changePassword(\n                                user.userId,\n                                null,\n                                trimmedNew,"
)

settings = settings.replace(
    "viewModel.changePassword(\n                                                        usr.userId,\n                                                        \"temp123\",",
    "viewModel.changePassword(\n                                                        usr.userId,\n                                                        null,\n                                                        \"temp123\","
)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(settings)

print("Fixed parameters")
