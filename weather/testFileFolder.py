import os

# 非递归
# print(os.listdir())

# for dirpath, dirnames, filenames in os.walk("."):
#     # print('Directory', dirpath)
#     for filename in filenames:
#         print (' File', filename)


def Test2(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        print(path)
        if os.path.isdir(path):
            Test2(path)

Test2(".")

print("adb".isalpha())
