from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
from tkinter import filedialog
import math
import re

path = "none"
RES = [1200,650]



root=Tk()
root.title("Pixelector")
root.geometry(f"{RES[0]}x{RES[1]}")
root.resizable(False, False)
nb = ttk.Notebook(root)
select = ttk.Frame(nb)
nb.add(select, text='select')
set = ttk.Frame(nb)
nb.add(set, text='set dimensions', padding=15, state="disabled") # normal / disabled / hidden
edit = ttk.Frame(nb)
nb.add(edit, text='edit', state="disabled")
export = ttk.Frame(nb)
nb.add(export, text='export', state="disabled")
nb.pack(expand=1, fill="both")

#                               SELECT PICTURE                              #

def open_file_dialog():
    filepath = filedialog.askopenfilename(
        title="Select an image",
        initialdir="/",
        filetypes=(
            ('Images', ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif', '*.webp')),
            ('All files', '*.*')
        )
    )

    if filepath:
        global path
        path = filepath
        select_nextButton.config(state="normal")
        select_pathText.config(text="Selected File: " + filepath)

def select_next():
    nb.tab(set, state="normal")
    nb.select(set)
    nb.tab(select, state="disabled")
    set_loadpic()

Label(select, text="Please select an image to extract the pixel art from", font=("Monocraft", 16)).pack(pady=5)

Button(select, text="open file", command=open_file_dialog, font=("Monocraft", 30)).pack(pady=5)
select_pathText = Label(select, text=f"file: {path}", font=("Monocraft", 8))
select_pathText.pack(pady=5)


select_nextButton = Button(select, text="next", command=select_next, font=("Monocraft", 8), state="disabled")
select_nextButton.pack(pady=5)

#                               SET LIMITS                              #


# note: VERY VEYER  YERYV YERYEYR VERY VERY IMPORTANT NOTE: !!!!!!!!: check cols and row for being less than 1
# note: VERY VEYER  YERYV YERYEYR VERY VERY IMPORTANT NOTE: !!!!!!!!: check cols and row for being less than 1
# note: VERY VEYER  YERYV YERYEYR VERY VERY IMPORTANT NOTE: !!!!!!!!: check cols and row for being less than 1

def set_validateLength(new_value):
    if new_value == "": return True
    max_len = 256
    yay = True
    if not new_value.isdigit():
        yay = False
    elif int(new_value) > max_len:
        yay = False
    if not yay:
        root.bell()
        messagebox.showwarning("invalid value", "column/row number must be an integer and can't be more than 256")
    return yay
set_vcmd = (root.register(set_validateLength), '%P')

set_imageBorders = [2,2]
set_canvasRes = [800,500]
mipmap = [[0,0],[0,0]]

class set_point:
    def __init__(self, canvas, x, y, color, borders, type):
        radius = 4
        self.canvas = canvas
        self.borders = borders
        self.radius = radius
        self.id = canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, 
            fill=color, outline="black", width=1, tags=("point",str(type))
        )
        self.x = x
        self.y = y
        self._drag_data = {"x": 0, "y": 0, "item": None}

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self._drag_data["item"] = self.id
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag(self, eventt):
        set_updateGrid()
        event = eventt
        if eventt.x > self.borders[0]: event.x = self.borders[0]
        elif eventt.x < 0: event.x = 0
        if eventt.y > self.borders[1]: event.y = self.borders[1]
        elif eventt.y < 0: event.y = 0
        self.canvas.coords(self._drag_data["item"], event.x - self.radius, event.y - self.radius, event.x + self.radius, event.y + self.radius)
        self.x = event.x
        self.y = event.y
        #delta_x = event.x - self._drag_data["x"]
        #delta_y = event.y - self._drag_data["y"]
        #self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        #self._drag_data["x"] = event.x
        #self._drag_data["y"] = event.y

    def on_release(self, event):
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

pil_image = None
set_imagescale = 1
def TEST_savepixelart():
    height = len(mipmap)
    width = len(mipmap[0])
    print(height,width)
    img = Image.new('RGBA', (width, height))
    flat_pixel_data = [pixel for row in mipmap for pixel in row]
    img.putdata(flat_pixel_data)
    img.save('output_image.png', 'PNG')
