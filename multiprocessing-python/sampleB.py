# sampleB.py
# 08/12/21

# Run with the following command:
# python3 sampleB.py example.fa list-of-contigs.txt

import sys
import time
# This is the only new import we'll need.
from multiprocessing import Pool

# To effectively script with multiprocessing, we need to set up a function-based
# script. The nested loop we used in the first script is basically contained
# within a single function here, which we will call 'search.' Everything else
# happens in the main function -- if that is not a familiar concept to you,
# that's okay. Just pretend the 'search' function doesn't exist for now and skip
# down to the weird 'if __name__' thing.

def search(i):
    # This is basically the same nested loop structure as in the other script,
    # but the outer loop is now split among processers in the main function.
    if (fa[i][0] == '>'):
        contig = fa[i][1:-1]
        for j in range(len(sl)):
            target = sl[j][:-1]
            if target == contig:
                # Here is the other key difference:  we return the fasta lines
                # rather than writing them to an outfile directly. Though that
                # would still technically be possible and probably even work
                # faster, it is dangerous to write to shared memory
                # simultaneously and as such it should be avoided when possible.
                return (fa[i] + fa[i+1])
                # Since only a handful of runs through 'search' will actually
                # reach this return statement, a 'None' object will be returned
                # in many cases. This will be dealt with when we write to the
                # outfile.

# Main function
if __name__ == '__main__':
    # This initial section of the main function is almost exactly the same as
    # the first section of the other script, with one key difference: this time
    # we have to make global variables for the arrays we make from the fasta and
    # txt files, since the search function has to have access to them.
    global fa
    fasta = open(sys.argv[1], 'r')
    fa = fasta.readlines()
    fasta.close()

    global sl
    sublist = open(sys.argv[2], 'r')
    sl = sublist.readlines()
    sublist.close()

    print('Lines read')
    start = time.time()

    # Here's where we dive into the real multiprocessing. This line may seem a
    # bit cryptic, but all you really need to know is we are using the Pool
    # module to specify how many concurrent processes we want to run (in this
    # case 10, just be mindful of the available processers on the server). Then
    # we have to give it a name, so we just call it pool with no capitalization
    # because what else would we call it?
    with Pool(processes=15) as pool:
        # Now we use this really cool Pool.map thing to give a function to
        # our pool of processers. The only arguments it needs are the name of
        # the function (search) and a list of values. Now this can be really
        # confusing, but essentially each value in the list will be used as an
        # argument for a single run of the function by a single processer. So,
        # in our case, we would like the function to be run once for every line
        # of the fasta file, so we use range(len(fa)) to make a list of every
        # line number. Each time the function is run it takes in a different
        # line number as an argument, which will be applied as the 'i' in the
        # search function. Then within that function we can just pretend it was
        # a loop all along.
        # As for the output, 'map' handily takes all the return values and
        # sticks them in another array.
        outarr = pool.map(search, range(len(fa)))

    outfile = open('subsetB.fa', 'w')
    # This time we just write the data that map put into our array to the
    # outfile all at once
    for val in outarr:
        # Most of the function calls will not have returned a hit, so it's
        # important to only write the values in the output array that are
        # actually in a string format, which is what 'isinstance' checks for.
        if isinstance(val, str):
            outfile.write(val)
    outfile.close()

    print("Process took " + str(time.time() - start) + " seconds.")

