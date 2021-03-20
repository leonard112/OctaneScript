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

function factorial(n)
    if [n equals 0]
        return 1
    else
        return (n * factorial(n - 1))
    end
end

# set val to countDown(498)

set val to factorial(10)
print val

#print shortCircuit()

print "done"