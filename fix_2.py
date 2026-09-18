with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

text = text.replace("""                                Toast.makeText(context, "School Wide Parameters Saved Successfully!", Toast.LENGTH_SHORT).show()
                            }
                ,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(48.dp)
                        ) {
                            Text("Save Facility Setup Configuration", fontWeight = FontWeight.Bold)
                        }
                                
                                
                }
                3 -> { // COMPREHENSIVE SECURITY AUDITS LOG""", """                                Toast.makeText(context, "School Wide Parameters Saved Successfully!", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(48.dp)
                        ) {
                            Text("Save Facility Setup Configuration", fontWeight = FontWeight.Bold)
                        }
                    }
                }
                3 -> { // COMPREHENSIVE SECURITY AUDITS LOG""")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
