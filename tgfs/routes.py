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
import asyncio
from aiohttp import web

from tgfs.telegram import multi_clients
from tgfs.utils import FileInfo

log = logging.getLogger(__name__)
routes = web.RouteTableDef()

client_selection_lock = asyncio.Lock()

@routes.get("/")
async def handle_root(_: web.Request):
    return web.json_response({key: [val.active_clients, val.users] for key, val in multi_clients.items()})

@routes.get(r"/{msg_id:-?\d+}/{name}")
async def handle_file_request(req: web.Request) -> web.Response:
    head: bool = req.method == "HEAD"
    msg_id = int(req.match_info["msg_id"])
    file_name = req.match_info["name"]

    transfer = None
    client_id = None

    async with client_selection_lock:
        client_id = min(multi_clients, key=lambda k: multi_clients[k].active_clients)
        transfer = multi_clients[client_id]
        transfer.active_clients += 1
        log.debug("Selected client %d for %s. Active downloads for this client: %d", client_id, file_name, transfer.active_clients)

    file: FileInfo = await transfer.get_file(msg_id, file_name)
    if not file:
        log.warning("File not found for msg_id %d, name %s using client %d", msg_id, file_name, client_id)
        return web.Response(status=404, text="404: Not Found")

    size = file.file_size
    from_bytes = req.http_range.start or 0
    until_bytes = (req.http_range.stop or size) - 1

    if (until_bytes >= size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(status=416, headers={"Content-Range": f"bytes */{size}"})

    if head:
        body=None
    else:
        body=transfer.download(file.location, file.dc_id, size, from_bytes, until_bytes)

    return web.Response(
        status=200 if (from_bytes == 0 and until_bytes == size - 1) else 206,
        body=body,
        headers={
        "Content-Type": file.mime_type,
        "Content-Range": f"bytes {from_bytes}-{until_bytes}/{size}",
        "Content-Length": str(until_bytes - from_bytes + 1),
        "Content-Disposition": f'attachment; filename="{file_name}"',
        "Accept-Ranges": "bytes",
    })
