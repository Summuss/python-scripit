import sys
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory

from ui.setting import Setting
from ui.setting import FunctionSettingRecord
from tools.enum_generator import generate_java_enum


def start():
    window.title('tool')
    window.geometry('1000x800')
    render_radio_button()
    render_option_input()
    render_input_text()
    render_output_text()
    render_confirm_button()
    load_setting(setting.get_function_type())

    window.mainloop()


def render_option_input():
    option_frame = Frame(window)
    option_frame.pack(fill=X, pady=5)

    def select_path():
        path_ = askdirectory()
        if path_:
            path.set(path_)

    path = StringVar()

    Label(option_frame, text="目标路径:").grid(row=0, column=0)
    entry = Entry(option_frame, textvariable=path, width=50)
    entry.grid(row=0, column=1)
    Button(option_frame, text="路径选择", command=select_path).grid(row=0, column=2)

    vars['path'] = path
    component['path_entry'] = entry


def render_radio_button():
    radio_frame = Frame(window)
    radio_value = IntVar()
    pady = 5

    def command():
        load_setting(radio_value.get())

    radio1 = Radiobutton(radio_frame, text='enum generator', variable=radio_value, value=1, command=command)
    radio1.pack(side=LEFT)

    radio2 = Radiobutton(radio_frame, text='vo generator', variable=radio_value, value=2, command=command)
    radio2.pack(side=LEFT)

    component['radios'] = (radio1, radio2)

    radio_frame.pack(side=TOP, fill=X, pady=pady)
    vars['radio'] = radio_value

    radio_value.set(setting.get_function_type())


def render_input_text():
    input_text_frame = Frame(window)
    input_text_frame.pack(fill=X, padx=15, pady=5)

    label = Label(input_text_frame, text='input:', font=('Arial', 12), height=1)

    label.pack(side=LEFT)

    text_input = Text(input_text_frame, height=10, font=('Arial', 14))
    text_input.pack(fill=X)
    component['input_text'] = text_input


def render_output_text():
    output_text_frame = Frame(window)
    output_text_frame.pack(fill=X, padx=15, pady=5)

    label = Label(output_text_frame, text='output:', font=('Arial', 12), height=1)

    label.pack(side=LEFT)

    text_output = Text(output_text_frame, height=10, font=('Arial', 14))
    text_output.pack(fill=X)
    text_output.insert(INSERT, 'hello world')
    component['output_text'] = text_output
    # print(text_output.get('0.0', END))


def render_confirm_button():
    confirm_button_frame = Frame(window)
    confirm_button_frame.pack(side=BOTTOM, pady=20, fill=X)

    confirm_button = Button(confirm_button_frame, text='confirm', font=('Arial', 15), command=confirm_action)
    confirm_button.pack(side=RIGHT, padx=20)


def load_setting(function_type):
    record = setting.get_record(function_type)
    vars['path'].set(record.output_path)
    component['input_text'].delete('1.0', END)
    component['input_text'].insert(INSERT, record.input_content)

    component['output_text'].delete('1.0', END)
    component['output_text'].insert(INSERT, record.output_content)

    component['path_entry'].xview_scroll(len(record.output_path), UNITS)

    pass


def process(function_type, input_text, path):
    output = ''
    if function_type == 1:
        output = generate_java_enum(input_text, path)

    return output


def confirm_action():
    try:
        function_type = vars['radio'].get()
        output_path = vars['path'].get()
        input_content = component['input_text'].get('0.0', END)
        output_content = process(function_type, input_content, output_path)

        record = FunctionSettingRecord(function_type, output_path, input_content, output_content)
        setting.set_function_type(function_type)
        setting.set_setting_record(function_type, record)
        setting.save_config()

        load_setting(function_type)
    except:
        messagebox.showerror(title='结果', message='错误')
    else:
        messagebox.showinfo(title='结果', message='成功')


if __name__ == '__main__':
    window = Tk()
    setting = Setting()
    component = {}
    vars = {}
    start()
