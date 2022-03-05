# MIT License
#
# Copyright (c) 2022 Lonny Wong
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import iterm2
import asyncio
from trzsz.libs.utils import TrzszCallback

async def get_iterm2_session(connection):
    app = await iterm2.async_get_app(connection)
    session = app.current_window.current_tab.current_session
    await session.async_inject(b'Hello from iTerm2 Python API\n')
    return session

class TextProgressBar(TrzszCallback):
    def __init__(self):
        self.num = 0
        self.idx = 0
        self.name = ''
        self.size = 0
        self.session = iterm2.run_until_complete(get_iterm2_session)

    def on_num(self, num):
        self.num = num
        self._inject_to_iterm2(f'num: {num}\n')

    def on_name(self, name):
        self.idx += 1
        self.size = 0
        self.name = name
        self._inject_to_iterm2(f'name: {name}\n')

    def on_size(self, size):
        self.size = size
        self._inject_to_iterm2(f'size: {size}\n')

    def on_step(self, step):
        self._inject_to_iterm2(f'step: {step}\n')

    def on_done(self, name):
        self._inject_to_iterm2(f'done: {name}\n')

    def _inject_to_iterm2(self, data):
        asyncio.get_event_loop().run_until_complete(self.session.async_inject(data.encode('utf8')))
