'''
This is like the first application of my data analysis.
The code that is going to be used here will be indispensable in my future things.

1. Make some initial hypothesis. plot graphs.
2. Explore the data: calculate the mean, mode, deviations, etc.

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

from functions import solve
from matplotlib import pyplot as plt
from collections import Counter
from math import sqrt
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

def plotScoresOfBooks (scores_of_books):
    return scores_of_books

def plotBooksFrequency (number_of_books, content):
    books = [0] * number_of_books
    for x in range(1,len(content)/2):
        for b in content[x * 2 + 1]:
            books[b] += 1
    return books

def plotScoresFrequencies (scores_of_books):
    max_score = max (scores_of_books)
    min_score = min (scores_of_books)
    books = [0] * (max_score + 1 - min_score)
    for s in scores_of_books:
        books[s - min_score] += 1
    return [books, "Scores", "Frequencies"]

def plotLibrariesSignup (number_of_libraries, content):
    libs = []
    for x in range(1,len(content)/2):
        libs.append(content[x * 2][1])
    return libs

def plotLibrariesThroughput (number_of_libraries, content):
    libs = []
    for x in range(1,len(content)/2):
        libs.append(content[x * 2][2])
    return libs

def plotLibrariesBestScore (number_of_libraries, content, books, time):
    libs = []
    for x in range(1,len(content)/2):
        max_run_time = time - content[x * 2][1]
        max_books = max_run_time * content[x * 2][2]
        b = []
        for b_i in content[x * 2 + 1]:
            b.append (books[b_i])
        b.sort(reverse=True)
        b = b[:max_books]
        libs.append( sum(b) )
    return libs

def plotLibrariesBestScoreAgainstOthers (number_of_libraries, content, books, booksInOtherLibs, time, rand):
    libs = []
    for x in range(1,len(content)/2):
        max_run_time = time - content[x * 2][1]
        max_books = max_run_time * content[x * 2][2]
        b = []
        for b_i in content[x * 2 + 1]:
            if (random.randint(1,booksInOtherLibs[b_i]) == 1):
                b.append (books[b_i])
        b.sort(reverse=True)
        b = b[:max_books]
        libs.append( sum(b) )
    return libs

def quantile (x,p):
    p_index = int (p * len(x))
    return sorted (x)[p_index]

def deviation (x_i, mean):
    return x_i - mean

def variance (x):
    var = 0
    if (len (x) <= 1):
        return 0
    mean = sum (x) / len (x)
    for x_i in x:
        var += (deviation (x_i, mean) ** 2)
    return var / (len (x) - 1.0)

def statistics (x, stats_name):
    print "Stats: " + stats_name + "\n=========="
    print "count        : " + str(len (x))
    print "range        : " + str(max (x)) + " - " + str(min (x)) + " = " + str(max (x) - min (x))
    print "mean         : " + str(sum (x) / len (x))
    print "median       : " + str(sorted (x) [len (x) // 2])
    print "quantile 25% : " + str( quantile (x,.25) )
    print "quantile 50% : " + str( quantile (x,.5) )
    print "quantile 75% : " + str( quantile (x,.75) )
    print "mode         : " + str(Counter (x).most_common (1))
    var = variance(x)
    print "variance     : " + str(var)
    print "std dev      : " + str(sqrt(var))
    print ""

def covariance (x,y):
    if (len (x) <= 1):
        return 0
    mean_x = sum (x) / len (x)
    mean_y = sum (y) / len (y)
    x_y = zip (x, y)
    corr = 0
    for i in x_y:
        corr += ((i[0] - mean_x) * (i[1] - mean_y))
    return corr / (len(x_y) - 1.0)

def correlation (x,y):
    dev_x = sqrt( variance(x) )
    dev_y = sqrt( variance(y) )
    if (dev_y > 0 and dev_x > 0):
        return covariance (x,y) / dev_x / dev_y;
    return 0.0
    
with open("input/" + filename + ".txt") as f:
    content = f.readlines()
f.close()

content = [[int(x1) for x1 in x.strip().split(" ")] for x in content]

number_of_books = content[0][0]
libraries_num   = content[0][1]
days            = content[0][2]

scores_of_books = content[1]
libraries       = []

scores          = plotScoresOfBooks  (scores_of_books)
frequencies     = plotBooksFrequency (number_of_books, content)

signup          = plotLibrariesSignup (libraries_num, content)
throughput      = plotLibrariesThroughput (libraries_num, content)
libBestScore    = plotLibrariesBestScore (libraries_num, content, scores_of_books, days)

r = random.random()

libBestScoreAO  = plotLibrariesBestScoreAgainstOthers (libraries_num, content, scores_of_books, frequencies, days, r)

# plt.axis([0, len(signup)-1, min(signup)-1, max(signup)+1]) 
# plt.xlabel("books")
plt.title (filename)
plt.plot(scores,label="scores")
plt.plot(frequencies,label="frequencies")
statistics (scores, "scores")
statistics (frequencies, "frequencies")
print "correlation  : " + str (correlation (scores,frequencies))
# plt.savefig(filename + "_" + y_label + ".png")
plt.legend()
plt.show()

plt.title (filename)
plt.plot(signup,label="signup")
# plt.plot(libBestScore,label="libBestScore")
plt.plot(throughput,label="throughput")
statistics (signup, "libraries signup")
# statistics (libBestScore, "libraries BestScore")
statistics (throughput, "libraries throughput")
print "correlation  : " + str (correlation (signup,throughput))
# print "correlationBS: " + str (correlation (libBestScore,throughput))
print "num of days  : " + str (days)
# plt.savefig(filename + "_" + y_label + ".png")
plt.legend()
plt.show()

print ("all done.")