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
from functools import wraps

from xsync import errors
from xsync.utils import get_fname

if t.TYPE_CHECKING:
    from xsync.types import DecoT, FuncT, MappingT

log = logging.getLogger(__name__)
mapping: MappingT = {}


def as_hybrid() -> DecoT:
    def decorator(func: FuncT) -> FuncT:
        fname = get_fname(func)
        mapping[fname] = None

        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            ctx = inspect.stack()[1].code_context

            if not ctx or "await" not in ctx[0]:
                return func(*args, **kwargs)

            coro = mapping[fname]
            if not coro:
                raise errors.NoAsyncImplementation(func)
            return coro(*args, **kwargs)

        return wrapper

    return decorator


def set_async_impl(func: FuncT) -> DecoT:
    def decorator(coro: FuncT) -> FuncT:
        fname = get_fname(func, coro)

        if fname not in mapping:
            raise errors.NotHybridCallable(func, coro)

        mapping[fname] = coro

        @wraps(coro)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return coro(*args, **kwargs)

        return wrapper

    return decorator
