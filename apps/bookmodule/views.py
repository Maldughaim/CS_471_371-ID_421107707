from django.shortcuts import render, redirect
from .models import Book,Address,Student,Student2, Images
from django.db.models import Q,Min,Max,Avg,Sum,Count
from .forms import BookForm,StudentForm, StudentForm2, ImageForm
from django.contrib.auth.decorators import login_required


def index(request):
    name = request.GET.get("name") or "World"
    return render(request, 'bookmodule/index1.html',{'name':name})

def index2(request, val1 = 0):
    return render(request, "bookmodule/index2.html", {"value":val1})

def index1(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook1(request, bookId):
    book1 = {'id': 123, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'}
    book2 = {'id': 456, 'title': 'Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId:
        targetBook = book1

    if book2['id'] == bookId:
        targetBook = book2

    context = {'book': targetBook}  # book is the variable name accessible by the template
    return render(request, 'bookmodule/show.html', context)

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html', {"bookId":bookId})

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links(request):
    return render(request, 'bookmodule/links.html')

def formatting(request):
    return render(request, 'bookmodule/formatting.html')

def listing(request):
    return render(request, 'bookmodule/listing.html')

def tables(request):
    return render(request, 'bookmodule/tables.html')

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower():
                contained = True
            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained: newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})
    else:
        return render(request, 'bookmodule/search.html')

def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull = False).filter(title__icontains='and').filter(edition__gte = 2).exclude(price__lte = 100)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task1(request):
    mybooks=Book.objects.filter(Q(price__lte = 50))
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task2(request):
    mybooks=Book.objects.filter(Q(edition__gt = 2) & Q(Q(title__contains = 'qu') | Q(author__contains = 'qu')))
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task3(request):
    mybooks=Book.objects.filter(~Q(edition__gt = 2) & Q(~Q(title__contains = 'qu') | ~Q(author__contains = 'qu')))
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task4(request):
    mybooks=Book.objects.filter().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task5(request):
    num =Book.objects.filter().count()
    sumb = Book.objects.aggregate(Sum('price', default=0))
    avgb = Book.objects.aggregate(a = Avg('price', default=0))
    maxb = Book.objects.aggregate(b = Max('price', default=0))
    minb = Book.objects.aggregate(c = Min('price', default=0))


    return render(request, 'bookmodule/task5.html', {'number_of_books': num, 'price_of_books': sumb['price__sum'], 'avg_of_books': avgb['a'], 'max_of_books': maxb['b'], 'min_of_books': minb['c']})

def task7(request):

    ad = Address.objects.annotate(n = Count('student'))

    return render(request, 'bookmodule/task7.html', {'arr': ad})

def lab9(request):
    q = Book.objects.filter().all
    return render(request, 'bookmodule/bookListq.html', {'books': q})

