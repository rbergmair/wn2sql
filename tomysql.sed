#
# wordnet2sql: software to convert data from WordNet(R)'s-Format to
#              an SQL-Script for a relational DBMS.
# Copyright (C) 2002 -- 2007 Richard Bergmair
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#



s/'//g
s/<apo>/\\'/g
s/<apo1>/\\`/g
s/<apo2>/\\´/g
s/^(//g
s/)$//g
s/NULL, /\\N	/g
s/, /	/g
s/<com>/,/g



#
# (c) Copyright 2002 -- 2007 by Richard Bergmair
#
