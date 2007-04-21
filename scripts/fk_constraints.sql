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



ALTER TABLE synset ADD CONSTRAINT fk_syn_lex FOREIGN KEY(lexno) REFERENCES lexname;

ALTER TABLE sense ADD CONSTRAINT fk_sen_wor FOREIGN KEY(wordno) REFERENCES word;
ALTER TABLE sense ADD CONSTRAINT fk_sen_syn FOREIGN KEY(synsetno) REFERENCES synset;

ALTER TABLE lexrel ADD CONSTRAINT fk_lex_sen1 FOREIGN KEY(wordno1,synsetno1) REFERENCES sense;
ALTER TABLE lexrel ADD CONSTRAINT fk_lex_sen2 FOREIGN KEY(wordno2,synsetno2) REFERENCES sense;
ALTER TABLE lexrel ADD CONSTRAINT fk_lex_rel FOREIGN KEY(reltypeno) REFERENCES reltype;

ALTER TABLE semrel ADD CONSTRAINT fk_sem_syn1 FOREIGN KEY(synsetno1) REFERENCES synset;
ALTER TABLE semrel ADD CONSTRAINT fk_sem_syn2 FOREIGN KEY(synsetno2) REFERENCES synset;
ALTER TABLE semrel ADD CONSTRAINT fk_sem_rel FOREIGN KEY(reltypeno) REFERENCES reltype;



ALTER TABLE sample ADD CONSTRAINT fk_sam_syn FOREIGN KEY(synsetno) REFERENCES synset;
ALTER TABLE adjmod ADD CONSTRAINT fk_adj_wor FOREIGN KEY(wordno,synsetno) REFERENCES sense;

ALTER TABLE lexverbframe ADD CONSTRAINT fk_lex_fra FOREIGN KEY(frameno) REFERENCES frame;
ALTER TABLE lexverbframe ADD CONSTRAINT fk_lex_sen FOREIGN KEY(wordno,synsetno) REFERENCES sense;

ALTER TABLE semverbframe ADD CONSTRAINT fk_sem_fra FOREIGN KEY(frameno) REFERENCES frame;
ALTER TABLE semverbframe ADD CONSTRAINT fk_sem_syn FOREIGN KEY(synsetno) REFERENCES synset;



--
-- (c) Copyright 2002 -- 2007 by Richard Bergmair
--
