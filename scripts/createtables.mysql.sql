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



DROP TABLE IF EXISTS word;
DROP TABLE IF EXISTS synset;
DROP TABLE IF EXISTS sense;
DROP TABLE IF EXISTS lexrel;
DROP TABLE IF EXISTS semrel;

DROP TABLE IF EXISTS reltype;
DROP TABLE IF EXISTS lexname;

DROP TABLE IF EXISTS sample; 
DROP TABLE IF EXISTS adjmod;
DROP TABLE IF EXISTS lexverbframe;
DROP TABLE IF EXISTS semverbframe;
DROP TABLE IF EXISTS frame;



--
-- core tables
--

CREATE TABLE word (
  wordno DECIMAL(6) NOT NULL,
  lemma VARCHAR(80) NOT NULL
);

CREATE TABLE synset (
  synsetno DECIMAL(6) NOT NULL,
  definition MEDIUMTEXT,
  lexno DECIMAL(2) NOT NULL
);

CREATE TABLE sense (
  wordno DECIMAL(6) NOT NULL,
  synsetno DECIMAL(6) NOT NULL,
  tagcnt DECIMAL(5) NOT NULL
);

CREATE TABLE lexrel (
  wordno1 DECIMAL(6) NOT NULL,
  synsetno1 DECIMAL(6) NOT NULL,
  wordno2 DECIMAL(6) NOT NULL,
  synsetno2 DECIMAL(6) NOT NULL,
  reltypeno DECIMAL(2) NOT NULL
);

CREATE TABLE semrel (
  synsetno1 DECIMAL(6) NOT NULL,
  synsetno2 DECIMAL(6) NOT NULL,
  reltypeno DECIMAL(2) NOT NULL
);



--
-- explanatory tables
--

CREATE TABLE reltype (
  reltypeno DECIMAL(2) NOT NULL,
  typeno CHAR(1) NOT NULL,
  description VARCHAR(50)
);

CREATE TABLE lexname (
  lexno DECIMAL(2) NOT NULL,
  lexname VARCHAR(30),
  description VARCHAR(80)
);



--
-- additional data including explanatory tables
--

CREATE TABLE sample (
  synsetno DECIMAL(6) NOT NULL,
  sampleno DECIMAL(2) NOT NULL,
  samp MEDIUMTEXT NOT NULL
);

CREATE TABLE adjmod (
  synsetno DECIMAL(6) NOT NULL,
  wordno DECIMAL(6) NOT NULL,
  modifier CHAR(2) NOT NULL
);

CREATE TABLE lexverbframe (
  synsetno DECIMAL(6) NOT NULL,
  wordno DECIMAL(6) NOT NULL,
  frameno DECIMAL(2) NOT NULL
);

CREATE TABLE semverbframe (
  synsetno DECIMAL(6) NOT NULL,
  frameno DECIMAL(2) NOT NULL
);

CREATE TABLE frame (
  frameno DECIMAL(2) NOT NULL,
  description VARCHAR(50)
);



--
-- (c) Copyright 2002 -- 2007 by Richard Bergmair
--
