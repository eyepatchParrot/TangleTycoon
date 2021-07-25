```
```

We make sure that we handle having code blocks as the first line correctly.
This also ensures that if no extension is present, we are OK.

# Hello world
Below, we demonstrate associating each language with the appropriate file,
combining the default cpp stream and handling foo.h separately.

```cpp
#include "foo.h"
```

```cpp stream=header
void hello_world();
```

```cpp stream=impl name=impl-body dep=impl-def
    std::cout << "Hello world\n";
}
```

```cpp stream=impl name=impl-inc
#include "foo.h"
#include <iostream>
```

```cpp stream=impl name=impl-def dep=impl-inc
void hello_world() {
```

Something we want to ensure happens is that indenting is handled
naturally.  For example, all of the hello-world indenting in the above
macro should be aligned based on the indent of the comment.  In the macro
itself, either use the indent of the first line or require zero indent.

```
this is a generic code block
```

```python
print("Hello world")
```

```cpp
int main() {
    hello_world();
}
```

The next step is to ensure that we can macro appropriately. This means
that we should be able to include a snippet out of order and it injects
appropriately.

Something to look for is to make sure that I'm handling whitepace and
stripping appropriately in the header line.

We can think of this as having positional arguments. For example, in a
block's header, you might have: `cpp impl my-tag`. However, just as valid
would be: `cpp macro:my-macro key:impl` which reverses the order since
the arguments are keyword arguments.  This forbids : from tags and such
since it's hard to tell the difference between a key `macro:my-macro`
and a keyword argument. `:` also collides with Bazel configuration So,
maybe `/` would be a better divider?

I wonder if this would be an interesting fit for SQL since it has a
macro system.

The reasoning for doing this with file keys rather than using file names
directly is to integrate with Bazel which wants control over the location
of outputs.
