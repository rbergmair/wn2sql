-- $Id: insert.mysql.sql,v 1.1 2002/08/13 20:19:44 bergmair1 Exp $

--
-- wordnet2sql: software to convert data from WordNet(R)'s-Format to
--              an SQL-Script for a relational DBMS.
-- Copyright (C) 2002 Richard Bergmair
--
-- This program is free software; you can redistribute it and/or
-- modify it under the terms of the GNU General Public License
-- as published by the Free Software Foundation; either version 2
-- of the License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
--

LOAD DATA INFILE 'word.mysql' INTO TABLE word;
LOAD DATA INFILE 'synset.mysql' INTO TABLE synset;
LOAD DATA INFILE 'sense.mysql' INTO TABLE sense;
LOAD DATA INFILE 'lexrel.mysql' INTO TABLE lexrel;
LOAD DATA INFILE 'semrel.mysql' INTO TABLE semrel;

LOAD DATA INFILE 'reltype.mysql' INTO TABLE reltype; 
LOAD DATA INFILE 'lexname.mysql' INTO TABLE lexname;

LOAD DATA INFILE 'sample.mysql' INTO TABLE sample;
LOAD DATA INFILE 'adjmod.mysql' INTO TABLE adjmod;
LOAD DATA INFILE 'lexverbframe.mysql' INTO TABLE lexverbframe;
LOAD DATA INFILE 'semverbframe.mysql' INTO TABLE semverbframe;
LOAD DATA INFILE 'frame.mysql' INTO TABLE frame;

--
-- (c) Copyright 2002 by Richard Bergmair
--
