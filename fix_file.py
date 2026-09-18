with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

# First, undo my bad insertions from earlier
# I inserted `}\n        }` before line 458
# Let's just find `            }\n        }\n            }\n            // Contact details update`
text = text.replace("            }\n        }\n            }\n            // Contact details", "            }\n            }\n            // Contact details")

# The issue is that `item {` is followed by `ElevatedCard { ... }`.
# But `ElevatedCard` is closed with `            }` and then the next thing is either `//` or `item {`.
# We need an extra `            }` to close the `item {`.

# Let's replace the endings of these specific cards:

# 1. Contact details update (starts above)
# Ends before `            // Security key updates`
text = text.replace("                    }\n            }\n            // Security key updates", "                    }\n                }\n            }\n            // Security key updates")

# 2. Security key updates
# Ends before `            // Theme Preferences`
text = text.replace("                        }\n                    }\n            }\n            // Theme Preferences", "                        }\n                    }\n                }\n            }\n            // Theme Preferences")

# 3. Theme Preferences
# Ends before `            // Alert Toggles`
text = text.replace("                            }\n                        }\n                    }\n            }\n            // Alert Toggles", "                            }\n                        }\n                    }\n                }\n            }\n            // Alert Toggles")

# 4. Alert Toggles
# Ends before `        }\n        // Principal permanent deletion capability`
text = text.replace("                            }\n                        )\n                    }\n            }\n        }\n        // Principal permanent deletion", "                            }\n                        )\n                    }\n                }\n            }\n        }\n        // Principal permanent deletion")

# And for the Avatar one, it ends before `            // Contact details update`
text = text.replace("                            }\n                        }\n                    }\n            }\n            // Contact details", "                            }\n                        }\n                    }\n                }\n            }\n            // Contact details")

# Also, the missing brace inside `deleteUserAccount`:
# Currently:
#                                 if (idToDelete != user.userId) {
#                                     selectedUser = user
#                                 }
#                             } else {
#                                 Toast.makeText(context, "Deletions failed. Please try again.", Toast.LENGTH_SHORT).show()
#                             }
# This was fixed by my previous python script? Wait, I didn't fix this yet!
# Let's fix it now:
text = text.replace("""                                if (idToDelete != user.userId) {
                                    selectedUser = user
                                } else {
                                Toast.makeText(context, "Deletions failed. Please try again.", Toast.LENGTH_SHORT).show()
                            }
                        }
                    },""", """                                if (idToDelete != user.userId) {
                                    selectedUser = user
                                }
                            } else {
                                Toast.makeText(context, "Deletions failed. Please try again.", Toast.LENGTH_SHORT).show()
                            }
                        }
                    },""")


with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
