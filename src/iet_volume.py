#!/usr/bin/python

# This file is part of IETView
#
# IETView is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IETView is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IETView.  If not, see <http://www.gnu.org/licenses/>.

import re
import iet_target

class IetVolume(object):
    def __init__(self, tid, target):
        self.tid = tid
        self.target = target

        self.luns = {}

    def add_lun(self, lun):
        self.luns[lun.number] = lun

    def get_lun_ids_by_path(self, path):
        luns = self.luns
        return [key for key in luns if path==luns[key].path]


#Get running volumes from volumes file
class IetVolumes(object):
    TARGET_REGEX='tid:(?P<tid>\d+)\s+name:(?P<target>.+)'
    LUN_REGEX='lun:(?P<lun>\d+)\s+state:(?P<state>\d+)\s+iotype:(?P<iotype>\w+)\s+iomode:(?P<iomode>\w+)\s+blocks:(?P<blocks>\d+)\s+blocksize:(?P<blocksize>\d+)\s+path:(?P<path>.+)'
    def __init__(self, filename):
        self.volumes = {}
        self.filename = filename

    def parse_file(self):
        f = file(self.filename, "r")

        tv = None

        for line in f:
            m = re.search(self.TARGET_REGEX, line)
            if m:
                tv = IetVolume(int(m.group('tid')), m.group('target'))
                self.volumes[tv.tid] = tv

            m = re.search(self.LUN_REGEX, line)

            if m:
                tv.add_lun(iet_target.IetLun(number=int(m.group('lun')),
                    state=int(m.group('state')),
                    iotype=m.group('iotype'), iomode=m.group('iomode'),
                    path=m.group('path')))

        f.close()

