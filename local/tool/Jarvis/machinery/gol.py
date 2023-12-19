# Copyright [pythonJaRvis] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-


def _init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    _global_dict[key] = value


def get_value(key, defValue=0):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue


def add_value(key):
    if key not in _global_dict:
        _global_dict[key] = 1
    else:
        _global_dict[key] = _global_dict[key] + 1


def transfer():
    print(_global_dict)
