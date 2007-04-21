#!/usr/bin/python
# -*- coding: latin-1 -*-



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



import pickle;
import string;
import sys;
import traceback;

import config;

#
# temporary mapping
#
offsets={'n':[], 'v':[], 'a':[], 'r':[]}
wordnos={'n':[], 'v':[], 'a':[], 'r':[]}

synoffs={'n':0, 'v':0, 'a':0, 'r':0}

#
# fields of a synset-record
#
offset=0;
lex_filenum=0;
ss_type=' ';
w_cnt=0;
word=[];
lex_id=[];
p_cnt=0;
pointer_symbol=[];
synset_offset=[];
cntlist={};
pos=[];
source=[];
target=[];
f_cnt=[];
f_num=[];
w_num=[];
gloss='';

words={};

def read_cntlist():
  global cntlist;
  cntlistrev=open(config.DICTDIR+"/cntlist.rev","r");
  dataline=cntlistrev.readline();
  while dataline!='':
    spl=string.split(dataline);
    sensekey=spl[0];
    sensenumber=spl[1];
    tagcnt=string.atoi(spl[2],10);
    dataline=cntlistrev.readline();
    cntlist[sensekey]=tagcnt;
  cntlistrev.close();

def sqlrecodestr(stri):
  stri=string.replace(stri,"'","<apo>");
  stri=string.replace(stri,",","<com>");
  stri=string.replace(stri,"_"," ");
  stri=string.replace(stri,"\n","");
  stri=string.replace(stri,"`","<apo1>");
  stri=string.replace(stri,"´","<apo2>");
  st='';
  for c in stri:
    if string.find(string.printable,c)!=-1:
      st=st+c;
  k=0;
  bla1='';
  while (k<len(st)) and (st[k]==' '):
    k=k+1;
  while k<len(st):
    bla1=bla1+st[k];
    k=k+1;
  k=len(bla1)-1;
  bla2='';
  while (k>=0) and (bla1[k]==' '):
    k=k-1;
  while k>=0:
    bla2=bla1[k]+bla2;
    k=k-1;
  return bla2;

def cnvtype(tp):
  typ=tp;
  if (typ=='s'):
    typ='a';
  return typ;

def remmod(stri):
  idx=string.find(stri,'(');
  if idx==-1:
    return stri;
  else:
    return stri[:string.find(stri,'(')];

def getmod(stri):
  idx1=string.find(stri,'(');
  if idx1==-1:
    return '';
  else:
    idx2=string.find(stri,')');
    if idx2==-1:
      return '';
    else:
      return stri[idx1+1:idx2];

def to0st(num):
  return string.replace("%2d" % (num),' ','0');

def to_keynot(sst):
  if sst=='n':
    return 1;
  if sst=='v':
    return 2;
  if sst=='a':
    return 3;
  if sst=='s':
    return 5;
  if sst=='r':
    return 4;

