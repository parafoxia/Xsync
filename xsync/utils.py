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

import sys
import typing as t
import warnings
from functools import wraps
from types import FunctionType

if t.TYPE_CHECKING:
    from xsync.types import DecoT, FuncT

warnings.simplefilter("once", DeprecationWarning)


def get_fname(func: FuncT, coro: FuncT | None = None) -> str:
    if sys.version_info >= (3, 10) or isinstance(func, FunctionType):
        return func.__qualname__

    # Class methods and static methods did not have a __qualname__ attr
    # before Python 3.10, but we can steal it from the coro function.
    base = ".".join(coro.__qualname__.split(".")[:-1])
    return f"{base}.{func.__func__.__name__}"


def deprecated(removal_version: str = "", replaced_with: str = "") -> DecoT:
    def decorator(func: FuncT) -> FuncT:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            msg = f"{func.__name__!r} is deprecated"
            if removal_version:
                msg += f", and will be removed in version {removal_version}"
            if replaced_with:
                msg += f" -- consider using {replaced_with!r} instead"

            warnings.warn(msg, DeprecationWarning)
            return func(*args, **kwargs)

        return wrapper

    return decorator
