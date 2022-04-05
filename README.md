# Xsync

A set of tools to create hybrid sync/async interfaces.

CPython versions 3.7 through 3.11-dev and PyPy versions 3.7 through 3.9 are officially supported.

Windows, MacOS, and Linux are all supported.

## What does *Xsync* do?

*Xsync* allows developers to create dynamic interfaces which can be run in sync or async contexts.

We'll use reading a text file as an example. Normally, users would have to use different function/method names depending on whether it was sync or async:

```py
read_file("How are you?")
await read_file_async("How are you?")
```

However, with *Xsync*, users don't have to worry about that:

```py
read_file("I'm great thanks!")
await read_file("I'm great thanks!")
```

This provides a slick and dynamic interface which is oftentimes far more intuitive.

## Usage

Hybrid interfaces can be created with the help of *Xsync*'s `maybe_async` decorator:

```py
import aiofiles
import xsync

@xsync.maybe_async()
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

async def _async_read_file(path: str) -> str:
    async with aiofiles.open(path) as f:
        return await f.read()
```

Here, `read_file` and `_async_read_file` are sync and async implementations of the same action.
The `maybe_async` decorator would determine which of the two to run at runtime, based on whether the code is running in an async context.

So `read_file` would be executed when doing the following...

```py
read_file("path/to/file")
```

...but `_async_read_file` would be executed when doing the following instead:

```py
await read_file("path/to/file")
```

The `_async_` prefix is important, as this is what *Xsync* uses to find async implementations.

This also works with methods within classes (as well as classmethods, provided the `classmethod` decorator is above the `maybe_async` one):

```py
import xsync

class Reader:
    @xsync.maybe_async()
    def read_file(self, path: str) -> str:
        ...

    async def _async_read_file(self, path: str) -> str:
        ...
```

## Contributing

Contributions are very much welcome! To get started:

* Familiarise yourself with the [code of conduct](https://github.com/parafoxia/analytix/blob/main/CODE_OF_CONDUCT.md)
* Have a look at the [contributing guide](https://github.com/parafoxia/analytix/blob/main/CONTRIBUTING.md)

## License

The *Xsync* module for Python is licensed under the [BSD 3-Clause License](https://github.com/parafoxia/Xsync/blob/main/LICENSE).