def read_line(dataline):
  global offset;
  global lex_filenum;
  global ss_type;
  global w_cnt;
  global word;
  global lex_id;
  global p_cnt;
  global pointer_symbol;
  global synset_offset;
  global pos;
  global source;
  global target;
  global gloss;
  global f_cnt;
  global f_num;
  global w_num;

  offset=0;
  lex_filenum=0;
  ss_type=' ';
  w_cnt=0;
  word=[];
  lex_id=[];
  p_cnt=0;
  pointer_symbol=[];
  synset_offset=[];
  pos=[];
  source=[];
  target=[];
  f_cnt=[];
  f_num=[];
  w_num=[];
  gloss='';

  # 
  #  split up glossary:
  # 
  #    gloss <- glossary
  #    data <- rest of the data
  #  
  splitline=string.split(dataline,'|');
  if not len(splitline)==2:
    return -1;

  data=splitline[0];
  gloss=splitline[1][1:];

  # 
  #  split up data
  #  
  splitdata=string.split(data);       

  # 
  #  synset_offset  Current byte offset in the file represented
  #                 as an 8 digit decimal integer.
  #  
  offset=string.atoi(splitdata[0],10);


  # 
  #  lex_filenum    Two  digit decimal integer corresponding to
  #                 the lexicographer file name containing  the
  #                 synset.   See lexnames(5WN) for the list of
  #                 filenames and their corresponding  numbers.
  #  
  lex_filenum=string.atoi(splitdata[1],10);

  # 
  #  ss_type        One  character  code  indicating the synset
  #                 type:
  # 
  #                 n    NOUN
  #                 v    VERB
  #                 a    ADJECTIVE
  #                 s    ADJECTIVE SATELLITE
  #                 r    ADVERB
  #  
  ss_type=splitdata[2];

  # 
  #  w_cnt          Two digit  hexadecimal  integer  indicating
  #                 the number of words in the synset.
  #  
  w_cnt=string.atoi(splitdata[3],16);

  # 
  #  word           ASCII  form  of  a  word  as entered in the
  #                 synset by the  lexicographer,  with  spaces
  #                 replaced by underscore characters (_).  The
  #                 text of the word is case sensitive, in con-
  #                 trast  to  its  form  in  the corresponding
  #                 index.pos file, that contains  only  lower-
  #                 case  forms.   In  data.adj, a word is fol-
  #                 lowed by a  syntactic  marker  if  one  was
  #                 specified  in  the  lexicographer  file.  A
  #                 syntactic marker is appended, in  parenthe-
  #                 ses,  onto  word  without  any  intervening
  #                 spaces.  See wninput(5WN) for a list of the
  #                 syntactic markers for adjectives.
  # 
  #  lex_id         One  digit  hexadecimal  integer that, when
  #                 appended onto lemma, uniquely identifies  a
  #                 sense  within a lexicographer file.  lex_id
  #                 numbers  usually  start  with  0,  and  are
  #                 incremented  as  additional  senses  of the
  #                 word are added to the same  file,  although
  #                 there is no requirement that the numbers be
  #                 consecutive or begin with 0.  Note  that  a
  #                 value of 0 is the default, and therefore is
  #                 not present in lexicographer files.
  # 
  #  If word[i] is the i-th word, then lex_id[i] is its lex_id.
  #  There are w_cnt elements in each array.
  #
  word=[];
  lex_id=[];
  startofs=4;
  ofs=range(startofs, startofs+(w_cnt*2), 2);
  for x in ofs:
    word.append(splitdata[x+0]);
  for x in ofs:
    lex_id.append(string.atoi(splitdata[x+1],16));

  # 
  #  p_cnt          Three digit decimal integer indicating  the
  #                 number  of  pointers  from  this  synset to
  #                 other synsets.  If p_cnt is 000 the  synset
  #                 has no pointers.
  #  
  p_cnt=string.atoi(splitdata[4+(w_cnt*2)],10);

  #
  #  ptr            A pointer from this synset to another.  ptr
  #                 is of the form:
  #
  #                 pointer_symbol  synset_offset  pos  source/target
  #
  #                 where synset_offset is the byte  offset  of
  #                 the  target  synset in the data file corre-
  #                 sponding to pos.
  #
  #                 The source/target field distinguishes lexi-
  #                 cal  and  semantic  pointers.  It is a four
  #                 byte hexadecimal field: the first two bytes
  #                 indicate  the  word  number  in the current
  #                 (source) synset, the last two  bytes  indi-
  #                 cate  the word number in the target synset.
  #                 A value of 0000 means  that  pointer_symbol
  #                 represents  a semantic relation between the
  #                 current  (source)  synset  and  the  target
  #                 synset indicated by synset_offset.
  #
  #                 A  lexical  relation  between  two words in
  #                 different synsets is  represented  by  non-
  #                 zero  values  in the source and target word
  #                 numbers.  The first and last two  bytes  of
  #                 this field indicate the word numbers in the
  #                 source and  target  synsets,  respectively,
  #                 between  which  the  relation  holds.  Word
  #                 numbers are assigned to the word fields  in
  #                 a  synset,  from  left  to right, beginning
  #                 with 1.
  #
  #                 See wninput(5WN) for a list of pointer_sym-
  #                 bols,  and  semantic  and  lexical  pointer
  #                 classifications.
  #
  pointer_symbol=[];
  synset_offset=[];
  pos=[];
  source=[]; 
  target=[]; 

  startofs=5+(w_cnt*2);
  ofs=range(startofs, startofs+(p_cnt*4), 4);
  for x in ofs:
    pointer_symbol.append(splitdata[x+0]);
  for x in ofs:
    synset_offset.append(string.atoi(splitdata[x+1],10));
  for x in ofs:
    pos.append(splitdata[x+2]);
  for x in ofs:
    source.append(string.atoi(splitdata[x+3][:2],16));
  for x in ofs:
    target.append(string.atoi(splitdata[x+3][2:],16));

  #
  #  frames         In data.verb only, a list of numbers corre-
  #                 sponding   to  the  generic  verb  sentence
  #                 frames for words in the synset.  frames  is
  #                 of the form:
  #
  #                 f_cnt  +  f_num  w_num  [+  f_num  w_num...]
  #
  #                 where  f_cnt  a  two  digit decimal integer
  #                 indicating the  number  of  generic  frames
  #                 listed,  f_num is a two digit decimal inte-
  #                 ger frame number, and w_num is a two  digit
  #                 hexadecimal  number  indicating the word in
  #                 the synset that the frame applies  to.   As
  #                 with  pointers, if this number is 00, f_num
  #                 applies to all words  in  the  synset.   If
  #                 non-zero, it is applicable only to the word
  #                 indicated.  Word numbers  are  assigned  as
  #                 described  for pointers.  Each f_num  w_num
  #                 pair is preceded by a +.  See  wninput(5WN)
  #                 for   the  text  of  the  generic  sentence
  #                 frames.
  #
  if ss_type=='v':
    startofs=5+(w_cnt*2)+(p_cnt*4)+1;
    f_cnt=string.atoi(splitdata[startofs-1],10);
    f_num=[];
    w_num=[];
    ofs=range(startofs,startofs+f_cnt*3,3);
    for x in ofs:
      f_num.append(string.atoi(splitdata[x+1],10));
    for x in ofs:
      w_num.append(string.atoi(splitdata[x+2],16));

  return 0;

