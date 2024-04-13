




def up(buffer,cursor,window):
    cursor.up(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor)
    
    

def down(buffer,cursor,window):
    cursor.down(buffer)
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
    
        
    
    
         