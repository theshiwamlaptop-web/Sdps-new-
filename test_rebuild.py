with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
indent_stack = [0]
# we will strip all lines of trailing spaces
# if a line is just '}', we ignore it.
# we will infer '}' by comparing the current line's indentation with the stack!

# wait, what if the line is `} else {` ?
# we will ignore the `}` part and treat it as `else {`, then infer the `}` before it!
