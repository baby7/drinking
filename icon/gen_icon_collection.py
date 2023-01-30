import base64

# with open("icon.py", "w") as f:
#     f.write('class Icon(object):\n')
#     f.write('\tdef __init__(self):\n')
#     f.write("\t\tself.ig='")
# # with open("GreenWaves.ico", "rb") as i:
# #     b64str = base64.b64encode(i.read())
# with open("BlakeBell.ico", "rb") as i:
#     b64str = base64.b64encode(i.read())
# with open("icon.py", "ab+") as f:
#     f.write(b64str)
# with open("icon.py", "a") as f:
#     f.write("'")

with open("collection.py", "w") as f:
    f.write('class Collection(object):\n')
    f.write('\tdef __init__(self):\n')
    f.write("\t\tself.ig='")
# with open("GreenWaves.ico", "rb") as i:
#     b64str = base64.b64encode(i.read())
with open("collection.jpg", "rb") as i:
    b64str = base64.b64encode(i.read())
with open("collection.py", "ab+") as f:
    f.write(b64str)
with open("collection.py", "a") as f:
    f.write("'")