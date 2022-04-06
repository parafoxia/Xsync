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

import xsync

# Functions


@xsync.maybe_async()
def func(text):
    return text[::-1]


async def _async_func(text):
    return text[::-1]


class MockObject:
    def __init__(self, sync=None):
        self.sync = sync

    @xsync.maybe_async()
    def meth(self, text):
        return text[::-1]

    async def _async_meth(self, text):
        return text[::-1]

    @classmethod
    @xsync.maybe_async()
    def from_love(cls):
        return MockObject(sync=True)

    @classmethod
    async def _async_from_love(cls):
        return MockObject(sync=False)


def test_sync_function():
    assert func("xsync") == "cnysx"


async def test_async_function():
    assert await func("xsync") == "cnysx"
    assert await _async_func("xsync") == "cnysx"


def test_sync_method():
    t = MockObject()
    assert t.meth("xsync") == "cnysx"


async def test_async_method():
    t = MockObject()
    assert await t.meth("xsync") == "cnysx"
    assert await t._async_meth("xsync") == "cnysx"


def test_sync_classmethod():
    t = MockObject.from_love()
    assert t.sync


async def test_async_classmethod():
    t1 = await MockObject.from_love()
    assert not t1.sync

    t2 = await MockObject._async_from_love()
    assert not t2.sync
