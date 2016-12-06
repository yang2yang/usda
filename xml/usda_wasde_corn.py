import xml.etree.cElementTree as ET

tree = ET.ElementTree(file="wasde-10-12-2016.xml")

print(tree.getroot())

root = tree.getroot()

# for child_of_root in root:
#     print(child_of_root.tag, child_of_root.attrib,child_of_root.text)

# wasde_corn 是s12(第4个) 进入Re 进入第二张表 进入Collection
s12_corn = root[4][0][1][0]

for a in s12_corn:
    for b in a.iter():
        print(b.attrib)