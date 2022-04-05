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
def function():
    return "sync"


async def _async_function():
    return "async"


def test_sync_function():
    assert function() == "sync"


async def test_async_function():
    assert await function() == "async"


# Classmethods


class MockObject:
    def __init__(self, sync=None):
        self.sync = sync

    @xsync.maybe_async()
    def method(self):
        return "sync"

    async def _async_method(self):
        return "async"

    @classmethod
    @xsync.maybe_async()
    def from_whatever(cls):
        print("sync clsmth")
        return MockObject(sync=True)

    @classmethod
    async def _async_from_whatever(cls):
        print("async clsmth")
        return MockObject(sync=False)


def test_sync_method():
    t = MockObject()
    assert t.method() == "sync"


async def test_async_method():
    t = MockObject()
    assert await t.method() == "async"


def test_sync_classmethod():
    t = MockObject.from_whatever()
    assert t.sync


async def test_async_classmethod():
    t = await MockObject.from_whatever()
    assert not t.sync
