with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

def insert_before(line_idx, text):
    lines.insert(line_idx, text)

# We must apply insertions from bottom to top so line numbers don't shift!
# Let's map original 1-based line numbers to 0-based indices.

# 2053: `                        } else {` -> `                        }\n                        } else {`
lines[2052] = "                        }\n" + lines[2052]

# 2049: `                2 -> {` -> insert `                }\n` before
lines.insert(2048, "                }\n")

# 2028: `                            } else {` -> insert `                            }\n`
lines[2027] = "                            }\n" + lines[2027]

# 2021: `                1 -> {` -> insert `                }\n` before
lines.insert(2020, "                }\n")

# 1996: `                            } else {`
lines[1995] = "                            }\n" + lines[1995]

# 1846: `                2 -> {`
lines.insert(1845, "                }\n")

# 1813: `                            } else {`
lines[1812] = "                            }\n" + lines[1812]

# 1799: `                1 -> {`
lines.insert(1798, "                }\n")

# 1764: `                            } else {`
lines[1763] = "                            }\n" + lines[1763]

# 1415: `                            } else {`
lines[1414] = "                            }\n" + lines[1414]

# 1364: `                                                                3 -> {` -> wait, it's 3 -> {
lines.insert(1363, "                }\n")

# 1232: `                2 -> {`
lines.insert(1231, "                }\n")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.writelines(lines)

