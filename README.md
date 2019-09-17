# ssh-mv

## What?

`ssh-mv` is a wrapper script for moving remote files visible on a
local filesystem (for example with NFS) via SSH.  Let me explain why
it's useful.

## Why?

My use case was pretty simple.  I own a NAS (network-attached storage)
with multiple file shares mounted separately as distinct filesystems
that I sometimes need to move files between.  As they are viewed as
separate filesystems by my operating systems, it cannot utilize the
fact that all these file shares are actually a single filesystem on
the NAS.  When I move the files between the shares, they need to be
physically moved from the NAS to my PC and from my PC back to the NAS,
instead of making a simple rename.

I used to manually log in via SSH onto my NAS and move the files there
but that's inconvenient.  And that's exactly what `ssh-mv` does: it
converts the supplied local paths onto the server paths and runs
`mv(1)` directly on the NAS, which is much faster for such cases.

## How?

There are two prerequisites:

1. Your NAS needs to support SSH logins.
2. Your mountpoints need to be named just like the file shares they
   represent.

To use `ssh-mv`, modify the beginning of the script, specifically the
`LOCAL_ROOT`, `REMOTE_ROOT` and `REMOTE_HOST` constants, to contain
the path where the NFS mounts live, path where the same files reside
on the remote filesystem and the hostname of the NAS to connect to,
respectively.

The default `REMOTE_ROOT` should work for QNAP devices though you
still need to provide the other two values.

Afterwards you can use `ssh-mv` just like you would use `mv(1)` for
the mentioned cases.  It will print the "expanded" paths for debug
purposes and call `mv(1)` on the server.

## Who?

Copyright (C) 2019  Wojciech Siewierski

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
