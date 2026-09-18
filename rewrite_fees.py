import re

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 'r') as f:
    content = f.read()

# We want to change the outer Column to a LazyColumn,
# and wrap the header parts in item { ... }
# and change the inner LazyColumn to items(...)

old_fees = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
        ) {
            // MODULE BAR: Material 3 Header & synchronization badge
            Surface(
                tonalElevation = 2.dp,"""

new_fees = """        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
        ) {
            item {
            // MODULE BAR: Material 3 Header & synchronization badge
            Surface(
                tonalElevation = 2.dp,"""

content = content.replace(old_fees, new_fees)

# Now we need to close the first item and start the next items or keep them in the same item.
# It's better to put all the headers in one `item {` and then use `items` for the student list.
old_header_end = """            // STUDENT LIST (Vertical LazyColumn)
            Text(
                text = "Registered Scholars Directory (${filteredStudentsByClassAndSearch.size})",
                style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                modifier = Modifier.padding(start = 16.dp, top = 8.dp, bottom = 8.dp),
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            if (filteredStudentsByClassAndSearch.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("No matching students found.", style = MaterialTheme.typography.bodyLarge)
                }
            } else {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                        .padding(horizontal = 16.dp)
                        .testTag("school_fees_student_list"),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    contentPadding = PaddingValues(bottom = 80.dp)
                ) {
                    items(filteredStudentsByClassAndSearch) { student ->"""

new_header_end = """            // STUDENT LIST (Vertical LazyColumn)
            Text(
                text = "Registered Scholars Directory (${filteredStudentsByClassAndSearch.size})",
                style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                modifier = Modifier.padding(start = 16.dp, top = 8.dp, bottom = 8.dp),
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            } // end of header item

            if (filteredStudentsByClassAndSearch.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                        Text("No matching students found.", style = MaterialTheme.typography.bodyLarge)
                    }
                }
            } else {
                item {
                    Spacer(modifier = Modifier.height(8.dp))
                }
                items(filteredStudentsByClassAndSearch) { student ->
                    Box(modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp)) {"""

content = content.replace(old_header_end, new_header_end)

# Also need to close the Box and the whole structure.
old_tail = """                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun FeeComponentRow(title: String, amount: Double, icon: ImageVector) {"""

new_tail = """                            }
                        }
                    }
                    } // close Box
                }
                item {
                    Spacer(modifier = Modifier.height(80.dp))
                }
            }
        }
    }
}

@Composable
fun FeeComponentRow(title: String, amount: Double, icon: ImageVector) {"""

content = content.replace(old_tail, new_tail)

with open("app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt", 'w') as f:
    f.write(content)

