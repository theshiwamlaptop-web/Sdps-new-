with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    text = f.read()

open_braces = text.count('{')
close_braces = text.count('}')
print(f"Open braces: {open_braces}")
print(f"Close braces: {close_braces}")
