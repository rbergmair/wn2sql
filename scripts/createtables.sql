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



-- DROP TABLE word;
-- DROP TABLE synset;
-- DROP TABLE sense;
-- DROP TABLE lexrel;
-- DROP TABLE semrel;

-- DROP TABLE reltype;
-- DROP TABLE lexname;

-- DROP TABLE sample;
-- DROP TABLE adjmod;
-- DROP TABLE lexverbframe;
-- DROP TABLE semverbframe;
-- DROP TABLE frame;



--
-- core tables
--

CREATE TABLE word (
  wordno INTEGER NOT NULL,
  lemma VARCHAR(80) NOT NULL
);

CREATE TABLE synset (
  synsetno INTEGER NOT NULL,
  definition VARCHAR(550),
  lexno SMALLINT NOT NULL
);

CREATE TABLE sense (
  wordno INTEGER NOT NULL,
  synsetno INTEGER NOT NULL,
  tagcnt SMALLINT NOT NULL
);

CREATE TABLE lexrel (
  wordno1 INTEGER NOT NULL,
  synsetno1 INTEGER NOT NULL,
  wordno2 INTEGER NOT NULL,
  synsetno2 INTEGER NOT NULL,
  reltypeno SMALLINT NOT NULL
);

CREATE TABLE semrel (
  synsetno1 INTEGER NOT NULL,
  synsetno2 INTEGER NOT NULL,
  reltypeno SMALLINT NOT NULL
);



--
-- explanatory tables
--

CREATE TABLE reltype (
  reltypeno SMALLINT NOT NULL,
  typeno CHAR(1) NOT NULL,
  description VARCHAR(50)
);

CREATE TABLE lexname (
  lexno SMALLINT NOT NULL,
  lexname VARCHAR(30),
  description VARCHAR(80)
);



--
-- additional data including explanatory tables
--

CREATE TABLE sample (
  synsetno INTEGER NOT NULL,
  sampleno SMALLINT NOT NULL,
  samp VARCHAR(550) NOT NULL
);

CREATE TABLE adjmod (
  synsetno INTEGER NOT NULL,
  wordno INTEGER NOT NULL,
  modifier CHAR(2) NOT NULL
);

CREATE TABLE lexverbframe (
  synsetno INTEGER NOT NULL,
  wordno INTEGER NOT NULL,
  frameno SMALLINT NOT NULL
);

CREATE TABLE semverbframe (
  synsetno INTEGER NOT NULL,
  frameno SMALLINT NOT NULL
);

CREATE TABLE frame (
  frameno SMALLINT NOT NULL,
  description VARCHAR(50)
);



--
-- (c) Copyright 2002 -- 2007 by Richard Bergmair
--
