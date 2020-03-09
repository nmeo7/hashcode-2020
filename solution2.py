'''
about the algorithm:

1. before you scan a book you can check whether it has been scanned by another library.
2. that means that you have to do all the scannings in parallel.

1. pick the best book in the shelf.
2. find a library to assign it to.
3. remove the book from the library.
4. see if there is still an iddle library at the moment.
5. if there is one, look for a book to assign it to.
6. check if there is no library in process.
7. if there isn't, add one library to the signup process.

'''

from functions   import solve
from matplotlib  import pyplot as plt
from collections import Counter
from math        import sqrt
import random

filenames = {
    "a": "a_example",
    "b": "b_read_on",
    "c": "c_incunabula",
    "d": "d_tough_choices",
    "e": "e_so_many_books",
    "f": "f_libraries_of_the_world",
}

filename = filenames["d"]

'''
incunabula:
remove all the books whose score is under a particular treshold. say 300. the mean.
keep the books only in the library that holds it and has the highest throughput.
well, frequency here is not that big of an issue though.

libraries throughput is very dynamic
keep the libraries whose throughput is at least the mean. 50000
keep also the libraries whose time to start is lowest. less than 500 at least.

so many books:
check by libraries who appear to have many important books.
signup time is the same, throughput is from 1 to 9 just
'''

def pick_book_at_random (frequencies):
    if (random.randint(0,frequencies - 1) > 1):
        return False
    return True

def lib_max_score (books_scores,books_frequencies,libraries,time):
    for i in libraries.keys():
        max_score = 0
        t = (time - libraries[i]['signup']) * libraries[i]['throughput']
        books = libraries[i]['books'][:t]
        for book in books:
            max_score += books_frequencies[book] # tough choices
            # if pick_book_at_random( books_frequencies[book] ): # not tough choices
                # max_score += books_scores[book]
        libraries[i]['max_score'] = max_score

def libraries_above_treshold (libraries):
    ret = []
    for i in libraries.keys():
        # if (libraries[i]['throughput'] > 10000 and libraries[i]['signup'] < 500): # incunabula
            # ret.append( [ i, libraries[i]['signup'] ] )
        # if (libraries[i]['signup'] < 5): # so many books
            # ret.append( [ i, libraries[i]['max_score'] ] )
        # ret.append( [ i, libraries[i]['signup'] ] ) # still so many books
        # ret.append( [ i, libraries[i]['signup'] ] ) # libraries of the world
        # if (libraries[i]['signup'] < 57): # libraries of the world
            # ret.append( [ i, libraries[i]['max_score'], libraries[i]['signup']] ) # libraries of the world
        ret.append( [ i, libraries[i]['max_score'] ]) # tough choices
        # ret.append( [ i, libraries[i]['signup'] ]) # read on

    ret.sort (key=lambda (a,b):b,reverse=False) # 14736 14976   

    ret2 = []
    for i,j in ret:
        ret2.append (i)
    return ret2

def libraries_per_signup_date_max_min (libs,libraries):
    ret  = []
    for i in libs:
        avg = sum (libraries[i]['books']) / len (libraries[i]['books'])
        max_score_avg = avg * libraries[i]['throughput']
        libraries[i]['max_score_avg'] = max_score_avg
    for i in libs:
        ret.append ( [ i, libraries[i]['max_score_avg'] ] )        
    ret = sorted (ret, key=lambda (a,b):b,reverse= False)
    ret2 = []
    for i,j in ret:
        ret2.append (i)
    return ret2

def libraries_per_signup_date_fast (libraries):
    ret = []
    for i in libraries.keys():
        if ( libraries[i]['throughput'] >= 9 ):
            ret.append ( [ i, libraries[i]['signup'] ] )
    ret = sorted (ret, key=lambda (a,b):b,reverse= False)
    ret2 = []
    for i,j in ret:
        ret2.append (i)
    return ret2

def libraries_per_signup_date (libraries):
    ret = []
    for i in libraries.keys():
        ret.append ( [ i, libraries[i]['signup'] ] )
    ret = sorted (ret, key=lambda (a,b):b,reverse= False)
    ret2 = []
    for i,j in ret:
        ret2.append (i)
    return ret2

