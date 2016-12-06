import xml.etree.cElementTree as ET


tree = ET.ElementTree(file="test.xml")

print(tree.getroot())

root = tree.getroot()

print(root.tag,root.attrib)

for child_of_root in root:
    print(child_of_root.tag, child_of_root.attrib,child_of_root.text)