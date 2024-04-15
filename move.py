




def up(buffer,cursor,window,line_numer):
    cursor.up(buffer,line_numer)
    window.up(cursor)
    window.horizontal_scroll(cursor)
    
    

def down(buffer,cursor,window,line_numer):
    cursor.down(buffer,line_numer)
    window.down(buffer,cursor)
    window.horizontal_scroll(cursor)
    
    
def left(buffer,cursor,window):
    cursor.left(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor)
    
    
def right(buffer,cursor,window):
    cursor.right(buffer,window)
    window.down(cursor,window)
    window.horizontal_scroll(cursor)
    
        
    
    
         