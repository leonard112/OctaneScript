# Release Notes

* __0.0.1-alpha__
  * `print` function implemented. `print` can print strings to the console. `print` must take one argument enclosed in single or double quotes. Coloring and styling can be applied to text easily by by calling a specialized version of `print`. For example you can print __RED__ and __UNDERLINED__ text with the following print function: `printRedUnderline "This text is red and underlined."` 
* __0.0.2-alpha__
  * `set` function implemented. `set` is used to __DEFINE VARIABLES__. Note that __String__ values are the only values supported in this version. Use the following syntax to set a variable: `set x to "string value"`
  * __STRING CONCATENATION__ added. String values can be concatenated using the `.` operator. Here are some string concatenation examples:
```
$ octane
>> set x to "Hello " . "world!"
>> set y to x
>> print x . " Here is some more text. " . y
Hello world! Here is some more text. Hellow world!
>> exit
$
```

* __0.0.3-alpha__
  * Math and numbers implemented. `print` can be used to print numbers or the results of a math expression, and `set` be used to set a number or the results of a math expression to a variable. All numbers and math must be inclosed in parentheses with the exception of integers and variables. Here are some examples:
```
$ octane
>> print 5
5
>> print (2.4)
2.4
>> print (2 + (4 * 4))
18
>> print (10 / 4)
2.5
>> set x to 5
>> set y to (3.5)
>> set z to (x - y)
print x . " " . y . " " . z
5 3.5 1.5
```
 * Code for parsing string concatenation expressions refactored and improved.
