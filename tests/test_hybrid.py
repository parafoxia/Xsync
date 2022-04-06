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

import pytest

import xsync
from xsync import errors


@xsync.as_hybrid()
def func(text):
    return text[::-1]


@xsync.set_async_impl(func)
async def async_func(text):
    return text[::-1]


class MockObject:
    def __init__(self, sync=None):
        self.sync = sync

    @xsync.as_hybrid()
    def meth(self, text):
        return text[::-1]

    @xsync.set_async_impl(meth)
    async def async_meth(self, text):
        return text[::-1]

    @classmethod
    @xsync.as_hybrid()
    def from_love(cls):
        return MockObject(sync=True)

    @classmethod
    @xsync.set_async_impl(from_love)
    async def async_from_love(cls):
        return MockObject(sync=False)


@xsync.as_hybrid()
def no_async_func(text):
    return text[::-1]


# ---


def test_sync_function():
    assert func("sync") == "cnys"


async def test_async_function():
    assert await func("async") == "cnysa"
    assert await async_func("not sync") == "cnys ton"


def test_sync_method():
    t = MockObject()
    assert t.meth("xsync") == "cnysx"


async def test_async_method():
    t = MockObject()
    assert await t.meth("xsync") == "cnysx"
    assert await t.async_meth("xsync") == "cnysx"


def test_sync_classmethod():
    t = MockObject.from_love()
    assert t.sync


async def test_async_classmethod():
    t1 = await MockObject.from_love()
    assert not t1.sync

    t2 = await MockObject.async_from_love()
    assert not t2.sync


async def test_no_async_implementation():
    assert no_async_func("xsync") == "cnysx"

    with pytest.raises(errors.NoAsyncImplementation) as exc:
        await no_async_func("xsync")
    assert (
        str(exc.value)
        == f"'no_async_func' does not have a defined async implementation"
    )


def test_async_impl_of_non_hybrid():
    def normal_func(text):
        return text[::-1]

    with pytest.raises(errors.NotHybridCallable) as exc:

        @xsync.set_async_impl(normal_func)
        def async_of_normal_func(text):
            return text[::-1]

    # Stupid closure -- only way to do this though.
    assert (
        str(exc.value)
        == f"'test_async_impl_of_non_hybrid.<locals>.normal_func' has not been registered as a hybrid callable"
    )
