function test(x)
    return (x + 1)
end
function equals(x, y)
    return [x equals y]
end

print "hello" . test(5) . "world" . test(10) . "test(5)"
print (test(1) + 1 + test(2) + test(3))
print [[test(1) and test(2)] equals equals(2, 4)]