#
# firstpass:
#
# the first pass initializes offsets[type]
# and wordnos[type], and its
# data structures.
# it also prints the INSERT Statements
# for inserting words and synsets, but
# not for any kind of relation between
# them.
#
def firstpass(filename):
  global offset;
  global lex_filenum;
  global ss_type;
  global w_cnt;
  global word;
  global lex_id;
  global p_cnt;
  global pointer_symbol;
  global synset_offset;
  global pos;
  global source;
  global target;
  global gloss;
  global f_cnt;
  global f_num;
  global w_num;
  global synoffs;
  global words;
  global offsets;

  f=open(filename);
  dataline=f.readline();

  #
  # PASS 1:
  #
  # initialization of words[] and offsets[]
  #
  # the synsetnumber of a synset is the
  # index, where its offset can be found
  # in offsets[]
  #
  # the wordnumber of a word is the
  # index, where its lemma can be found in
  # in words[]
  #

  # rewind the file
  f.seek(0,0);
  synsetno=0;
  # read first line
  dataline=f.readline();
  # for each line:
  while dataline!='':
    if read_line(dataline)==0:
      glosslist=string.split(gloss,';');
      if glosslist[0][0]=='"':
        definition='NULL';
        samples=glosslist;
      else:
        definition="'"+sqlrecodestr(glosslist[0])+"'";
        samples=glosslist[1:];
