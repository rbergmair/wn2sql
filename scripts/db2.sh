#!/bin/sh



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



for VAL in *.bz2
do
  TABLENAME=`echo $VAL | sed "s/.bz2//g"`;
  echo "DELETE FROM $TABLENAME"
  echo "COMMIT"
  i=0
  bzcat $VAL | {
      while read STATEMENT 
      do
        STATEMENT=`echo $STATEMENT | sed "s/<apo>/''/g"`
        STATEMENT=`echo $STATEMENT | sed "s/<apo1>/''/g"`
        STATEMENT=`echo $STATEMENT | sed "s/<apo2>/''/g"`
        STATEMENT=`echo $STATEMENT | sed "s/<com>/,/g"`
        echo "INSERT INTO $TABLENAME VALUES $STATEMENT"

	# this is to make sure the transaction-log doesn't
 	# overflow, when inserting so many records in a single transaction.
        i=`expr $i + 1`
	if [ $i -eq 100 ]
        then
          echo "COMMIT"
          i=0
        fi
      done
    }
  echo "COMMIT"
done



#
# (c) Copyright 2002 -- 2007 by Richard Bergmair
#