def set_getpixels():
    global set_pointNW, set_pointNE, set_pointSW, set_pointSE, set_colentry, set_rowentry
    NW = set_pointNW
    NE = set_pointNE
    SW = set_pointSW
    SE = set_pointSE
    COLS = int(set_colentry.get())
    ROWS = int(set_rowentry.get())
    def get_cos(bir,iki):
        return math.cos(math.atan2(iki.y - bir.y , iki.x - bir.x))
    def get_sin(bir,iki):
        return math.sin(math.atan2(iki.y - bir.y , iki.x - bir.x))
    
    dis_top = math.dist((NW.x,NW.y),(NE.x,NE.y))
    cos_top = get_cos(NW, NE)
    sin_top = get_sin(NW, NE)
    
    dis_bottom = math.dist((SW.x,SW.y),(SE.x,SE.y))
    cos_bottom = get_cos(SW, SE)
    sin_bottom = get_sin(SW, SE)
    
    dis_left = math.dist((NW.x,NW.y),(SW.x,SW.y))
    cos_left = get_cos(NW, SW)
    sin_left = get_sin(NW, SW)
    
    dis_right = math.dist((NE.x,NE.y),(SE.x,SE.y))
    cos_right = get_cos(NE, SE)
    sin_right = get_sin(NE, SE)
    
    #cords = [NW.x+(1*dis_top/COLS*cos_top)+(dis_top/COLS/2),NW.y+(1*dis_top/COLS*sin_top)+(dis_top/COLS/2)]
    #pixel_color = pil_image.getpixel(((cords[0]/set_imagescale),(cords[1]/set_imagescale)))
    #set_canvas.create_oval(cords[0]-1,cords[1]-1, cords[0]+1, cords[1]+1)
    
    
    def get_coss(bir,iki):
        return math.cos(math.atan2(iki[1] - bir[1] , iki[0] - bir[0]))
    def get_sinn(bir,iki):
        return math.sin(math.atan2(iki[1] - bir[1] , iki[0] - bir[0]))
    
    global mipmap
    mipmap = [[(r, c) for c in range(COLS)] for r in range(ROWS)]
    
    #for i in range(COLS):
    #    set_canvas.create_line(NW.x+(i*dis_top/COLS*cos_top)+(dis_top/COLS*cos_top/2),NW.y+(i*dis_top/COLS*sin_top)+(dis_top/COLS*sin_top/2),SW.x+(i*dis_bottom/COLS*cos_bottom)+(dis_bottom/COLS*cos_bottom/2),SW.y+(i*dis_bottom/COLS*sin_bottom)+(dis_bottom/COLS*sin_bottom/2))
    #    for l in range(ROWS):
    #        set_canvas.create_line(NW.x+(l*dis_left/ROWS*cos_left)+(dis_left/ROWS*cos_left/2),NW.y+(l*dis_left/ROWS*sin_left)+(dis_left/ROWS*sin_left/2),NE.x+(l*dis_right/ROWS*cos_right)+(dis_right/ROWS*cos_right/2),NE.y+(l*dis_right/ROWS*sin_right)+(dis_right/ROWS*sin_right/2))
    for i in range(COLS):
        heighta = [[NW.x+(i*dis_top/COLS*cos_top)+(dis_top/COLS*cos_top/2),NW.y+(i*dis_top/COLS*sin_top)+(dis_top/COLS*sin_top/2)],[SW.x+(i*dis_bottom/COLS*cos_bottom)+(dis_bottom/COLS*cos_bottom/2),SW.y+(i*dis_bottom/COLS*sin_bottom)+(dis_bottom/COLS*sin_bottom/2)]]
        for l in range(ROWS):
            widtha = [[NW.x+(l*dis_left/ROWS*cos_left)+(dis_left/ROWS*cos_left/2),NW.y+(l*dis_left/ROWS*sin_left)+(dis_left/ROWS*sin_left/2)],[NE.x+(l*dis_right/ROWS*cos_right)+(dis_right/ROWS*cos_right/2),NE.y+(l*dis_right/ROWS*sin_right)+(dis_right/ROWS*sin_right/2)]]
            sexyarray = [
                NW.x+(l*dis_left/ROWS*cos_left)+(dis_left/ROWS*cos_left/2) + (i*math.dist(widtha[0],widtha[1])/COLS*get_coss(widtha[0],widtha[1]))+(math.dist(widtha[0],widtha[1])/COLS*get_coss(widtha[0],widtha[1])/2)
                ,
                NW.y+(l*dis_left/ROWS*sin_left)+(dis_left/ROWS*sin_left/2) + (i*math.dist(widtha[0],widtha[1])/COLS*get_sinn(widtha[0],widtha[1]))+(math.dist(widtha[0],widtha[1])/COLS*get_sinn(widtha[0],widtha[1])/2)
                ]
            #sexyarray = [
            #    (NW.x+)+((i*math.dist(widtha[0],widtha[1])/COLS*get_coss(widtha[0],widtha[1]))+(math.dist(widtha[0],widtha[1])/COLS*get_coss(widtha[0],widtha[1])/2))
            #    ,
            #    NW.y+((l*math.dist(heighta[0],heighta[1])/ROWS*get_sinn(heighta[0],heighta[1]))+(math.dist(heighta[0],heighta[1])/ROWS*get_sinn(heighta[0],heighta[1])/2))
            #    ]
            pixel_color = pil_image.getpixel(((sexyarray[0]/set_imagescale),(sexyarray[1]/set_imagescale)))
            mipmap[l][i] = pixel_color
            #set_canvas.create_oval(sexyarray[0]-1,sexyarray[1]-1,sexyarray[0]+1,sexyarray[1]+1)
    TEST_savepixelart()
