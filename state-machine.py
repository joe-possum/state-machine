#! /bin/env python3

import sys
import getopt

args = getopt.getopt(sys.argv[1:],"n:f:p:")
states = args[1]
prefix = None
name = None
filestem = None
for switch in args[0] :
    if '-n' == switch[0] :
        name = switch[1]
    elif '-f' == switch[0] :
        filestem = switch[1]
    elif '-p' == switch[0] :
        prefix = switch[1]

if None == name or None == filestem :
    raise RuntimeError('Usage state-machine -n <namespace> -f <filestem> [ -p <prefix> ] <state> [ <state> [ ... ]]')
if None == prefix :
    prefix = name.upper() + '_'

comment = '/*\n * Machine generated code\n *\n * '
for arg in sys.argv :
    comment += ' %s'%(arg)
comment += '\n *\n */\n\n'

define = 'H_%s'%(name.upper())
header = comment
source = comment
header += '#ifndef %s\n#define %s\n\n'%(define,define)
source += '#include <stdio.h>\n'
source += '#include <string.h>\n'
source += '#include "%s.h"\n\n'%(filestem)
header += "typedef enum {"
source += "static const char *" + name + '_states_str[%d] = {'%(len(states))
sep = '\n  '
for state in states :
    header += sep + prefix + state
    source += sep + '"' + state + '"'
    sep = ',\n  '
header += '\n} %s_states;\n\n'%(name)
header += 'struct %s_state {\n  const char *name;\n  %s_states current;\n};\n\n'%(name,name)
header += 'void %s_state_init(struct %s_state *pvar, const char *name);\n'%(name,name)
header += 'void %s_state_set(struct %s_state *,%s_states);\n\n'%(name,name,name)
header += '#define %s_SET(P,X) %s_state_set(P,%s ## X)\n'%(name,name,prefix)
header += '#define %s_IS(X,V) (%s ## X == V.current)\n'%(name,prefix)
header += '#endif\n'
source += '\n};\n\n'
source += 'void %s_state_init(struct %s_state *pvar, const char *name) {\n'%(name,name)
source += '  fprintf(stderr,"%s_state_init(%%s) -> %%s\\n",name,%s_states_str[0]);\n'%(name,name)
source += '  pvar->name = strdup(name);\n'
source += '  pvar->current = 0;\n}\n\n'
source += 'void %s_state_set(struct %s_state *pvar, %s_states state) {\n'%(name,name,name)
source += '  fprintf(stderr,"%s_state_set(%%s) %%s -> %%s\\n",pvar->name,%s_states_str[pvar->current],%s_states_str[state]);\n'%(name,name,name)
source += '  pvar->current = state;\n}\n\n'

fh = open('%s.h'%(filestem),'w')
fh.write(header)
fh.close()

fh = open('%s.c'%(filestem),'w')
fh.write(source)
fh.close()
