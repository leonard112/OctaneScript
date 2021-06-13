function returnString()
    return "string"
end
function addOne(x)
    return (x + 1)
end
function addPointFive(x)
    return (x + .5)
end
function returnBool()
    return true
end
function testArray(x, y)
    return x
end

set stringValue to "hello" . returnString() . "world"
set integerValue to "hello" . addOne(1) . "world"
set decimalValue to "hello" . addPointFive(1) . "world"
set booleanValue to "hello" . returnBool() . "world"
set arrayValue to testArray(<1, 2, 3>, <4, 5, 6>)
print arrayValue
if [true]
    function returnOne()