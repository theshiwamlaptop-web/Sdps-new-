with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

text = text.replace("""                ) {
                    Text("Change")
                }
            ,""", """                ) {
                    Text("Change")
                }
            },""")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
