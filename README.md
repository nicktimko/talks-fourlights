# How many lights do you see?

&bull; **Quick Links** &bull;
[Slides][slides] &bull;
[Notebook](./romulan-mind-probe.ipynb) &bull;

## Gentle Interrogation

Python's introspective features can also be used to some extent. `sys.getsizeof(1)` reports `28` on the Python 3.7 I built on x86_64 Ubuntu 18.04, but `id(2) - id(1)` is `32`. What gives? Probably 8 byte (64-bit) [alignment][wiki-x86align] for the sake of processor access.


## Romulan Mind Probe Findings

Repo: `python/cpython`, Path: `Include/object.h`

```c
typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
} PyObject;
```

`_PyObject_HEAD_EXTRA` is nothing unless compiled with debug options:

```c
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

That question probably (certainly) came from 1984, which was in-turn from various ["2 + 2 = 5" propaganda][wiki-2-2-5] (not always overtly denying reality any more than, for example, ["26 + 6 = 1"][wiki-unitedireland])

It was reimagined in the *ST:TNG* episode "The Chain of Command". *Our hero* Jean-Luc Picard (Winston Smith from 1984) was captured by the totalitarian Cardassians (the Ingsoc Party) and his interrogator Gul Madred (O'Brien) tries to convince him that there are 5 lights (fingers) when in fact there are only 4.

### The Chain of Command

> [JEAN-LUC] PICARD: I've told you all that I know.
>
> [GUL] MADRED: Yes, I'm sure you have. (he turns on four spotlights behind his desk) How many lights do you see there?
>
> PICARD: I see four lights.
>
> MADRED: No, there are five. Are you quite sure?
>
> PICARD: There are four lights.
>
> MADRED: Perhaps you're aware of the incision on your chest. While you were under the influence of our drugs, you were implanted with a small device. It's a remarkable invention. By entering commands in this PADD, I can produce pain in any part of your body at various levels of severity. Forgive me. I don't enjoy this but I must demonstrate. It will make everything clearer.
>
> (Picard falls to his knees in agony)
>
> MADRED: Surprising, isn't it? Most people feel at first that they can steel themselves against it but they're completely unprepared for the intensity of the pain. That was the lowest possible setting.
>
> PICARD: I know nothing about Minos Korva.
>
> MADRED: But I've told you that I believe you. I didn't ask you about Minos Korva. I asked how many lights you see.
>
> PICARD: There are four lights.
>
> MADRED: I don't understand how you can be so mistaken.
>
> &mdash; Abatemarco, Frank (Writer) & Landau, Les (Director). (1992). [The Chain of Command - Part 2][tng-coc-wiki] [Television series episode] In *Star Trek: The Next Generation*. Paramount Domestic Television. [Transcript][tng-coc-transcript]


### 1984
> 'Do you remember,' he went on, 'writing in your diary, "Freedom is the freedom to say that two plus two make four"?'
>
> 'Yes,' said Winston.
>
>O'Brien held up his left hand, its back towards Winston, with the thumb hidden and the four fingers extended.
>
>'How many fingers am I holding up, Winston?'
>
>'Four.'
>
>'And if the party says that it is not four but five -- then how many?'
>
>'Four.'
>
> The word ended in a gasp of pain. The needle of the dial had shot up to fifty-five. The sweat had sprung out all over Winston's body. The air tore into his lungs and issued again in deep groans which even by clenching his teeth he could not stop. O'Brien watched him, the four fingers still extended. He drew back the lever. This time the pain was only slightly eased.
>
> 'How many fingers, Winston?'
>
> &mdash; Orwell, George. (1949). [*Nineteen Eighty-Four: A novel*][n1984-wiki]. New York: Harcourt, Brace & Co. [Part 3, Chapter 2][n1984-p3ch2].

On the face it may be absurd, but if *our hero* can be broken and made to believe that it is *true*, then there's no extent to what else can be impressed onto them by the state. The [*blackwhite*][newspeak] will have set in.

[slides]: https://docs.google.com/presentation/d/1gngNbRzgzLHwjqd9YjppLrpt3g5tlRcMyx1quiqIR-8/edit?usp=sharing

[wiki-2-2-5]: https://en.wikipedia.org/wiki/2_%2B_2_%3D_5
[wiki-unitedireland]: https://en.wikipedia.org/wiki/United_Ireland
[wiki-x86align]: https://en.wikipedia.org/wiki/Data_structure_alignment#Typical_alignment_of_C_structs_on_x86

[n1984-p3ch2]: http://www.george-orwell.org/1984/18.html
[n1984-wiki]: https://en.wikipedia.org/wiki/Nineteen_Eighty-Four
[newspeak]: https://en.wikipedia.org/wiki/Newspeak#Vocabulary

[tng-coc-wiki]: https://en.wikipedia.org/wiki/Chain_of_Command_(Star_Trek:_The_Next_Generation)
[tng-coc-transcript]: http://www.chakoteya.net/NextGen/237.htm
