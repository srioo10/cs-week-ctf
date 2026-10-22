# Empty File - it's a program in the Whitespace language (only space, tab, newline matter)
# Instructions used here:   [space][space] <number> LF  = push number
#                           [tab][LF][space][space]     = print the top of the stack as a character
src = open("../files/empty.txt").read()
src = "".join(ch for ch in src if ch in " \t\n")

i, stack, out = 0, [], ""
def number():
    global i
    sign = -1 if src[i] == "\t" else 1       # first char is the sign
    i += 1
    bits = ""
    while src[i] != "\n":
        bits += "1" if src[i] == "\t" else "0"
        i += 1
    i += 1                                   # skip the LF that ends the number
    return sign * int(bits or "0", 2)

while i < len(src):
    if src[i:i+2] == "  ":                   # push
        i += 2
        stack.append(number())
    elif src[i:i+4] == "\t\n  ":             # output character
        i += 4
        out += chr(stack.pop())
    else:
        break                                # end of the part we care about
print(out)
