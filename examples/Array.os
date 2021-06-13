set arrayOne to <<"hello", "world">, <1, 2>, <true, false>>
set arrayTwo to array 
for nestedArray in arrayOne
    for element in nestedArray
        append element to arrayTwo
    end
end

set x to array
print x
append 1 to x
print x
append "hello" to x
print x
prepend true to x
print x
set y to <1, 2, 3>
print y
append y to x
print x
append "string, with, commas" to x
print x
print x<0>
pop from x
print x
set index to "first"
print x<2><first>
print index<last>

print "hello" . index<first>

repeat for index in x
    print index
end

print
print index