TangleTycoon
=============

TangleTycoon is another tool for generating code files from Markdown.
My motivation for it is to merge documentation with some integration
tests allowing for tutorials which compile for any language.  Given an
input markdown on stdin, group code blocks into streams, re-ordering
them based on future dependencies.  A stream is a set of code blocks
which get accumulated to be written to a file specified by a map from
streams to paths.

```sh
< README.md tangletycoon.py --force --cpp main.cpp
```

Here, we send this readme to tangletycoon and write the default C++
stream to main.cpp.  Our force flag is required since we didn't specify
paths for other streams, such as the above shell block. So, we don't
error when this is mising.

## Macros

Given an input markdown on stdin, group each code block into streams and macros.

1. A macro is a code block which gets expanded
2. A stream is a set of code blocks which get accumulated to be written to a file specified by a map from streams to paths.

Macro expansion is delimited by surrounding the name of the macro with 3 of the comment identifier for the language of the code block.
If a link is used, then the fragment is extracted instead.
```python
### expand-python ###
```
```cpp
/// [](#expand-cpp) ///
```

To Do
-----

1. Add macros
2. Handle recursion with a visited set and error.
3. Handle keyword arguments. Positional arguments are in a fixed order, so track which is the next remaining one, and use that one.

I don't think that I actually need macros. Languages already have mechanisms for duplicating code. I can instead have 3 items:

1. What stream does this belong to? Default to lang stream.
2. What is the name of this block? Default to anonymous.
3. What does this depend on in the same stream?

So, the header is `lang stream name dep...`

If we make sure that resolution of dependencies happens in file order, then the case where nothing is specified results in a file per language in order.


Design decisions
----------------

### Why the syntax for referencing macros?
[noweb syntax](https://en.wikipedia.org/wiki/Noweb#Example_of_a_simple_Noweb_program) is pretty well known for referencing macros. (Chunks in noweb terminology.)
However, the use of any particular set of symbols means that rendering of code **prior** to being tangled may break the handling thereof.

### Why input on stdin?
stdin input makes it easier to manipulate the markdown files before they
get into TangleTycoon. For example, supporting multiple inputs just using
`cat`.

### Why separate file paths from streams?
TangleTycoon targets first class support for Bazel which wants control
over output file paths.

### Inline outputs
TangleTycoon does not calculate results and inline them because it
focuses on not needing to understand target languages and focusing on
support for compiled languages and C++ in particular. Maybe with a DSL
where you specify functions and mark that they should be invoked and
the output serialized to string based on the type of the result, but
then you have to integrate that with each language.  I'm not sure that
this complexity pays for itself. Rather, the way this could be handled
is using tests and asserts as seen below:

```cpp lib.h
inline add2(int x) {
    return x + 2;
}
```
```cpp name:add2 dep:test-main
assert(add2(2) == 4);
```
We can be sure of the result by adding a test with an assert for the
expected value. Since they're adjacent, the result is clear, but if we
care about the output of lib.h, it's not polluted with our results.

Alternatives considered
-----------------------

- [Org Babel](https://orgmode.org/worg/org-contrib/babel)
    - Leading literate coding environment
    - Targets org files rather than markdown which prevents integration with git hosts which only support markdown.
    - No support for sessions for C++ limiting tangling and weaving.
- Jupyter notebooks
    - Allows interleaving text with code and can have C++ support with xeus-cling
    - Personally had challenges with cling stability
    - Changing order of evaluation is done interactively, rather than repeatably.
    - Limited ability to generate multiple files automatically.
- [driusan/lmt](https://github.com/driusan/lmt)
    - Meets a lot of the requirements: markdown, C++.
    - I got inspiration here for using the header of the code block.
    - Macros are an interesting way of re-working the ordering and better for repeating sections of code.
    - Written in Go, but I don't have a Go compiler everywhere.
- [joakimmj/md-tangle](https://github.com/joakimmj/md-tangle)
    - Delimiting code blocks is by tilde rather than backticks as is more standard.
- [nuweb](http://nuweb.sourceforge.net) specifically targets latex.
- [noweb](https://www.cs.tufts.edu/~nr/noweb)
- [brokestream/tangle.py](http://brokestream.com/tangle.html) Not Markdown
- [Pweave]()
- [Sweave]()
- [NanoLP]()
