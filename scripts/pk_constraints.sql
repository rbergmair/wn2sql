--
-- wordnet2sql: software to convert data from WordNet(R)'s-Format to
--              an SQL-Script for a relational DBMS.
-- Copyright (C) 2002 -- 2007 Richard Bergmair
--
-- This library is free software; you can redistribute it and/or
-- modify it under the terms of the GNU Lesser General Public
-- License as published by the Free Software Foundation; either
-- version 2.1 of the License, or (at your option) any later version.
--
-- This library is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
-- Lesser General Public License for more details.
--
-- You should have received a copy of the GNU Lesser General Public
-- License along with this library; if not, write to the Free Software
-- Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
--



--
-- primary keys
--
ALTER TABLE word ADD CONSTRAINT pk_word PRIMARY KEY(wordno);
ALTER TABLE synset ADD CONSTRAINT pk_synset PRIMARY KEY(synsetno);
ALTER TABLE sense ADD CONSTRAINT pk_sense PRIMARY KEY(wordno,synsetno);
ALTER TABLE lexrel ADD CONSTRAINT pk_lexrel PRIMARY KEY(wordno1,synsetno1,wordno2,synsetno2,reltypeno);
ALTER TABLE semrel ADD CONSTRAINT pk_semrel PRIMARY KEY(synsetno1,synsetno2,reltypeno);

ALTER TABLE reltype ADD CONSTRAINT pk_reltype PRIMARY KEY(reltypeno);
ALTER TABLE lexname ADD CONSTRAINT pk_lexname PRIMARY KEY(lexno);

ALTER TABLE sample ADD CONSTRAINT pk_sample PRIMARY KEY(synsetno,sampleno);
ALTER TABLE adjmod ADD CONSTRAINT pk_adjmod PRIMARY KEY(synsetno,wordno);
ALTER TABLE lexverbframe ADD CONSTRAINT pk_lexverbframe PRIMARY KEY(wordno,synsetno,frameno);
ALTER TABLE semverbframe ADD CONSTRAINT pk_semverbframe PRIMARY KEY(synsetno,frameno);
ALTER TABLE frame ADD CONSTRAINT pk_frame PRIMARY KEY(frameno);



--
-- (c) Copyright 2002 -- 2007 by Richard Bergmair
--
