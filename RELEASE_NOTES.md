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
