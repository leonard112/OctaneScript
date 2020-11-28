
print "Outside of if"
if [false]
    if [false]
        print "in second if"
    else
        print "in second else"
    end
end
print "This won't print"