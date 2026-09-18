with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

# Fix 1: item for Contact Details
text = text.replace(
    "                    }\n            }\n            // Contact details update",
    "                    }\n                }\n            }\n            // Contact details update"
)

# Fix 2: item for Security key updates
text = text.replace(
    "                        }\n                    }\n            }\n            // Security key updates",
    "                        }\n                    }\n                }\n            }\n            // Security key updates"
)

# Fix 3: item for Theme Preferences
text = text.replace(
    "                            }\n                        }\n                    }\n            }\n            // Theme Preferences",
    "                            }\n                        }\n                    }\n                }\n            }\n            // Theme Preferences"
)

# Fix 4: item for Alert Toggles
text = text.replace(
    "                            }\n                        )\n                    }\n            }\n        }\n        // Principal permanent deletion",
    "                            }\n                        )\n                    }\n                }\n            }\n        }\n        // Principal permanent deletion"
)

# Fix 5: deleteUserAccount missing brace inside confirmButton
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

# Fix 6: Missing closing braces for showDeleteConfirmDialog and item at the end of Principal deletion
text = text.replace("""                ) {
                    Text("NO (Cancel)", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onErrorContainer)
                }
            }
        )
        if (showPasswordDialog) {""", """                ) {
                    Text("NO (Cancel)", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onErrorContainer)
                }
            }
        }
        }
        if (showPasswordDialog) {""")

# Fix 7: Missing closing braces for showPasswordDialog and SettingsScreen?
# At the end of ProfileSettingsTab:
#        }
#    )
#
#
#
#@Composable
text = text.replace("""                ) {
                    Text("Cancel")
                }
            }
        )
        



@Composable""", """                ) {
                    Text("Cancel")
                }
            }
        }
    }
}

@Composable""")

# Fix 8: myStudent == null missing brace in StudentERPPanel
text = text.replace("""                    if (myStudent == null) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Text("Aadhaar files and pupil particulars not fully synchronized. Please contact administration desk.", color = Color.Gray, textAlign = TextAlign.Center)
                        }
                        } else {""", """                    if (myStudent == null) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Text("Aadhaar files and pupil particulars not fully synchronized. Please contact administration desk.", color = Color.Gray, textAlign = TextAlign.Center)
                        }
                    } else {""")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
