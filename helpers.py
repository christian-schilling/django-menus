
def branch(path):
    """
    Builds a tuple containing all path above this one.
    None of the returned paths or the given paths is required to
    actually have a corresponding Node.
    Expample:
    >>> branch("/a/b/c/")
    ('/', '/a/', '/a/b/', '/a/b/c/')
    """
    li = tuple(p for p in path.split('/') if p)
    return ('/',)+tuple('/'+'/'.join(li[:c])+'/' for c in range(1,len(li)+1))

