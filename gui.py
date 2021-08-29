import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
import time

BACKGROUND_COLOR = '#42444B'
COLUMN_SPACING = 30
ROW_SPACING = 30
ITEM_ICON_COLUMN_MIN_SIZE = 110
ITEM_NAME_COLUMN_MIN_SIZE = 250
COLUMN_MIN_SIZE = 250


def create_column_label(item_frame, fossil_value, counter, column_num, column_size):
    label = tkinter.Label(item_frame, text=fossil_value, bg=BACKGROUND_COLOR, font=('Arial Rounded MT Bold', 14), fg='#EFEEEE')
    label.grid(row=counter, column=column_num, padx=COLUMN_SPACING, pady=ROW_SPACING, sticky='w')
    item_frame.grid_columnconfigure(index=column_num, minsize=column_size)


def on_mousewheel(event):
    scroll = -1 if event.delta > 0 else 1
    main_canvas.yview_scroll(scroll, "units")


def updateGUI(fossilAvgPriceList):

        if second_frame.winfo_children():
            for widget in second_frame.winfo_children():
                widget.destroy()

        counter = 0

        for fossil in fossilAvgPriceList:
            column_num = 0

            item_frame = tkinter.Frame(second_frame)
            item_frame.configure(bg=BACKGROUND_COLOR)
            item_frame.pack()

            icon = ImageTk.PhotoImage(Image.open(fossil.id + '.png'))
            icon_label = tkinter.Label(item_frame, image=icon, bg=BACKGROUND_COLOR)
            icon_label.photo = icon
            icon_label.grid(row=counter, column=column_num, padx=COLUMN_SPACING, pady=ROW_SPACING, sticky='w')
            item_frame.grid_columnconfigure(index=column_num, minsize=ITEM_ICON_COLUMN_MIN_SIZE)
            column_num += 1

            create_column_label(item_frame, fossil.name, counter, column_num, ITEM_NAME_COLUMN_MIN_SIZE)
            column_num += 1

            create_column_label(item_frame, round(fossil.avgPrice, 1), counter, column_num, COLUMN_MIN_SIZE)
            column_num += 1

            create_column_label(item_frame, round(fossil.bulkQuant, 1), counter, column_num, COLUMN_MIN_SIZE)
            column_num += 1

            create_column_label(item_frame, round(fossil.profit, 1), counter, column_num, COLUMN_MIN_SIZE)
            column_num += 1

            create_column_label(item_frame, round(fossil.profitPerFossil, 1), counter, column_num, COLUMN_MIN_SIZE)
            column_num += 1

            create_column_label(item_frame, fossil.supply, counter, column_num, 2000)
            column_num += 1

            tkinter.ttk.Separator(item_frame, orient='horizontal').grid(row=counter + 1, column=0,
                                                                        columnspan=20, sticky='we')

            counter += 1


root = tkinter.Tk()
root.title('POE Bulk Flipper')
ico = Image.open('Bulk Flip Logo.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

main_frame = tkinter.Frame(root)
main_frame.pack(fill='both', expand=1, side='bottom')


main_canvas = tkinter.Canvas(main_frame)
main_canvas.pack(side='left', fill='both', expand=1)
main_canvas.configure(bg='#42444B')
main_canvas.bind_all("<MouseWheel>", on_mousewheel)


scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=main_canvas.yview)
scrollbar.pack(side='right', fill='y')

main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox('all')))

second_frame = tkinter.Frame(main_canvas)
second_frame.configure(bg='#42444B')
main_canvas.create_window((0, 0), window=second_frame, anchor='nw')

category_frame = tkinter.Frame(root)
category_frame.pack(side='top', fill='x')
category_frame.configure(bg='#42444B')


category_titles = ['Item', 'Avg Price', 'Bulk Quant', 'Profit', 'Profit Per', 'Supply']
total_categories = len(category_titles)
for index in range(total_categories):
    if index == 0:
        col_size = ITEM_NAME_COLUMN_MIN_SIZE + ITEM_ICON_COLUMN_MIN_SIZE
    else:
        col_size = COLUMN_MIN_SIZE
    item_label = tkinter.Label(category_frame, text=category_titles[index], bg='#42444B', font=('Arial Rounded MT Bold', 20, 'bold'), fg='#EFEEEE')
    item_label.grid(row=0, column=index, padx=COLUMN_SPACING, pady=ROW_SPACING, sticky='w')
    category_frame.grid_columnconfigure(index=index, minsize=col_size)

tkinter.ttk.Separator(category_frame, orient='horizontal').grid(row=1, column=0, columnspan=total_categories, sticky='we')