def edit(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        p = render(request, 'bookmodule/editm.html', {'message': 'Something went wrong'})
        p['Refresh'] = '3; url=/books/lab9_part1/listbooks/'
        return p

    if request.POST.get('edit') == 'edit':
        title = request.POST.get('title')
        author = request.POST.get('author')
        edition = request.POST.get('edition')
        price = request.POST.get('price')

        book.title = title
        book.author = author
        book.edition = edition
        book.price = price

        book.save()
        p = render(request, 'bookmodule/editm.html', {'message': f'The book {book.title} is edited successfully'})
        p['Refresh'] = '3; url=/books/lab9_part1/listbooks/'
        return p
    else:
        return render(request, 'bookmodule/edit.html',{'book':book})

def delete(request, id):
    try:
        book = Book.objects.get(id = id)
        m = f'The book {book.title} is deleted successfully!'
        book.delete()
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab9_part1/listbooks/'
    except Book.DoesNotExist:
        m = 'Something went wrong!'
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab9_part1/listbooks/'

    return p

def addb(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        edition = request.POST.get('edition')
        price = request.POST.get('price')

        Book.objects.create(title=title, author=author, edition=edition, price=price)

        m = 'User added successfully!'
        p = render(request, 'bookmodule/addm.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab9_part1/listbooks/'
        return p
    else:
        return render(request,'bookmodule/add.html')

def lab9_2(request):
    q = Book.objects.filter().all
    return render(request, 'bookmodule/bookListq2.html', {'books': q})

def delete_2(request, id):
    try:
        book = Book.objects.get(id = id)
        m = f'The book {book.title} is deleted successfully!'
        book.delete()
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab9_part2/listbooks/'
    except Book.DoesNotExist:
        m = 'Something went wrong!'
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab9_part2/listbooks/'

    return p

def addb_2(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            edition = form.cleaned_data['edition']
            price = form.cleaned_data['price']
            Book.objects.create(title=title, author=author, edition=edition, price=price)

            m = 'Book added successfully!'
            p = render(request, 'bookmodule/addm.html', {'message': m})
            p['Refresh'] = '3; url=/books/lab9_part2/listbooks/'
            return p
    else:
        form = BookForm()
        return render(request,'bookmodule/add_2.html',{'form': form})

def edit_2(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        p = render(request, 'bookmodule/editm.html', {'message': 'Something went wrong'})
        p['Refresh'] = '3; url=/books/lab9_part2/listbooks/'
        return p

    if 'title' in request.POST:
        form = BookForm(request.POST, instance=book)  # Bind data to the form
        if form.is_valid():
            form.save()  # Save the changes to the database
            p = render(request, 'bookmodule/editm.html', {'message': 'Book edited successfully'})
            p['Refresh'] = '3; url=/books/lab9_part2/listbooks/'
            return p
    else:
        form = BookForm(instance=book)
        return render(request, 'bookmodule/edit_2.html', {'form': form})

def liststudents(request):
    q = Student.objects.filter().all
    return render(request, 'bookmodule/liststudents.html', {'students': q})

def addstudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            p = render(request, 'bookmodule/addm.html', {'message': 'Student added successfully'})
            p['Refresh'] = '3; url=/books/lab10/liststudents/'
            return p

    form = StudentForm(None)
    return render(request, 'bookmodule/addstudent.html', {'form': form})

def editstudent(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        p = render(request, 'bookmodule/editm.html', {'message': 'Something went wrong'})
        p['Refresh'] = '3; url=/books/lab10/liststudents/'
        return p

    if 'name' in request.POST:
        form = StudentForm(request.POST, instance=student)  # Bind data to the form
        if form.is_valid():
            form.save()  # Save the changes to the database
            p = render(request, 'bookmodule/editm.html', {'message': 'Student edited successfully'})
            p['Refresh'] = '3; url=/books/lab10/liststudents/'
            return p
    else:
        form = StudentForm(instance=student)
        return render(request, 'bookmodule/editstudent.html', {'form': form})

def deletestudent(request, id):
    try:
        student = Student.objects.get(id = id)
        m = f'The Student {student.name} is deleted successfully!'
        student.delete()
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab10/liststudents/'
    except Student.DoesNotExist:
        m = 'Something went wrong!'
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab10/liststudents/'

    return p

def liststudents2(request):
    q = Student2.objects.filter().all
    return render(request, 'bookmodule/liststudents2.html', {'students': q})

def addstudent2(request):
    if request.method == 'POST':
        form = StudentForm2(request.POST)
        if form.is_valid():
            form.save()
            p = render(request, 'bookmodule/addm.html', {'message': 'Student added successfully'})
            p['Refresh'] = '3; url=/books/lab10/task2/liststudents/'
            return p

    form = StudentForm2(None)
    return render(request, 'bookmodule/addstudent.html', {'form': form})

def editstudent2(request, id):
    try:
        student = Student2.objects.get(id=id)
    except Student2.DoesNotExist:
        p = render(request, 'bookmodule/editm.html', {'message': 'Something went wrong'})
        p['Refresh'] = '3; url=/books/lab10/task2/liststudents/'
        return p

    if 'name' in request.POST:
        form = StudentForm2(request.POST, instance=student)  # Bind data to the form
        if form.is_valid():
            form.save()  # Save the changes to the database
            p = render(request, 'bookmodule/editm.html', {'message': 'Student edited successfully'})
            p['Refresh'] = '3; url=/books/lab10/task2/liststudents/'
            return p
    else:
        print(student.addresses.all())
        form = StudentForm2(instance=student)
        return render(request, 'bookmodule/editstudent.html', {'form': form})

def deletestudent2(request, id):
    try:
        student = Student2.objects.get(id = id)
        m = f'The Student {student.name} is deleted successfully!'
        student.delete()
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab10/task2/liststudents/'
    except Student.DoesNotExist:
        m = 'Something went wrong!'
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab10/task2/liststudents/'

    return p

@login_required(login_url='/users/login/')
def listimages(request):
    q = Images.objects.filter().all
    return render(request, 'bookmodule/imageslist.html', {'images': q})

def deleteimage(request, id):
    try:
        image = Images.objects.get(id = id)
        m = f'The Image deleted successfully!'
        image.delete()
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab10/task3/listimages/'
    except Images.DoesNotExist:
        m = 'Something went wrong!'
        p = render(request, 'bookmodule/delete.html', {'message': m})
        p['Refresh'] = '3; url=/books/lab10/task3/listimages/'

    return p

def addimage(request):
    if request.method == 'POST':
        print("FILES:", request.FILES)  # Debug uploaded files
        print("CoverPage:", request.FILES.get('coverPage'))  # Check for specific file
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            print('here')
            form.save()
            p = render(request, 'bookmodule/addm.html', {'message': 'Image added successfully'})
            p['Refresh'] = '3; url=/books/lab10/task3/listimages/'
            return p
        print(form.errors)

    form = ImageForm(None)
    return render(request, 'bookmodule/addimage.html', {'form': form})

def lab12_1(request):
    return render(request, 'bookmodule/lab12-1.html')

def lab12_2(request):
    return render(request, 'bookmodule/lab12-2.html')

def lab12_3(request):
    return render(request, 'bookmodule/lab12-3.html')

def lab12_4(request):
    return render(request, 'bookmodule/lab12-4.html')