#      print "INSERT INTO synset VALUES (%d, %s, %d)" % \
#        (len(offsets[cnvtype(ss_type)])+synoffs[cnvtype(ss_type)],definition,lex_filenum);
      print "INSERT INTO synset VALUES (%d, %s, %d)" % \
        (synsetno+synoffs[cnvtype(ss_type)],definition,lex_filenum);
      k=0;
      for samp in samples:
        print "INSERT INTO sample VALUES (%d, %d, '%s')" % \
          (synsetno+synoffs[cnvtype(ss_type)],k,sqlrecodestr(string.replace(samp,'"','')));
        k=k+1;
      # for each word within the synset
      for curword in word:
        # if we don't already have the word in our wordlist
      	if not words.has_key(remmod(curword)):
          # print an insert-statement for the word
          print "INSERT INTO word VALUES (%d, '%s')" % \
            (len(words),sqlrecodestr(remmod(curword)));
          # and last but not least: append the word to our list.
      	  words[remmod(curword)]=len(words);
        # insert the modifiers, if we have any:
        if (cnvtype(ss_type)=='a') and (getmod(curword)!=''):
          print "INSERT INTO adjmod VALUES (%d, %d, '%s')" % \
            (synsetno+synoffs[cnvtype(ss_type)],words[remmod(curword)],getmod(curword));
      # append the offset to the offset-list
      offsets[cnvtype(ss_type)].append(offset);
      synsetno=synsetno+1;
    # read the next line
    dataline=f.readline();
    
  #
  # PASS 2:
  #
  # initialize the wordnos[][][]-structure:
  #
  # it is an associative array of
  # two-dimensional arrays of wordnos.
  # wordnos[type][synset][word] hold the wordnumber
  # of the "word"-th word within the "synset"-th synset
  # of type "type".
  #

  # rewind the file
  f.seek(0,0);
  # read the first line
  dataline=f.readline();

  tpe='';
  # for each synset:
  while dataline!='':
    if read_line(dataline)==0:
      # create a curwordnos-array, holding the wordnos
      # of the synset we are currently at.
      curwordnos=[];
      for curword in word:
	curwordnos.append(words[remmod(curword)]);
      # append the curwordnos-array to the wordnos-array
      # of the ss_type we are currently at:
      wordnos[cnvtype(ss_type)].append(curwordnos);
      # "remember" the type
      tpe=ss_type;
    # read the next line
    dataline=f.readline();

  return len(offsets[cnvtype(tpe)]);



