#
#    py-ard
#    Copyright (c) 2023 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
import pyard


def before_all(context):
    context.ard = pyard.init("3440", data_dir="/tmp/py-ard")

    # an ard with ping set to True
    ping_config = {
        "ping": True,
    }
    context.ard_ping = pyard.init("3440", data_dir="/tmp/py-ard", config=ping_config)

    # an ard with ARS suffix for lg
    lg_ars_config = {
        "ARS_as_lg": True,
    }
    context.ard_ars = pyard.init("3440", data_dir="/tmp/py-ard", config=lg_ars_config)

    # use non-strict mode
    non_strict_config = {"strict": False}
    context.ard_non_strict = pyard.init(
        "3440", data_dir="/tmp/py-ard", config=non_strict_config
    )
