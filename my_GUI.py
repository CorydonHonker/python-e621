from tkinter import *
from custom_e621_mgr import DownloadMGR

custom_mgr = DownloadMGR()
root = Tk()
search_page = Frame(root)
download_page = Frame(root)
advanced_tag_page = Frame(root)


def show_downloads():
    search_page.forget()
    advanced_tag_page.forget()
    download_page.pack(fill=BOTH, expand=True)


def show_search():
    download_page.forget()
    advanced_tag_page.forget()
    search_page.pack(fill=BOTH, expand=True)


def show_advanced_tags():
    download_page.forget()
    search_page.forget()
    advanced_tag_page.pack(fill=BOTH, expand=True)


def page_1():
    def begin():
        if left_entry.get() == "":
            print('empty search')
        else:
            print(f'Search: "{left_entry.get()}"; Pools: {pool_bool.get()}')
            custom_mgr.post_search(left_entry.get())

    def end():
        custom_mgr.stop()

    middle_frame = Frame(search_page, bd=5, bg="purple")
    middle_frame.pack()
    info_data = '[INFO]\n' \
                'Input e621 search in the search box;\n\n' \
                'Toggle for downloading pool data (off is faster);\n\n' \
                'Toggle for sorting family data (negligible for time);'
    label = Label(middle_frame, text=info_data)
    label.pack()

    left_frame = Frame(search_page, bg="blue")
    left_frame.pack(side=LEFT)
    label = Label(left_frame, text="Search")
    label.pack()
    left_entry = Entry(left_frame)
    left_entry.insert(0, "set:cm_favlist_3 date:16_weeks_ago")
    left_entry.pack()
    button = Button(left_frame, text="Begin Search", command=begin)
    button.pack(padx=5, pady=5)
    button = Button(left_frame, text="Stop Search", command=end)
    button.pack(padx=5, pady=5)
    pool_bool = BooleanVar()
    pool_toggle = Checkbutton(left_frame, text="Get pool data;", variable=pool_bool)
    pool_toggle.pack()

    right_frame = Frame(search_page, bg="red")
    right_frame.pack(side=RIGHT)
    label = Label(right_frame, text="Navigation")
    label.pack()
    up_button = Button(right_frame, text="Up", command=show_advanced_tags)
    up_button.pack(padx=3, pady=3)
    info_button = Label(right_frame, text="Adv Tags\n----\nDownloads")
    info_button.pack(padx=3, pady=3)
    down_button = Button(right_frame, text="Down", command=show_downloads)
    down_button.pack(padx=3, pady=3)
    search_page.pack()


def page_2():
    def retrieve():
        print(f'Download Families: {family_bool.get()}; Download pools: {pool_bool.get()}')

    middle_frame = Frame(download_page, bd=5, bg="purple")
    middle_frame.pack()
    info_data = '[INFO]\n' \
                'Download'
    label = Label(middle_frame, text=info_data)
    label.pack()

    left_frame = Frame(download_page, bg="blue")
    left_frame.pack(side=LEFT)
    label = Label(left_frame, text="Download options")
    label.pack()
    button = Button(left_frame, text="Begin Download", command=retrieve)
    button.pack(padx=5, pady=5)
    pool_bool = BooleanVar()
    pool_toggle = Checkbutton(left_frame, text="Get pool data;", variable=pool_bool)
    pool_toggle.pack()
    family_bool = BooleanVar()
    pool_toggle = Checkbutton(left_frame, text="Get family data;", variable=family_bool)
    pool_toggle.pack()

    right_frame = Frame(download_page, bg="red")
    right_frame.pack(side=RIGHT)
    label = Label(right_frame, text="Navigation")
    label.pack()
    up_button = Button(right_frame, text="Up", command=show_search)
    up_button.pack(padx=3, pady=3)
    info_button = Label(right_frame, text="Search\n----\nDav Tags")
    info_button.pack(padx=3, pady=3)
    down_button = Button(right_frame, text="Down", command=show_advanced_tags)
    down_button.pack(padx=3, pady=3)
    download_page.pack()


def page_3():
    def retrieve():
        pass
        # print(f'Download Families: {family_bool.get()}; Download pools: {pool_bool.get()}')

    middle_frame = Frame(advanced_tag_page, bd=5, bg="purple")
    middle_frame.pack()
    info_data = '[INFO]\n' \
                'Adv Tags'
    label = Label(middle_frame, text=info_data)
    label.pack()

    left_frame = Frame(advanced_tag_page, bg="blue")
    left_frame.pack(side=LEFT)
    label = Label(left_frame, text="Tag options")
    label.pack()
    left_entry = Entry(left_frame)
    left_entry.pack()
    button = Button(left_frame, text="Submit list", command=retrieve)
    button.pack(padx=5, pady=5)

    right_frame = Frame(advanced_tag_page, bg="red")
    right_frame.pack(side=RIGHT)
    label = Label(right_frame, text="Navigation")
    label.pack()
    up_button = Button(right_frame, text="Up", command=show_downloads)
    up_button.pack(padx=3, pady=3)
    info_button = Label(right_frame, text="Downloads\n----\nSearch")
    info_button.pack(padx=3, pady=3)
    down_button = Button(right_frame, text="Down", command=show_search)
    down_button.pack(padx=3, pady=3)
    advanced_tag_page.pack()


def start_gui():
    root.geometry("400x300")
    page_1()  # search page
    page_2()  # download page
    page_3()  # advanced tag page
    show_search()
    root.title("Test")
    root.mainloop()
