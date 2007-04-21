#
# wordnet2sql: software to convert data from WordNet(R)'s-Format to
#              an SQL-Script for a relational DBMS.
#              Copyright (C) 2002 -- 2007 Richard Bergmair
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



##############################################################################
# Environment-settings: feel free to modify these!
RM=rm -f
CAT=cat
SED=sed
GREP=grep
BZIP2=bzip2
PYTHON=python
ECHO=echo
SORT=sort

##############################################################################
# here is how to create the distributed files:
TOTABLE=$(GREP) -e "INSERT INTO $* VALUES " | \
        $(SED) "s/INSERT INTO $* VALUES //g" | \
        $(SORT) -u
TOMYSQL=$(SED) -f tomysql.sed | $(SORT) -u

##############################################################################
# these are all the files we have
TABS=data/word.tab data/adjmod.tab data/synset.tab data/sense.tab \
     data/lexverbframe.tab data/lexrel.tab data/semrel.tab \
     data/reltype.tab data/frame.tab data/lexname.tab data/sample.tab \
     data/semverbframe.tab

MYSQLS=data.mysql/word.mysql data.mysql/adjmod.mysql data.mysql/synset.mysql \
       data.mysql/sense.mysql data.mysql/lexverbframe.mysql \
       data.mysql/lexrel.mysql data.mysql/semrel.mysql \
       data.mysql/reltype.mysql data.mysql/frame.mysql \
       data.mysql/lexname.mysql data.mysql/sample.mysql \
       data.mysql/semverbframe.mysql

TABBZ2S=dist/word.bz2 dist/adjmod.bz2 dist/synset.bz2 dist/sense.bz2 \
        dist/lexverbframe.bz2 dist/lexrel.bz2 dist/semrel.bz2 \
        dist/reltype.bz2 dist/frame.bz2 dist/lexname.bz2 dist/sample.bz2 \
        dist/semverbframe.bz2

MYSQLBZ2S=dist.mysql/word.mysql.bz2 dist.mysql/adjmod.mysql.bz2 \
          dist.mysql/synset.mysql.bz2 dist.mysql/sense.mysql.bz2 \
          dist.mysql/lexverbframe.mysql.bz2 dist.mysql/lexrel.mysql.bz2 \
          dist.mysql/semrel.mysql.bz2 \
          dist.mysql/reltype.mysql.bz2 dist.mysql/frame.mysql.bz2 \
          dist.mysql/lexname.mysql.bz2 dist.mysql/sample.mysql.bz2 \
          dist.mysql/semverbframe.mysql.bz2

##############################################################################
# targets
all: rawdata tabs mysql tabs-dist mysql-dist
clean: rawdata-clean tabs-clean mysql-clean tabs-dist-clean mysql-dist-clean

tabs: $(TABS)
mysql: $(MYSQLS)
tabs-dist: $(TABBZ2S)
mysql-dist: $(MYSQLBZ2S)

sampleconfig:
	$(RM) config.py
	$(ECHO) "DICTDIR=\"/root/wn/dict\"" >> config.py
	$(ECHO) "TMPDIR=\"tmp\"" >> config.py

rawdata:
	$(PYTHON) translatewn.py > rawdata
rawdata-clean:
	$(RM) rawdata
	$(RM) tmp/*.pickle

dist.mysql/%.mysql.bz2: data.mysql/%.mysql
	$(BZIP2) -c $< > $@
mysql-dist-clean:
	$(RM) dist.mysql/*.mysql.bz2

dist/%.bz2: data/%.tab
	$(BZIP2) -c $< > $@
tabs-dist-clean:
	$(RM) dist/*.bz2

data.mysql/%.mysql: data/%.tab
	$(CAT) $< | $(TOMYSQL) > $@
mysql-clean:
	$(RM) data.mysql/*.mysql

data/%.tab: staticdata rawdata
	$(CAT) staticdata rawdata | $(TOTABLE) > $@
tabs-clean:
	$(RM) data/*.tab



#
# (c) Copyright 2002 -- 2007 by Richard Bermair
#
