from functions import solve
# filename = "c_incunabula"
# filename = "a_example"
filename = "f_libraries_of_the_world"
filename = "c_incunabula"
filename = "e_so_many_books"
filename = "a_example"
filename = "b_read_on"
filename = "d_tough_choices"

class book():
    def __init__(self, id, score):
        self.id = id
        self.score = score

class lib():
    def __init__(self, id, books_num, signup_days, books_per_day, books):
        self.id = id
        self.books = books
        self.books_num = books_num
        self.signup_days = signup_days
        self.books_per_day = books_per_day
    
with open("input/" + filename + ".txt") as f:
    content = f.readlines()
f.close()

content = [[int(x1) for x1 in x.strip().split(" ")] for x in content]

number_of_books = content[0][0]
libraries_num   = content[0][1]
days            = content[0][2]

scores_of_books = content[1]
libraries       = []

# print (scores_of_books)

for x in range(1,len(content)/2):
    # books = {}
    # for b in content[x * 2 + 1]:
    #     books[b] = book(b,scores_of_books[b])
    books = []
    for b in content[x * 2 + 1]:
        books.append (book(b,scores_of_books[b]))
    books.sort(key=lambda x: x.score, reverse=True)
    libraries.append ( lib(x - 1, content[x * 2][0], content[x * 2][1], content[x * 2][2], books) )

print ("done reading file")
ret = solve (days, libraries)

ret = [ ' '.join(map(str, x)) for x in ret]

with open("output/" + filename + ".out", "w") as f:
    for item in ret:
        print >> f, item

print ("all done.")
# print (ret)