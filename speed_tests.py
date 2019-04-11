import timeit


proper = timeit.timeit('people.test_print()', setup='import people', number=10)
fiat = timeit.timeit('people.test_fiat()', setup='import people', number=10)

print(proper, fiat)