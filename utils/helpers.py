from itertools import islice


def loop_batched(iterable, n):
    """Batches iterable data into lists of length n.

    This function takes an iterable and divides it into batches of length `n`.
    The last batch may be shorter than the specified `n` if the remaining elements
    in the iterable are not divisible by `n`. It then yields each batch as a list,
    making them available for further processing.

    Args:
    iterable (any iterable): The data to be batched.
    n (int): The desired batch size. Must be >= 1.

    Yields:
    list: A list containing elements from the iterable in batches of size `n`.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch


resumes_urls_list = []
