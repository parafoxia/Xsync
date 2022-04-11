# Copyright (c) 2022-present, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import inspect
import logging
import typing as t

_log = logging.getLogger(__name__)

if t.TYPE_CHECKING:
    AsyncT_co = t.TypeVar("AsyncT_co", bound="AsyncInitMixin", covariant=True)


class AsyncInitMixin:
    __ainit__: t.Callable[..., t.Any]
    _args: tuple[t.Any, ...]
    _kwargs: dict[str, t.Any]

    def __new__(
        cls: type[AsyncInitMixin], *args: t.Any, **kwargs: t.Any
    ) -> AsyncInitMixin:
        obj = super(AsyncInitMixin, cls).__new__(cls)
        orig_init = cls.__init__

        def __init__(self: AsyncInitMixin, *args: t.Any, **kwargs: t.Any) -> None:
            ctx = inspect.stack()[1].code_context

            if not ctx or "await" not in ctx[0]:
                _log.debug(f"Initialising {cls.__name__!r} normally")
                return orig_init(obj, *args, **kwargs)

            cls._args = args
            cls._kwargs = kwargs

        setattr(cls, "__init__", __init__)

        if not hasattr(cls, "__ainit__"):

            async def __ainit__(self: AsyncInitMixin) -> None:
                ...

            setattr(cls, "__ainit__", __ainit__)

        return obj

    def __await__(self: AsyncT_co) -> t.Generator[t.Any, t.Any, AsyncT_co]:
        async def main() -> AsyncInitMixin:
            _log.debug(f"Initialising {self.__class__.__name__!r} asynchronously")
            await self.__ainit__(*self.__class__._args, *self.__class__._kwargs)
            del self.__class__._args
            del self.__class__._kwargs
            return self

        return main().__await__()  # type: ignore
