import argparse
import curses
import sys
import Buffer
import Window
import Cursor
import NormalMode












def Action(k,cursor,buffer,window,args):

         if k == 27:  
            sys.exit(0)


         elif k==115:
                   buffer.insert(cursor,1,window)
                   with open(args.filename, "w") as f:
                     f.write("\n".join(buffer.lines))
                     

