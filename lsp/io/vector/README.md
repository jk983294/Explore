# main convenience offered by readv, writev

## It allows working with non contiguous blocks of data. i.e. buffers need not be part of an array, but separately allocated.

## The I/O is 'atomic'. i.e. If you do a writev, all the elements in the vector will be written in one contiguous operation, and writes done by other processes will not occur in between them.
