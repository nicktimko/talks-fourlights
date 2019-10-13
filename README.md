# How many lights do you see?

&middot; **Quick Links** &middot; [Slides][slides] &middot;

## Romulan Mind Probe Findings

Repo: `python/cpython`, Path: `Include/object.h`

```c
typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
} PyObject;
```


`_PyObject_HEAD_EXTRA` is nothing unless compiled with debug options

```
#ifdef Py_TRACE_REFS
/* Define pointers to support a doubly-linked list of all live heap objects. */
#define _PyObject_HEAD_EXTRA            \
    struct _object *_ob_next;           \
    struct _object *_ob_prev;

#define _PyObject_EXTRA_INIT 0, 0,

#else
#define _PyObject_HEAD_EXTRA
#define _PyObject_EXTRA_INIT
#endif
```

a `PyObject` is inserted into every other definition via `PyObject_HEAD` preprocessor definition which is:
```c
/* PyObject_HEAD defines the initial segment of every PyObject. */
#define PyObject_HEAD                   PyObject ob_base;
```

## Dramatis Personae

* Gul Madred
* O'Brien


## Inspiration

Inspired by the [answer I produced](https://codegolf.stackexchange.com/a/28851/176) for "Write a program that makes 2 + 2 = 5" on Programming Puzzles and Code Golf StackExchange. In CPython 2 (which has slightly different memory structures, so it won't run in CPython 3), it was:

> ```python
> >>> patch = '\x312\x2D7'
> >>> import ctypes;ctypes.c_int8.from_address(id(len(patch))+8).value=eval(patch)
> >>> 2 + 2
> 5
> ```
>
> CPython uses the same memory location for any copy of the first few small integers (0-255 if memory serves). This goes in and directly edits that memory location via `ctypes`. patch is just an obfuscated "`12-7`", a string with length 4, which `eval`'s to 5.

That question probably (certainly) came from 1984.

Slightly more modern was a version of it reimagined in the *ST:TNG* episode "The Chain of Command". *Our hero* Jean-Luc Picard (Winston Smith from 1984) was captured by the totalitarian Cardassians (the Ingsoc Party) and his interrogator Gul Madred (O'Brien) tries to convince him that there are 5 lights (2 + 2 = 5) when in fact there are only 4.

On the face it may be absurd, but if *our hero* can be broken and made to believe that it is *true*, then there's no extent to what else can be impressed onto them by the state. The [*blackwhite*][newspeak] will have set in.

* Orwell, George. (1949). [*Nineteen Eighty-Four: A novel*][n1984-wiki]. New York: Harcourt, Brace & Co.

* Abatemarco, Frank (Writer) & Landau, Les (Director). (1992). [The Chain of Command - Part 2][tng-coc-wiki] [Television series episode] In *Star Trek: The Next Generation*. Paramount Domestic Television.
  * [Transcript][tng-coc-transcript]


[n1984-wiki]: https://en.wikipedia.org/wiki/Nineteen_Eighty-Four
[newspeak]: https://en.wikipedia.org/wiki/Newspeak#Vocabulary
[tng-coc-wiki]: https://en.wikipedia.org/wiki/Chain_of_Command_(Star_Trek:_The_Next_Generation
[tng-coc-transcript]: http://www.chakoteya.net/NextGen/237.htm
[slides]: https://docs.google.com/presentation/d/1gngNbRzgzLHwjqd9YjppLrpt3g5tlRcMyx1quiqIR-8/edit?usp=sharing
