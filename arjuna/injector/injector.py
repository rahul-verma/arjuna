from tkinter import *
from io import StringIO
from contextlib import redirect_stdout
from tkinter import filedialog
from tkcode import CodeEditor
import os
from idlelib.tooltip import Hovertip


root = Tk()

class Injector:


    def __init__(self, context):

        self.__staged_code_editor_list = []
        self.__single_code_editor_plus_button_frames_list = []

        root.geometry("1000x600")
        root.title(" Python Code Interpreter: ")

        self.__code_label = Label(root, text = "Code: ")   
  

        self.__canvas = Canvas(root, borderwidth=0, width=950)

        self.__main_code_editor_frame = Frame(self.__canvas)

        self.__vertical_scrollbar_main_code_editor_frame = Scrollbar(
                                root,
                                orient='vertical',
                                command= self.__canvas.yview)


        self.__canvas['yscrollcommand'] = self.__vertical_scrollbar_main_code_editor_frame.set

        self.__canvas.create_window((0,0), window=self.__main_code_editor_frame, anchor="nw", tags="self.__main_code_editor_frame")
        self.__main_code_editor_frame.bind("<Configure>", self.onFrameConfigure)

        self.__play_frame = Frame(root)

        self.__create_code_editor_button = Button(self.__play_frame, height = 2,
                        width = 5,
                        text ="+",
                        command = lambda:self.create_code_editor(context)) 

        self.__play_all_button = Button(self.__play_frame, height = 1,
                        width = 10,
                        text ="Play All",
                        font='Geneva 10',
                        command = lambda:self.play_all_code(context))

        play_all_tip = Hovertip(self.__play_all_button,'Play All Code Snippets In The Order Shown.')


        self.__export_staged_code_button = Button(self.__play_frame, height = 1,
                        width = 12,
                        text ="Save As",
                        font='Geneva 10',
                        command = lambda:self.export_staged_code())

        self.__output_frame = Frame(root)
        self.__output_label = Label(self.__output_frame, text = "Output: ", anchor='w', font='Consolas 12 bold')

        self.__clear_output_button = Button(self.__output_frame, height = 1,
                        width = 10,
                        text ="Clear Output",
                        font='Geneva 10',
                        command = lambda:self.clear_output())

        self.__output_text = Text(root, height = 10, wrap=NONE,
                    width = 130,
                    bg = "light cyan", font= ('Consolas 10'))

        self.__vertical_scrollbar_output = Scrollbar(
                                root,
                                orient='vertical',
                                command=self.__output_text.yview)

        self.__horizontal_scrollbar_output = Scrollbar(
                                root,
                                orient='horizontal',
                                command=self.__output_text.xview)
        
        self.__output_text['yscrollcommand'] = self.__vertical_scrollbar_output.set
        self.__output_text['xscrollcommand'] = self.__horizontal_scrollbar_output.set

        #  create default code editor
        self.create_code_editor(context)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.__canvas.configure(scrollregion=self.__main_code_editor_frame.bbox("all"))

    def play_staged_code(self, context, code_editor):
        code = code_editor.get("1.0", "end-1c")
        print(code)
        self._play_code(context, code=code, clear_output=True)
 
    def _play_code(self, context, code = None, clear_output=True):
        if clear_output:
            self.clear_output()
        f = StringIO()
        out = None
        er = None
        try:
            with redirect_stdout(f):
                exec(code, context)
            out = f.getvalue()
            self.__output_text.insert(INSERT, out)
        except Exception as e:
            out = f.getvalue()
            self.__output_text.insert(INSERT, out)
            try:
                start_index = float(len(out.splitlines()) + 1)
                end_index = self.__output_text.index('end')
                self.__output_text.insert(INSERT, str(end_index))
                self.__output_text.tag_configure('Error', foreground='red')
                self.__output_text.tag_add('Error', start_index, end_index)
            except Exception as g:
                self.__output_text.insert(INSERT, str(g))
            er = str(e)
            self.__output_text.insert(INSERT, er + os.linesep)

    def play_all_code(self, context):
        print(self.__staged_code_editor_list)
        self.clear_output()
        for code_editor in self.__staged_code_editor_list:
            saved_code =  code_editor.get("1.0", "end-1c")
            print(saved_code)
            self._play_code(context, saved_code, clear_output=False)
        

    def create_code_editor(self, context):

        # create a frame that contains code editor, minimize/maximize/play/delete buttons

        _single_code_editor_plus_buttons_frame = Frame(self.__main_code_editor_frame)

        _stage_code_editor = CodeEditor(_single_code_editor_plus_buttons_frame, 
                        height = 16, 
                        wrap=NONE, 
                        width = 130,
                        bg = "black", 
                        font= ('Consolas 10'),
                        language="python",
                        highlighter='dracula',
                        autofocus=True, 
                        blockcursor = True, 
                        insertofftime=0,
                        ) 
        _stage_code_editor.config(state=NORMAL)

        self.__single_code_editor_plus_button_frames_list.append(_single_code_editor_plus_buttons_frame)

        self.__staged_code_editor_list.append(_stage_code_editor)

        # create a sub frame that contains play/delete buttons

        _button_frame = Frame(_single_code_editor_plus_buttons_frame)

        # create associated play button
        _play_code_editor_button = Button(_button_frame, height = 0,
                        width = 2,
                        text ="p",
                        command = lambda:self.play_staged_code(context, _stage_code_editor))

        # create associated delete button
        _delete_code_editor_button = Button(_button_frame, height = 0,
                        width = 2,
                        text ="X",
                        command = lambda:self.delete_code_editor(_single_code_editor_plus_buttons_frame, _stage_code_editor))

        # create associated minimize/maximize button
        _min_max_code_editor_button = Button(_button_frame, height = 0,
                        width = 2,
                        text ="-",
                        command = lambda:self.minimize_maximize_code_editor(_single_code_editor_plus_buttons_frame, _stage_code_editor, _min_max_code_editor_button))

        _single_code_editor_plus_buttons_frame.grid(column=0, row=len(self.__staged_code_editor_list), sticky=N)
        _stage_code_editor.grid(column=0, row=0)
        _button_frame.grid(column=1, row=0, sticky=N)
        _min_max_code_editor_button.grid(column=0, row=0, sticky=N)
        _delete_code_editor_button.grid(column=0, row=1, sticky=N)
        _play_code_editor_button.grid(column=0, row=2, sticky=N)
   

    def delete_code_editor(self, single_code_editor_plus_buttons_frame, stage_code_editor):
        single_code_editor_plus_buttons_frame.destroy()
        self.__staged_code_editor_list.remove(stage_code_editor)
        self.__single_code_editor_plus_button_frames_list.remove(single_code_editor_plus_buttons_frame)

        index = 0
        for code_editor_button_frame in self.__single_code_editor_plus_button_frames_list:
            code_editor_button_frame.grid(column=0, row=index)
            index += 1

        self.onFrameConfigure(event=None)

    def minimize_maximize_code_editor(self, single_code_editor_plus_buttons_frame, stage_code_editor, _min_max_code_editor_button):
        if _min_max_code_editor_button['text'] == "-":
            stage_code_editor['height'] = 2
            _min_max_code_editor_button['text'] = "[]"
        else:
            stage_code_editor['height'] = 17
            _min_max_code_editor_button['text'] = "-"



    def export_staged_code(self):
        self.save_file()


    def clear_output(self):
        self.__output_text.delete('1.0', END)

    def save_file(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".py", filetypes = [("Python file", "*.py")])
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return

        text_to_save = ""

        for code_editor in self.__staged_code_editor_list:
            text_to_save +=  str(code_editor.get("1.0", "end-1c")) + os.linesep
    
        f.write(text_to_save)
        f.close()

    


    def launch(self):
        self.__code_label.grid(column=0, row=0)
        self.__canvas.grid(column=0, row=1, padx=(10, 10))
        self.__vertical_scrollbar_main_code_editor_frame.grid(column=1, row=1, sticky=N+S+E+W)
        self.__play_frame.grid(column=0, row=2)
        self.__create_code_editor_button.grid(column=0, row=0, padx=(10, 10))
        self.__play_all_button.grid(column=1, row=0, padx=(20, 0))
        self.__export_staged_code_button.grid(column=2, row=0, padx=(10, 0))
        self.__output_frame.grid(column=0, row=3)
        self.__output_label.grid(column=0, row=0)
        self.__clear_output_button.grid(column=1, row=0, padx=(10, 10), sticky=E)
        self.__output_text.grid(column=0, row=4, columnspan=3, padx=(10, 0))
        self.__horizontal_scrollbar_output.grid(column=0, row=5, sticky=N+S+E+W, columnspan=3)
        self.__vertical_scrollbar_output.grid(column=3, row=4, sticky=N+S+E+W)

        self.__menubar=Menu(root)
        self.__filemenu=Menu(self.__menubar,tearoff=0)
        self.__filemenu.add_command(label="Save As", command=self.save_file)
        self.__menubar.add_cascade(label="File", menu=self.__filemenu)
        root.config(menu=self.__menubar)

        
        
        mainloop()

        try:
            root.destroy()
        except TclError:
            # When the destroy isn't necessary, it's actually illegal. And we
            # don't know from inside the app whether it's necessary or not.
            pass        

injector = Injector(vars())
injector.launch()