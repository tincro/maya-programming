# Decorators are functions that wrap other functions

def foo():
    print("This is a foo")

# if we run foo, it will print, "This is a foo"
print("\n\n-----------------------\nCalling Foo without any wrappers\n")
foo()
# this should give us back the name of foo which is Foo
print(foo.__name__)

# But now lets say we want to always wrap foo inside some other logic.
# We'll create another function and call it spam that takes a functions

def spam(func):
    print("This is spam")
    # We capture the value returned by Foo
    value = func()
    # Then we finish up
    print("Spam is done")
    # and finally return the value
    return value

# We can now wrap foo when we call it
# This should print
# This is Spam
# This is Foo
# Spam is done
print("\n\n----------------------\nCalling foo directlly wrapped by spam\n")
spam(foo)

# but we have to remember to do this everytime we call Foo
# Another way to do this is to wrap foo and hold it as a new Foo
# so lets make a second spam, called deferSpam

# so first we define the outer layer that will create a new function
def deferSpam(func):
    # this function will wrap around Foo
    # We don't know what arguments foo will take if any,
    # so we just capture every argument just in case and give it to foo to deal with
    def wrapperSpam(*args, **kwargs):
        # inside this generated function, we'll do everything we did in Spam
        print("This is wrapperSpam spam")
        # Just like above we store the value returned by Foo
        value = func(*args, **kwargs)
        # Then finish up and return that value
        print("wrapper Spam is done")
        return value

    # The outer function then returns the newly created function that wraps around Foo
    return wrapperSpam

# We can then wrap foo forever by doing this
# Now foo will actually be a copy of wrapperSpam that knows to call Foo
print("\n\n----------------------\nCalling foo wrapped by wrapperSpam created by deferSpam\n")
foo = deferSpam(foo)

# So if I call foo Now
# this should print:
# This is spam
#This is foo
# Spam is done
foo()

# in fact we can check stuff about Foo
print("\n\n-------------------\n")
# This tell us that foo is now actually fwrapperSpam
print(foo.__name__)

# This is kind of ugly, so a better way to do it so like so
# Lets create a new functions
# We can wrap it directly by deferSpam using the @ symbol
# This is a python syntax for doing the wrapping we did above at definition time
@deferSpam
def hello(name):
    print("Hello, %s" % name)

# Now lets call it
print("\n\n-------------------------\nCalling hello wrapped by wrapperSpam created by deferSpam\n")
# This should print
#This is Spam
# Hello, David
# Spam is done
hello('David')
print hello.__name__

# so lets import something to help us out here instead
# Typically for decorators we also make use of the functools.wraps functions
# This itself is a decorator that fixes some issues with Decorators

from functools import wraps

# Lets create a new wrappers
def eggs(func):
    # But this time we use functools.wraps as a decorator and give it the func arguments
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Then we make the decorator as we did above
        print("this is eggs")
        ret = func(*args, **kwargs)
        print("Eggs is done")
        return ret

    return wrapper

# now lets make a new function and add the eggs decorators
@eggs
def goodbye(name):
    print("Goodbye, %s" % name)

# Lets call it
# This will print
#This is Eggs
#Goodbye, Mary
# Eggs is done
goodbye('Mary')
# But now lets check the __name__
# This will now print Goodbye
print(goodbye.__name__)

# And thats the beauty of fucntools.wraps 
# It can hide the fact that our function was evver decorated
# this is very useful because now any code that wants to know the original function doesn't have to search for it
# it can jsut call it like it was never decorated
# this is great for functions like help() in python that need to know the original functions docstrings etc...
