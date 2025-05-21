# TG-FileStream
# Copyright (C) 2025 Deekshith SH

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from urllib import parse

from telethon import events
from telethon.custom import Message

from tgfs.config import Config
from tgfs.telegram import client
from tgfs.utils import get_filename

log = logging.getLogger(__name__)

@client.on(events.NewMessage(incoming=True, func=lambda x: x.is_private and not x.file))
async def handle_text_message(evt: events.NewMessage.Event) -> None:
    await evt.reply("Send me any telegram file or photo I will generate a link for it")

@client.on(events.NewMessage(incoming=True, func=lambda x: x.is_private and x.file))
async def handle_file_message(evt: events.NewMessage.Event) -> None:
    fwd_msg: Message = await evt.message.forward_to(Config.BIN_CHANNEL)
    url = f"{Config.PUBLIC_URL}/{fwd_msg.id}/{parse.quote(get_filename(evt))}"
    await evt.reply(url)
    log.info("Generated Link %s", url)
