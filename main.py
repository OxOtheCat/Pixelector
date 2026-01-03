from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
from tkinter import filedialog
import math

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


# note: VERY VEYER  YERYV YERYEYR VERY VERY IMPORTANT NOTE: !!!!!!!!: check cols and row for being less than 2
# note: VERY VEYER  YERYV YERYEYR VERY VERY IMPORTANT NOTE: !!!!!!!!: check cols and row for being less than 2
# note: VERY VEYER  YERYV YERYEYR VERY VERY IMPORTANT NOTE: !!!!!!!!: check cols and row for being less than 2

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

def set_loadpic():
    global set_imageBorders
    pil_image = Image.open(path)
    resized_image = ImageOps.contain(pil_image,(1050, 500), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(resized_image)
    set_imageBorders[0] = tk_image.width()
    set_imageBorders[1] = tk_image.height()
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
    
    for i in range(COLS+1):
        set_canvas.create_line(NW.x+(i*dis_top/COLS*cos_top),NW.y+(i*dis_top/COLS*sin_top),SW.x+(i*dis_bottom/COLS*cos_bottom),SW.y+(i*dis_bottom/COLS*sin_bottom), fill="red", width=1, tags=("line","column"))
   
    for i in range(ROWS+1):
        set_canvas.create_line(NW.x+(i*dis_left/ROWS*cos_left),NW.y+(i*dis_left/ROWS*sin_left),NE.x+(i*dis_right/ROWS*cos_right),NE.y+(i*dis_right/ROWS*sin_right), fill="blue", width=1, tags=("line","column"))
    
set_canvas = Canvas(set, width=1050, height=500, bg="#DAAAAA")
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

set_columnsFrame.grid(row=1,column=0)


set_rowsFrame = Frame(set)

set_rowscale = Scale(set_rowsFrame, from_=256, to=2, length=485, showvalue=0, command=set_setrow)
set_rowscale.pack(side="top")

set_rowentry = Entry(set_rowsFrame, font=("monocraft",8), width=4, validate="key", validatecommand=set_vcmd)
set_rowentry.pack(side="bottom")
set_rowentry.insert(0, "16")

set_rowlabel = Label(set_rowsFrame, text="rows:", font=("monocraft",8))
set_rowlabel.pack(side="bottom")

set_rowsFrame.grid(row=0,column=1)


set_buttonsFrame = Frame(set)

Button(set_buttonsFrame, text="next", font=("monocraft",8)).pack()
Button(set_buttonsFrame, text="previous", font=("monocraft",8)).pack()

set_buttonsFrame.grid(row=1,column=1)
set_updateGrid()

root.mainloop()
