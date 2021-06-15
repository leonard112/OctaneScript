set x to type <>
#print [type "hello" equals type "world"]
set x to array
append type "hello" to x

function y()
    return 1
end
function returnType(valueType)
    return valueType
end

function takesTypes(a, b, c, d, e)
    print "Success!"
end

print type x
print type y
#print [type  y equals type "hello"]
#print [type "hello" equals type   y]
#print [type "hello   type y" equals type   y]
print "hello type y" . type y
print "hello type y" . "type x type y " . type y

print returnType(@Type:String)
takesTypes(@Type:String, @Type:Number, @Type:Boolean, @Type:Array, @Type:Function)
print [@Type:String]
print [@Type:String equals @Type:String]
print [true and false]