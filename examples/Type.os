set x to type <>
#print [type "hello" equals type "world"]
set x to array
append type "hello" to x

function y()
    return 1
end
print type x
print type y
print [type  y equals type "hello"]
print [type "hello" equals type   y]
print [type "hello   type y" equals type   y]
print "hello type y" . type y
print "hello type y" . "type x type y " . type y