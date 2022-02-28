import tkinter
import datetime


class Timer:
    def __init__(self):
        self.coundowning = False
        self.target_time = 0
        self.text_id = None
        self.isringing = False

    def set_time(self, seconds):
        if self.coundowning:
            return
        self.coundowning = True
        self.target_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

    def pause_time(self):
        pass

    def get_remaining_time(self):
        if self.coundowning:
            return self.target_time - datetime.datetime.now()

    def rise_alarm(self):
        self.coundowning = False
        self.isringing = True
        BtnSetter.change_button_command(lambda: self.stop_ring())
        self.ring()
        BtnSetter.set_text('Stop')

    def ring(self):
        if not self.isringing:
            return
        print('\a')
        get_root().attributes('-topmost', True)
        get_root().attributes('-topmost', False)
        get_root().after(1000, lambda: self.ring())

    def stop_ring(self):
        self.isringing = False
        BtnSetter.set_time()

    def update(self):
        # Update displayed remaining time.
        if self.coundowning:
            if self.get_remaining_time() <= datetime.timedelta(seconds=0):
                self.rise_alarm()
            else:
                if self.text_id:
                    delete_from_canvas(self.text_id)
                self.text_id = time_drawing(self.get_remaining_time())
        get_root().after(100, self.update)


class BtnSetter:
    """Class for interacting with Set button.
    """
    btn = None
    set_time_cmd = None

    def __init__(self, btn):
        raise RuntimeError('This is non-instantiable class.')

    @classmethod
    def set_time(cls):
        cls.change_button_command(cls.set_time_cmd)
        cls.set_text('Set')

    @classmethod
    def change_button_command(cls, cmd):
        cls.btn['command'] = cmd

    @classmethod
    def set_text(cls, text):
        cls.btn['text'] = text


timer = Timer()

root = tkinter.Tk()
root.geometry('400x300')

cvs = tkinter.Canvas(root, width=300, height=150)

e = tkinter.Entry(root)
cvs.create_window(100, 100, window=e)

btn = tkinter.Button(root, text='Set')
cvs.create_window(100, 130, window=btn)


def string_to_sec(string):
    total_sec = 0
    var = string.split(':')
    var.reverse()
    for i in range(len(var)):
        total_sec += int(var[i]) * 60**i
    return total_sec


BtnSetter.btn = btn
BtnSetter.set_time_cmd = lambda: timer.set_time(string_to_sec(e.get()))

BtnSetter.set_time()


# Interface
def time_drawing(seconds):
    return cvs.create_text(150, 50, text=str(seconds), fill='black',
                           font=('Helvetica 19 bold'),)


def delete_from_canvas(id):
    cvs.delete(id)


def get_root(root=root):
    return root


timer.update()
cvs.pack()
root.mainloop()
