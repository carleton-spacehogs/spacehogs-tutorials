# sampleA.py
# 08/12/21

# Run with the following command:
# python3 sampleA.py example.fa list-of-contigs.txt

# Sys is a standard import for file specification, time is just for timing.
import sys
import time

# The following lines simply open the input files and convert their information
# into an array format that can be used multiple times.
fasta = open(sys.argv[1], 'r')
fa = fasta.readlines()
fasta.close()

sublist = open(sys.argv[2], 'r')
sl = sublist.readlines()
sublist.close()

print('Lines read')
# Here we begin "timing" the operations that can be sped up with multiprocessing
start = time.time()

# The output file is of course a fasta, as we are taking a subset of example.fa
outfile = open('subsetA.fa', 'w')

# Now we jump into the nested loop, comparing every contig in the list to every
# one in the fasta file to find where they match up. Theoretically it shouldn't
# matter which file contents we use for the outer and inner loops, but actually
# it's a lot easier to traverse the short txt list, so we would rather do that
# millions of times and just go through each line in the fasta once.
for i in range(len(fa)):
    # If the fasta line begins with '>' and therefore contains a contig name...
    if (fa[i][0] == '>'):
        # ...then the contig name is what's between '>' and the invisible return
        # character at the end of the line.
        contig = fa[i][1:-1]
        # Now for each target contig in the list file...
        for j in range(len(sl)):
            # ...the target contig name is just the line minus the invisible
            # return character at the end of the line.
            target = sl[j][:-1]
            if target == contig:
                # When a match is found, we write both the contig name and the
                # corresponding sequence from the fasta file into the subset
                # output file
                outfile.write(fa[i])
                outfile.write(fa[i+1])
                # Then we break from the inner loop to save a little time, since
                # we only make it this far if a match was found.
                break

outfile.close()
# Now we print the amount of time the whole process took
print("Process took " + str(time.time() - start) + " seconds.")