def set_loadpic():
    global set_imagescale
    global set_imageBorders
    global pil_image
    pil_image = Image.open(path)
    resized_image = ImageOps.contain(pil_image,(set_canvasRes[0], set_canvasRes[1]), Image.Resampling.NEAREST)
    tk_image = ImageTk.PhotoImage(resized_image)
    set_imageBorders[0] = tk_image.width()
    set_imageBorders[1] = tk_image.height()
    set_imagescale = set_imageBorders[0]/pil_image.width
    set_canvas.create_image(0, 0, anchor=NW, image=tk_image, tags=("MAINPIC"))
    set_canvas.image = tk_image
    set_canvas.tag_lower("MAINPIC")
def set_setcol(value):
    set_colentry.delete(0, END)
    set_colentry.insert(0, value)
    set_updateGrid()
def set_setrow(value):
    set_rowentry.delete(0, END)
    set_rowentry.insert(0, value)
    set_updateGrid()
def set_updateGrid():
    global set_pointNW, set_pointNE, set_pointSW, set_pointSE, set_colentry, set_rowentry
    NW = set_pointNW
    NE = set_pointNE
    SW = set_pointSW
    SE = set_pointSE
    COLS = int(set_colentry.get())
    ROWS = int(set_rowentry.get())
    set_canvas.delete("line")
    
    #set_canvas.create_line(NW.x,NW.y,NE.x,NE.y, fill="black", width=4, tags=("line","square_line"))
    #set_canvas.create_line(NW.x,NW.y,NE.x,NE.y, fill="red", width=2, tags=("line","square_line"))
    
    #set_canvas.create_line(NE.x,NE.y,SE.x,SE.y, fill="black", width=4, tags=("line","square_line"))
    #set_canvas.create_line(NE.x,NE.y,SE.x,SE.y, fill="red", width=2, tags=("line","square_line"))
    
    #set_canvas.create_line(SW.x,SW.y,SE.x,SE.y, fill="black", width=4, tags=("line","square_line"))
    #set_canvas.create_line(SW.x,SW.y,SE.x,SE.y, fill="red", width=2, tags=("line","square_line"))
    
    #set_canvas.create_line(SW.x,SW.y,NW.x,NW.y, fill="black", width=4, tags=("line","square_line"))
    #set_canvas.create_line(SW.x,SW.y,NW.x,NW.y, fill="red", width=2, tags=("line","square_line"))
    
    def get_cos(bir,iki):
        return math.cos(math.atan2(iki.y - bir.y , iki.x - bir.x))
    def get_sin(bir,iki):
        return math.sin(math.atan2(iki.y - bir.y , iki.x - bir.x))
    
    dis_top = math.dist((NW.x,NW.y),(NE.x,NE.y))
    cos_top = get_cos(NW, NE)
    sin_top = get_sin(NW, NE)
    
    dis_bottom = math.dist((SW.x,SW.y),(SE.x,SE.y))
    cos_bottom = get_cos(SW, SE)
    sin_bottom = get_sin(SW, SE)
    
    dis_left = math.dist((NW.x,NW.y),(SW.x,SW.y))
    cos_left = get_cos(NW, SW)
    sin_left = get_sin(NW, SW)
    
    dis_right = math.dist((NE.x,NE.y),(SE.x,SE.y))
    cos_right = get_cos(NE, SE)
    sin_right = get_sin(NE, SE)
    
    cooloor = set_colcolorentry.get()
    color = cooloor
    if not set_isHexColor(cooloor):
        color = set_defaultcolcolor
    
    
    for i in range(COLS+1):
        set_canvas.create_line(NW.x+(i*dis_top/COLS*cos_top),NW.y+(i*dis_top/COLS*sin_top),SW.x+(i*dis_bottom/COLS*cos_bottom),SW.y+(i*dis_bottom/COLS*sin_bottom), fill=color, width=1, tags=("line","column"))
   
   
    cooloor = set_rowcolorentry.get()
    color = cooloor
    if not set_isHexColor(cooloor):
        color = set_defaultrowcolor
   
    for i in range(ROWS+1):
        set_canvas.create_line(NW.x+(i*dis_left/ROWS*cos_left),NW.y+(i*dis_left/ROWS*sin_left),NE.x+(i*dis_right/ROWS*cos_right),NE.y+(i*dis_right/ROWS*sin_right), fill=color, width=1, tags=("line","row"))
    set_canvas.tag_raise("point")