def libraries_per_quality_of_books (libraries,books_scores,time):
    ret = []
    for i in libraries.keys():
        books_weights = 0
        max_scores = libraries[i]['books'][:time*libraries[i]['throughput']]
        for book in max_scores:
            books_weights += books_scores[book]
        avg = books_weights
        max_score_avg = avg * libraries[i]['throughput']
        libraries[i]['max_score_avg'] = max_score_avg
        ret.append ( [ i, libraries[i]['max_score_avg'] ] ) 
    ret = sorted (ret, key=lambda (a,b):b,reverse= True)
    ret2 = []
    for i,j in ret:
        ret2.append (i)
    return ret2

# maybe reorder them in such a way that the ones with good books come last.
# to make sure the same books are maybe taken care from other libraries.
def append_library (active_libraries, library):
    active_libraries.append(library)

def process_signup (active_libraries, all_libraries, signing_up):
    if signing_up.get("remaining_days") == 0:
        append_library (active_libraries, signing_up.get("queue")[0])
        signing_up["queue"] = signing_up.get("queue")[1:]
        if (len(signing_up["queue"]) == 0):
            signing_up["remaining_days"] = -1
        else:
            signing_up["remaining_days"] = all_libraries[signing_up.get("queue")[0]].get('signup')
    signing_up["remaining_days"] = signing_up.get("remaining_days") - 1

def process_scans (read_books, active_libraries, all_libraries):
    for lib in active_libraries:
        limit = all_libraries[lib].get("throughput")
        skip = 0
        for book in all_libraries[lib].get("books"):
            if book not in read_books:
                limit = limit - 1
                read_books.add (book)
                all_libraries[lib].get("read").append(book)
            skip = skip + 1
            if limit == 0:
                break
        all_libraries[lib]["books"] = all_libraries[lib].get("books")[skip:]

# all these parameters are given by reference.
# read all these books without repeating the ones that have already been read.
def process_day (read_books, active_libraries, all_libraries, signing_up):
    process_signup (active_libraries, all_libraries, signing_up)
    process_scans (read_books, active_libraries, all_libraries)
    
with open("input/" + filename + ".txt") as f:
    content = f.readlines()
f.close()

content = [[int(x1) for x1 in x.strip().split(" ")] for x in content]

books_num,libs_num,days_num = content[0]
scores_of_books             = content[1]

content                     = content[2:]
libraries                   = {}

frequencies = [0] * books_num
for x in range(0,libs_num):
    for b in content[x * 2 + 1]:
        frequencies[b] += 1

for x in range(0,libs_num):
    books = []
    for b in content[x * 2 + 1]:
        books.append([b, scores_of_books[b]])
    books.sort (key=lambda (a,b):b,reverse=True)
    books1 = []
    for i,b in books:
        books1.append (i)
    libraries[x] = {
                'signup': content[x * 2][1],
                'throughput': content[x * 2][2], 
                'books': books1,
                'read': []
            }

# print (libraries)

# pre touch of the data: order the books, order the libraries in all the sorts I want.
# somehow remove the books that are too frequent, reorder the libraries, etc.
queue = libraries.keys()
lib_max_score (scores_of_books,frequencies,libraries,days_num)
queue = libraries_above_treshold (libraries)
copy_of_queue = queue[:]

read_books = set()
active_libraries = []
signing_up = {
    "remaining_days": libraries[0].get('signup'),
    "queue": copy_of_queue
}

print "done reading. starting processing"

for day in range(0,days_num):
    process_day (read_books,active_libraries,libraries,signing_up)
    print "day " + str (day) + "/" + str(days_num-1)
    # print (libraries)

libs = []
for lib in queue:
    if lib not in libraries:
        continue
    if len(libraries[lib]["read"]) < 1:
        continue
    libs.append (lib)

ret = [ [len(libs)] ]
for lib in libs:
    ret.append ( [ lib, len(libraries[lib]["read"]) ] )
    ret.append ( libraries[lib]["read"] )

ret = [ ' '.join(map(str, x)) for x in ret]

# print ret

with open("output/" + filename + ".out", "w") as f:
    for item in ret:
        print >> f, item

print ("all done.")
print str(len(libs)) + " libraries of " + str(len(libraries))
