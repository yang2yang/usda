import re

# 这是需要匹配的文本
text = "<h3>下一个你需要输入的数字是36752. 还有一大波数字马上就要到来...</h3>"

# 首先要定义一个pattern，注意这里要使用r''这种形式
pattern = re.compile(r'.+输入.*数字\D*(\d+).+')
# pattern = re.compile(r'.+输入.*数字\D*(\d+)..+')

#然后调用re模块中的API，这里调用的search函数
num = pattern.search(text)

#匹配到的字符串后，会将括号中的东西放入group中
print("hello")
print(num.group(0))
print(num.group(1))


print(type("123") == type(""))