#
# secondpass:
#
# prints SQL for handling relations
#
def secondpass(filename):
  global offset;
  global lex_filenum;
  global ss_type;
  global w_cnt;
  global word;
  global lex_id;
  global p_cnt;
  global pointer_symbol;
  global synset_offset;
  global pos;
  global source;
  global target;
  global gloss;
  global f_cnt;
  global f_num;
  global w_num;
  global synoffs;
  global words;
  global cntlist;

  f=open(filename);

  #
  # PASS 1
  # 
  # insert the senses, using the data from
  # the wordnos-structure, and the lex-ids
  # from the file.
  #
  # insert the verbframes.
  #

  # rewind the file
  f.seek(0,0);
  # read the first line
  dataline=f.readline();
  # count the synsetno we are currently at
  synsetno=0;
  while dataline!='':
    # for each synset
    if read_line(dataline)==0:
      # for each word
      k=0;
      try:
        while k<len(wordnos[cnvtype(ss_type)][synsetno]):
          try:
            sensekey="%s%%%d:%s:%s::" % (word[k],to_keynot(ss_type),to0st(lex_filenum),to0st(lex_id[k]));
            tagcnt=cntlist[sensekey];
          except:
            tagcnt=0;
          print "INSERT INTO sense VALUES (%d, %d, %d)" % \
            (wordnos[cnvtype(ss_type)][synsetno][k], \
             synsetno+synoffs[cnvtype(ss_type)], tagcnt);
          k=k+1;
      except:
        try:
          sys.stderr.write("--- ERROR at MEANING: synset %d, offset %d : ---\n" % (synsetno, offsets[cnvtype(ss_type)][synsetno]));
        except:
          sys.stderr.write("--- ERROR IN ERROR at MEANING\n");
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]);
        sys.stderr.write("offset=%d, k=%d" % (offset, k));
        sys.stderr.write("\n\n");

      # if it is a verb:
      if ss_type=='v':
        # for each frame:
        k=0;
        try:
          while k<f_cnt:
            # print an insert-statement for the frame
            wnumstr='';
            if w_num[k]==0:
              print "INSERT INTO semverbframe VALUES (%d, %d)" % \
                (synsetno+synoffs[cnvtype(ss_type)], \
                f_num[k]);
            else:
              print "INSERT INTO lexverbframe VALUES (%d, %d, %d)" % \
                (synsetno+synoffs[cnvtype(ss_type)], \
                wordnos[cnvtype(ss_type)][synsetno][w_num[k]-1], \
                f_num[k]);
            k=k+1;
        except:
          try:
            sys.stderr.write("--- ERROR at VERBFRAME synset %d, offset %d : ---\n" % (synsetno, offsets[cnvtype(ss_type)][synsetno]));
          except:
            sys.stderr.write("--- ERROR IN ERROR at VERBFRAME\n");
          traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]);
          sys.stderr.write("offset=%d, k=%d" % (offset, k));
          sys.stderr.write("\n\n");
        
      synsetno=synsetno+1;
    dataline=f.readline();
 
  #
  # PASS 2
  # 

  dohcount=0 ;
  pos_out = {'asdfa': 'foo'} ;

  # rewind the file
  f.seek(0,0);
  # read the first line
  dataline=f.readline();
  # count the synsetno we are at
  synsetno=0;
  while dataline!='':
    # for each synset
    if read_line(dataline)==0:
      # for each pointer
      k=0;
      try:
	while k<p_cnt:
          # convert the pointer-symbol to a ptrno
	  ptrno=0;

	  if pointer_symbol[k]=='+':
	    ptrno=28;
	  elif pointer_symbol[k]==';c':
	    ptrno=29;
	  elif pointer_symbol[k]=='-c':
	    ptrno=30;
	  elif pointer_symbol[k]==';r':
	    ptrno=31;
	  elif pointer_symbol[k]=='-r':
	    ptrno=32;
	  elif pointer_symbol[k]==';u':
	    ptrno=33;
	  elif pointer_symbol[k]=='-u':
	    ptrno=34;

	  # elif pos[k]=='n':
	  elif ss_type=='n':
	    if pointer_symbol[k]=='!':
	      ptrno=1;
	    elif pointer_symbol[k]=='@':
	      ptrno=2;
	    elif pointer_symbol[k]=='@i':
	      ptrno=3;
	    elif pointer_symbol[k]=='~':
	      ptrno=4;
	    elif pointer_symbol[k]=='~i':
	      ptrno=5;
	    elif pointer_symbol[k]=='#m':
	      ptrno=6;
	    elif pointer_symbol[k]=='#s':
	      ptrno=7;
	    elif pointer_symbol[k]=='#p':
	      ptrno=8;
	    elif pointer_symbol[k]=='%m':
	      ptrno=9;
	    elif pointer_symbol[k]=='%s':
	      ptrno=10;
	    elif pointer_symbol[k]=='%p':
	      ptrno=11;
	    elif pointer_symbol[k]=='=':
	      ptrno=12;

	  elif ss_type=='v':
	    if pointer_symbol[k]=='!':
	      ptrno=13;
	    elif pointer_symbol[k]=='@':
	      ptrno=14;
	    elif pointer_symbol[k]=='~':
	      ptrno=15;
	    elif pointer_symbol[k]=='*':
	      ptrno=16;
	    elif pointer_symbol[k]=='>':
	      ptrno=17;
	    elif pointer_symbol[k]=='^':
	      ptrno=18;
	    elif pointer_symbol[k]=='$':
	      ptrno=19;

	  elif ss_type=='a' or ss_type=='s':
	    if pointer_symbol[k]=='!':
	      ptrno=20;
	    elif pointer_symbol[k]=='&':
	      ptrno=21;
	    elif pointer_symbol[k]=='<':
	      ptrno=22;
	    elif pointer_symbol[k]=='\\':
	      ptrno=23;
	    elif pointer_symbol[k]=='=':
	      ptrno=24;
	    elif pointer_symbol[k]=='^':
	      ptrno=25;

	  elif ss_type=='r':
	    if pointer_symbol[k]=='!':
	      ptrno=26;
	    elif pointer_symbol[k]=='\\':
	      ptrno=27;

          if (ptrno==0):
	    if (pos_out.has_key(pos[k])!=True):
	      pos_out[pos[k]]={'asdfa': 'foo'} ;
	    if (pos_out[pos[k]].has_key(pointer_symbol[k]) != True):
	      pos_out[pos[k]][pointer_symbol[k]] = 1 ;
	      sys.stderr.write("FAILED! - filename == '" + filename + "' - pos[k] == '" + pos[k] + "' - pointer_symbol[k] == '" + pointer_symbol[k] + "' data:\n" + dataline + "\n\n") ;
	      dohcount += 1 ;

	  if ((source[k]==0) and (target[k]==0)):
	    print "INSERT INTO semrel VALUES (%d, %d, %d)" % \
	      (synsetno+synoffs[cnvtype(ss_type)], \
	       offsets[pos[k]].index(synset_offset[k])+synoffs[pos[k]], \
	       ptrno);
	  else:
	    print "INSERT INTO lexrel VALUES (%d, %d, %d, %d, %d)" % \
	      (wordnos[cnvtype(ss_type)][synsetno][source[k]-1],
	       synsetno+synoffs[cnvtype(ss_type)],
	       wordnos[pos[k]][offsets[pos[k]].index(synset_offset[k])][target[k]-1],
	       offsets[pos[k]].index(synset_offset[k])+synoffs[pos[k]],
	       ptrno);
          k=k+1;
        synsetno=synsetno+1;
      except:
        try:
          sys.stderr.write("--- ERROR bei der RELATION: synset %d, offset %d : ---\n" % (synsetno, offsets[cnvtype(ss_type)][synsetno]));
        except:
          sys.stderr.write("--- ERROR IN ERROR der RELATION\n");
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]);
        sys.stderr.write("offset=%d, k=%d" % (offset, k));
        sys.stderr.write("\n\n");

    dataline=f.readline();




