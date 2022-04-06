# Xsync

A set of tools to create hybrid sync/async interfaces.

CPython versions 3.7 through 3.11-dev and PyPy versions 3.7 through 3.9 are officially supported.

Windows, MacOS, and Linux are all supported.

## What does *Xsync* do?

*Xsync* allows developers to create dynamic interfaces which can be run in sync or async contexts.

In simple terms, it makes this possible:

```py
result = my_function()
result = await my_function()
```

How neat is that?!

## Usage

The above behaviour can be achieved with the `as_hybrid` decorator:

```py
@xsync.as_hybrid()
def my_function():
    ...
```

This sets `my_function` up as a "hybrid callable", which is capable of being run both synchronously and asynchronously.
However, we also need to set an async implementation for `my_function` for it to work.
We can do this using the `set_async_impl` decorator:

```py
@xsync.set_async_impl(my_function)
async def my_async_function():
    ...
```

Doing this tells *Xsync* to run this function instead of `my_function` when awaiting:

```py
my_function()        # runs as normal
await my_function()  # calls `my_async_function` instead
```

Don't worry, `my_async_function` can still be run directly, as you'd expect.

It also works on methods, class methods, and static methods:

```py
class MyClass:
    @xsync.as_hybrid()
    def my_method(self):
        ...

    @xsync.set_async_impl(my_method)
    async def my_async_method(self):
        ...

    @classmethod
    @xsync.as_hybrid()
    def my_class_method(cls):
        ...

    @classmethod
    @xsync.set_async_impl(my_class_method)
    async def my_async_class_method(cls):
        ...

    @staticmethod
    @xsync.as_hybrid()
    def my_static_method(cls):
        ...

    @staticmethod
    @xsync.set_async_impl(my_static_method)
    async def my_async_static_method(cls):
        ...
```

***

The above is the newer (and better) of two available implementations.

<details>
<summary>View the old implementation</summary>

The above behaviour can be achieved with the `maybe_async` decorator:

```py
@xsync.maybe_async()
def my_function():
    ...
```

This sets `my_function` up as a "hybrid callable", which is capable of being run both synchronously and asynchronously.
However, we also need to set an async implementation for `my_function` for it to work.
We can do this by creating another function of the same name, but with an `_async_` prefix:

```py
async def _async_my_function():
    ...
```

*Xsync* searches for a function with the name of the original function prefixed by `_async_` at runtime, and runs this instead when awaiting:

```py
my_function()        # runs as normal
await my_function()  # calls `_async_my_function` instead
```

It also works on methods and class methods:

```py
class MyClass:
    @xsync.maybe_async()
    def my_method(self):
        ...

    async def _async_my_method(self):
        ...

    @classmethod
    @xsync.maybe_async()
    def my_class_method(cls):
        ...

    @classmethod
    async def _async_my_class_method(cls):
        ...
```

**This implementation does not work with static methods.**
</details>

## Contributing

Contributions are very much welcome! To get started:

* Familiarise yourself with the [code of conduct](https://github.com/parafoxia/analytix/blob/main/CODE_OF_CONDUCT.md)
* Have a look at the [contributing guide](https://github.com/parafoxia/analytix/blob/main/CONTRIBUTING.md)

## License

The *Xsync* module for Python is licensed under the [BSD 3-Clause License](https://github.com/parafoxia/Xsync/blob/main/LICENSE).
