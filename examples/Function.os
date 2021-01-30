function countDown(x)
    if [x greaterThan 0]
        return countDown((x-1))
    else
        return x
    end
end

function shortCircuit()
    return "hello"
    print err
end

set val to countDown(100)

print val

#print shortCircuit()

print "done"