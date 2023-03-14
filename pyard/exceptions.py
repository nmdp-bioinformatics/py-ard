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
class PyArdError(Exception):
    """
    Base Class for All py-ard Errors
    """

    def __init__(self, message: str) -> None:
        self.message = message


class InvalidAlleleError(PyArdError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"Invalid Allele: {self.message}"


class InvalidMACError(PyArdError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"Invalid MAC Code: {self.message}"


class InvalidTypingError(PyArdError):
    def __init__(self, message: str, cause=None) -> None:
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        return f"Invalid HLA Typing: {self.message}"