set_canvas = Canvas(set, width=set_canvasRes[0], height=set_canvasRes[1])
set_canvas.grid(row=0, column=0)

set_pointNW = set_point(set_canvas, 100, 100, "red", set_imageBorders, "NW")
set_pointNE = set_point(set_canvas, 200, 100, "red", set_imageBorders, "NE")
set_pointSW = set_point(set_canvas, 100, 200, "red", set_imageBorders, "SW")
set_pointSE = set_point(set_canvas, 200, 200, "red", set_imageBorders, "SE")


set_columnsFrame = Frame(set)

set_colscale = Scale(set_columnsFrame, from_=2, to=256, orient=HORIZONTAL, length=1080, showvalue=0, command=set_setcol)
set_colscale.pack(side="top")

set_collabel = Label(set_columnsFrame, text="columns:", font=("monocraft",8))
set_collabel.pack(side="left")

set_colentry = Entry(set_columnsFrame, font=("monocraft",8), width=4, validate="key", validatecommand=set_vcmd)
set_colentry.pack(side="left")
set_colentry.insert(0, "16")
set_colentry.bind("<KeyRelease>", lambda heh: set_updateGrid())

set_columnsFrame.grid(row=1,column=0, columnspan=2)


set_rowsFrame = Frame(set)

set_rowscale = Scale(set_rowsFrame, from_=256, to=2, length=485, showvalue=0, command=set_setrow)
set_rowscale.pack(side="top")

set_rowentry = Entry(set_rowsFrame, font=("monocraft",8), width=4, validate="key", validatecommand=set_vcmd)
set_rowentry.pack(side="bottom")
set_rowentry.insert(0, "16")
set_rowentry.bind("<KeyRelease>", lambda heh: set_updateGrid())

set_rowlabel = Label(set_rowsFrame, text="rows:", font=("monocraft",8))
set_rowlabel.pack(side="bottom")

set_rowsFrame.grid(row=0,column=2)


set_settingsFrame = Frame(set)

Label(set_settingsFrame, text="hex codes of common colors:\nred: #F00    green: #0F0\nblue: #00F    yellow: #FF0\nblack: #000    white: #FFF\n",font=("monocraft",8)).grid(row=0,column=0,columnspan=2)

def set_isHexColor(color):
    pattern = r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$'
    if re.match(pattern, color):
        return True
    else:
        return False

set_defaultrowcolor = "#0000FF"
set_rowcolorentry = Entry(set_settingsFrame, font=("monocraft",8), width=16)
Label(set_settingsFrame, text="row color hex code:", font=("monocraft",8)).grid(row=1,column=0)
set_rowcolorentry.grid(row=1,column=1)
def set_rowcolorentryupdate(event):
    cooloor = set_rowcolorentry.get()
    color = cooloor
    if not set_isHexColor(cooloor):
        color = set_defaultrowcolor
    set_canvas.itemconfigure("row", fill=color)
set_rowcolorentry.bind("<KeyRelease>", set_rowcolorentryupdate)

set_defaultcolcolor = "#FF0000"
set_colcolorentry = Entry(set_settingsFrame, font=("monocraft",8), width=16)
Label(set_settingsFrame, text="col color hex code:", font=("monocraft",8)).grid(row=2,column=0)
set_colcolorentry.grid(row=2,column=1)
def set_colcolorentryupdate(event):
    cooloor = set_colcolorentry.get()
    color = cooloor
    if not set_isHexColor(cooloor):
        color = set_defaultcolcolor
    set_canvas.itemconfigure("column", fill=color)
set_colcolorentry.bind("<KeyRelease>", set_colcolorentryupdate)

set_settingsFrame.grid(row=0, column=1)



set_buttonsFrame = Frame(set)

Button(set_buttonsFrame, text="next", font=("monocraft",8), command=set_getpixels).pack()
Button(set_buttonsFrame, text="previous", font=("monocraft",8)).pack()

set_buttonsFrame.grid(row=1,column=2)
set_updateGrid()

root.mainloop()
