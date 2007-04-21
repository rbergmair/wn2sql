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
-- secondary indices
--
CREATE INDEX si_word_lemma ON word(lemma);
CREATE INDEX si_sense1 ON sense(wordno);
CREATE INDEX si_sense2 ON sense(synsetno);
CREATE INDEX si_lexrel1 ON lexrel(wordno1,synsetno1);
CREATE INDEX si_lexrel2 ON lexrel(wordno2,synsetno2);
CREATE INDEX si_semrel1 ON semrel(synsetno1);
CREATE INDEX si_semrel2 ON semrel(synsetno2);



--
-- (c) Copyright 2002 -- 2007 by Richard Bergmair
--
