Goal:
Process + Shared memory
mmap based sharing is most likely the multiprocessing package way
Observed through strace.

Tried on:
Python 3.6.9
Python 3.8.2

Use pyenv for python version management. It's very helpful.

Achieved using multiprocessing package
Ref:https://docs.python.org/3/library/multiprocessing.html

Known Issues:

1. How nested dicts work in in Managers!
    Ref: https://stackoverflow.com/questions/37510076/unable-to-update-nested-dictionary-value-in-multiprocessings-manager-dict
    For now, remove body from response!

    The below dict creation does not work
    response = {
        "statusCode" : 200,
        "body" : {"number" : output}
    }

To get the above dict using Managers:
    response['statusCode'] = 200
    response['body'] = {}
    o_dict = response['body']
    o_dict['number'] = output
    response['body'] = o_dict

It's rather a pain, but now way around it!

Managers provide a diverse interface, but are rather slow:
Ref: https://docs.python.org/3/library/multiprocessing.html
