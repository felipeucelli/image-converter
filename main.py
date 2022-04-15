# -*- coding: utf-8 -*-

# @autor: Felipe Ucelli
# @github: github.com/felipeucelli

# Built-in
import tkinter
from _thread import start_new_thread
from tkinter import ttk, messagebox, filedialog

from PIL import Image


class Gui:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Image Converter')
        self.root.geometry('750x395')
        self.root.resizable(False, False)

        self.status_convert = True
        self.file_path = []

        self.variable_out_file = tkinter.IntVar()

        self.format_files = {
            1: {
                'outfile': 'png',
                'chanel': 'RGBA'
            },
            2: {
                'outfile': 'jpeg',
                'chanel': 'RGB'
            }
        }

        self.style_root = ttk.Style(self.root)
        self.style_root.configure('TButton', font=('Arial', 15))
        self.style_root.configure('btn.TButton', font=('Arial', 10))
        self.style_root.configure('TRadiobutton', font=('Arial', 15))
        self.style_root.map('btn_stop_convert.TButton', foreground=[('!disabled', 'red'), ('disabled', 'grey')])
        self.style_root.map('btn_start_convert.TButton', foreground=[('!disabled', 'green'), ('disabled', 'grey')])

        self._interface()

    def _interface(self):
        """
        Configuring the interface widgets
        :return:
        """
        self.frame_main = tkinter.Frame(self.root, width=540, height=520)
        self.frame_main.pack(padx=5, pady=5, )

        self.frame_convert = tkinter.LabelFrame(self.frame_main, width=540, height=520)
        self.frame_convert.pack()

        # File selection frame
        self.frame_add = tkinter.Frame(self.frame_convert, width=540, height=100)
        self.frame_add.pack(fill='both', padx=5, pady=5)

        self.btn_add = ttk.Button(self.frame_add, text='ADD FILE', command=self.add_file)
        self.btn_add.pack(pady=15, padx=15, side='left')

        self.radio_bnt_mp3 = ttk.Radiobutton(self.frame_add, text='PNG', variable=self.variable_out_file, value=1)
        self.radio_bnt_mp3.pack(side='right', padx=15)

        self.radio_bnt_mp4 = ttk.Radiobutton(self.frame_add, text='JPEG', variable=self.variable_out_file, value=2)
        self.radio_bnt_mp4.pack(side='right', padx=15)

        self.label_out_file = tkinter.Label(self.frame_add, font='arial 12', text='OUTPUT: ')
        self.label_out_file.pack(side='right', padx=15)

        # Frame listbox
        self.frame_list_box = tkinter.Frame(self.frame_convert, width=540, height=200)
        self.frame_list_box.pack(fill='both', pady=5, padx=5)

        list_playlist_scrollbar_y = tkinter.Scrollbar(self.frame_list_box, orient='vertical')
        list_playlist_scrollbar_y.pack(side="right", fill="y")

        list_playlist_scrollbar_x = tkinter.Scrollbar(self.frame_list_box, orient='horizontal')
        list_playlist_scrollbar_x.pack(side="bottom", fill="x")

        self.list_box_files = tkinter.Listbox(self.frame_list_box, width=540, height=8, font='arial 15',
                                              yscrollcommand=list_playlist_scrollbar_y.set,
                                              xscrollcommand=list_playlist_scrollbar_x.set, activestyle='none')
        self.list_box_files.pack()
        list_playlist_scrollbar_y.config(command=self.list_box_files.yview)
        list_playlist_scrollbar_x.config(command=self.list_box_files.xview)

        # Conversion buttons and listbox frame
        self.frame_convert = tkinter.Frame(self.frame_convert, width=540, height=120)
        self.frame_convert.pack(fill='both', pady=5, padx=5)

        self.btn_clear = ttk.Button(self.frame_convert, text='CLEAR', command=self.clear_list_box)
        self.btn_clear.pack(anchor='nw', side='left', pady=20, padx=5)
        self.btn_clear.config(state=tkinter.DISABLED)

        self.btn_remove = ttk.Button(self.frame_convert, text='REMOVE', command=self.remove_item_list_box)
        self.btn_remove.pack(anchor='nw', side='left', pady=20, padx=5)
        self.btn_remove.config(state=tkinter.DISABLED)

        self.btn_start_convert = ttk.Button(self.frame_convert, text='CONVERT', command=self.convert_file,
                                            style='btn_start_convert.TButton')
        self.btn_start_convert.pack(anchor='ne', side='right', pady=20, padx=5)
        self.btn_start_convert.config(state=tkinter.DISABLED)

        self.btn_stop_convert = ttk.Button(self.frame_convert, text='STOP',
                                           style='btn_stop_convert.TButton')
        self.btn_stop_convert.pack(anchor='ne', side='right', pady=20, padx=5)
        self.btn_stop_convert.config(state=tkinter.DISABLED)

    def change_interface_status(self, status: str):
        """
        Change the status of interface buttons
        :return:
        """
        self.btn_add['state'] = status
        self.radio_bnt_mp4['state'] = status
        self.radio_bnt_mp3['state'] = status
        self.btn_start_convert['state'] = status
        self.btn_remove['state'] = status
        self.btn_clear['state'] = status
        self.btn_stop_convert['state'] = 'enable' if status == 'disable' else 'disable'

    def remove_item_list_box(self):
        """
        Removes selected items in the listbox
        :return:
        """
        pos = self.list_box_files.curselection()
        if pos != ():
            self.list_box_files.delete(pos)
            self.file_path.pop(pos[0])
        if self.list_box_files.size() == 0:
            self.btn_start_convert['state'] = 'disable'
            self.btn_remove['state'] = 'disable'
            self.btn_clear['state'] = 'disable'

    def clear_list_box(self):
        """
        Clear all items from the listbox
        :return:
        """
        self.list_box_files.delete(0, 'end')
        self.file_path.clear()
        self.btn_start_convert['state'] = 'disable'
        self.btn_remove['state'] = 'disable'
        self.btn_clear['state'] = 'disable'

    def cancel_convert(self):
        """
        Cancel the conversation
        :return:
        """
        stop_convert = messagebox.askokcancel('Cancel Convert', 'Do you really want to stop the conversation?')
        if stop_convert:
            self.btn_stop_convert['state'] = 'disable'
            self.btn_stop_convert['text'] = 'STOPPING'
            self.status_convert = False

    def start_conversion(self):
        """
        Configures the interface to start the conversion
        :return:
        """
        self.status_convert = True
        for pos, value in enumerate(self.file_path):
            self.list_box_files.itemconfig(pos, fg='black')
        self.change_interface_status('disable')

    def conversion_finished(self):
        """
        Reset the interface
        :return:
        """
        messagebox.showinfo('Info', 'Conversion Finished')
        self.change_interface_status('normal')

        self.btn_stop_convert['state'] = 'disable'
        self.btn_stop_convert['text'] = 'STOP'

    def add_file(self):
        """
        Opens a box to select files, and inserts the files into a listbox
        :return:
        """
        files = filedialog.askopenfilenames(filetypes=(('all files', '*.*'),))
        if files != '' and files != ():
            self.change_interface_status('normal')
            for file in files:
                self.file_path.append(file)
                self.list_box_files.insert('end', file)

    def _thread_convert_file(self, *args):
        """
        Conversion function
        :param args: None
        :return:
        """
        _none = args
        if self.variable_out_file.get() == 0:
            messagebox.showerror('Error', 'Please, Select a Output File')
        else:
            save_path = filedialog.askdirectory()
            if save_path != '' and save_path != ():
                self.start_conversion()

                out_file = self.format_files[self.variable_out_file.get()]['outfile']
                chanel = self.format_files[self.variable_out_file.get()]['chanel']

                for pos, file in enumerate(self.file_path):  # Cycle through the list of paths
                    self.list_box_files.itemconfig(pos, fg='gray')
                    try:
                        img = Image.open(file).convert(chanel)
                        img.save(file.replace(f'.{self.get_extension(file)}', f'.{out_file}'), out_file)
                        img.close()
                    except (KeyError, IOError):
                        self.list_box_files.itemconfig(pos, fg='red')
                    else:
                        self.list_box_files.itemconfig(pos, fg='green')

                    if not self.status_convert:
                        break

                self.conversion_finished()

    def convert_file(self):
        """
        Start a new thread for the conversion
        :return:
        """
        start_new_thread(self._thread_convert_file, (None, None))

    @staticmethod
    def get_extension(file_path: str) -> str:
        """
        Get the file extension
        :param file_path: file_path
        :return: file extension
        """
        return file_path.split('.')[-1]

    def start_gui(self):
        """
        Start tkinter mainloop
        :return:
        """
        self.root.mainloop()


if __name__ == '__main__':
    main = Gui()
    main.start_gui()
