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

if t.TYPE_CHECKING:
    FuncT = t.Callable[..., t.Any]
    WrapperT = FuncT
    DecoratorT = t.Callable[[FuncT], WrapperT]

log = logging.getLogger(__name__)


def maybe_async() -> DecoratorT:
    def decorator(func: FuncT) -> WrapperT:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            ctx = inspect.stack()[1].code_context

            if not ctx or "await" not in ctx[0]:
                log.info(f"Selected {func.__qualname__} to run (sync)")
                return func(*args, **kwargs)

            if args:
                # Account for classmethods.
                n = args[0].__class__.__name__
                clsname = n if n != "type" else args[0].__name__

                if func.__qualname__.split(".")[0] == clsname:
                    meth = getattr(args[0], f"_async_{func.__name__}")
                    log.info(f"Selected {meth.__qualname__} to run (async meth)")
                    return meth(*args[1:], **kwargs)

            meth = func.__globals__[f"_async_{func.__name__}"]
            log.info(f"Selected {meth.__qualname__} to run (async func)")
            return meth(*args, **kwargs)

        return wrapper

    return decorator
