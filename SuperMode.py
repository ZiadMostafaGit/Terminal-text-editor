import sys

def Action(k,cursor,buffer,window,args,stdscr):

         if k == 113:
            

            sys.exit(0)


         elif k==115:
                   with open(args.filename, "w") as f:
                     f.write("\n".join(buffer.lines))
         elif k==97:
            filename = "numbers.txt"
            with open(filename, "w") as file:
               file.write(f"{cursor.start_row}\n")
               file.write(f"{cursor.end_row}\n")
               file.write(f"{cursor.start_col}\n")
               file.write(f"{cursor.end_col}\n")  



                     


                     