#
# Do first passes over files
#
synoffs["n"]=0;
synoffs["v"]=firstpass(config.DICTDIR+"/data.noun");
synoffs["a"]=synoffs["v"]+firstpass(config.DICTDIR+"/data.verb");
synoffs["r"]=synoffs["a"]+firstpass(config.DICTDIR+"/data.adj");
firstpass(config.DICTDIR+"/data.adv");

#
# this is the code to save/load
# data created after the first pass.
# for debugging purposes uncomment
# the appropriate code, so you don't
# have to do the first passes again,
# if something goes wrong during the
# second passes.
#
#
# SAVE
#
f=open(config.TMPDIR+"/wordnos.pickle","w");
pickle.dump(wordnos,f);
f.close();

f=open(config.TMPDIR+"/offsets.pickle","w");
pickle.dump(offsets,f);
f.close();

f=open(config.TMPDIR+"/synoffs.pickle","w");
pickle.dump(synoffs,f);
f.close();
#
# LOAD
#
#f=open(config.TMPDIR+"/wordnos.pickle");
#wordnos=pickle.load(f);
#f.close();
#
#f=open(config.TMPDIR+"/offsets.pickle");
#offsets=pickle.load(f);
#f.close();
#
#f=open(config.TMPDIR+"/synoffs.pickle");
#synoffs=pickle.load(f);
#f.close();

read_cntlist();

#
# do second passes
#
secondpass(config.DICTDIR+"/data.noun");
secondpass(config.DICTDIR+"/data.verb");
secondpass(config.DICTDIR+"/data.adj");
secondpass(config.DICTDIR+"/data.adv");



#
# (c) Copyright 2002 -- 2007 by Richard Bergmair
#
