import sys

def Action(k,cursor,buffer,window,args,stdscr):

         if k == 113:  
            sys.exit(0)


         elif k==115:
                   with open(args.filename, "w") as f:
                     f.write("\n".join(buffer.lines))




                     


                     

