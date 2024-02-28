import tkinter as tk
from tkinter import PhotoImage, messagebox,ttk
from tkinter import *
import sqlite3
import json
from datetime import datetime
import re

# to save parking slot list

# Function to save parking slot to a JSON file
def save_space_availability_data(matrix):
    with open("availability.json", "w") as json_file:
        json.dump(matrix, json_file)

# Function to load avaliability list from a file
def load_space_availability_data():
    try:
        with open("availability.json", 'r') as file:
            data = json.load(file)
            #space_availability_matrix.clear()
            return data
    except FileNotFoundError:
        return [[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]]

#parking_data =[] # to save user parking data

# Function to save parking data to a JSON file
def save_parking_data(parking_info):
    with open("parking_data.json", "w") as json_file:
        json.dump(parking_info, json_file)

# Function to load parking data from a file
def load_parking_data():
    try:
        with open("parking_data.json", 'r') as file:
            data = json.load(file)
            return data 
    except FileNotFoundError:
        return []
    



def space_availability():
    global space_availability_window 
    space_availability_window = tk.Tk()
    space_availability_window.title("Parking Management System")
    #Get the screen width and height
    screen_width = space_availability_window.winfo_screenwidth()
    screen_height = space_availability_window.winfo_screenheight()
    space_availability_window.geometry(f"{screen_width}x{screen_height}")

    space_availability_window.resizable(False,False)


    label = tk.Label(space_availability_window, text="Parking Slots", font=('calibri', 30, 'bold'))
    label.place(x='680',y='110')
    
    # Create a frame to contain the parking slots
    frame_for_slots = tk.Frame(space_availability_window)
    frame_for_slots.place(x='250', y='200')
    space_availability_matrix = load_space_availability_data()


    back_icon1 = PhotoImage(file="back.png")
    # Resize the image to fit within the button
    resized_back_icon1 = back_icon1.subsample(6, 6)  # Adjust the subsample factor as needed

    #action to be taken when back button is clicked
    def back_action():
        space_availability_window.destroy()
        homescreen()

    # Create back button
    back_button1 = tk.Button(space_availability_window,  image=resized_back_icon1, compound=tk.TOP,bd=0,command=back_action)
    back_button1.place(x='10',y='10')

    greenbox_label = tk.Label(space_availability_window, width=5, height=2, bg="green", relief="ridge")
    greenbox_label.place(x='30',y='250')
    greenbox_name_label = tk.Label(space_availability_window,text='Available',font=('calibri', 18))
    greenbox_name_label.place(x='90',y='250')

    redbox_label = tk.Label(space_availability_window, width=5, height=2, bg="Red", relief="ridge")
    redbox_label.place(x='30',y='300')
    redbox_name_label = tk.Label(space_availability_window,text='Not Available',font=('calibri', 18))
    redbox_name_label.place(x='90',y='300')


    
    rows = 5
    columns = 10
    for row in range(rows):
        for col in range(columns):
            if space_availability_matrix[row][col] == 0:
                slot_label = tk.Label(frame_for_slots, text=str(row * 10 + col + 1), width=15, height=7, bg="green", relief="ridge")
                slot_label.grid(row=row, column=col)
            else:
                slot_label = tk.Label(frame_for_slots, text=str(row * 10 + col + 1), width=15, height=7, bg="red", relief="ridge")
                slot_label.grid(row=row, column=col)


    space_availability_window.mainloop()

def parking(): 
    parking_window = tk.Tk()
    parking_window.title("Parking Management System")
    # Get the screen width and height
    screen_width = parking_window.winfo_screenwidth()
    screen_height = parking_window.winfo_screenheight()
    parking_window.geometry(f"{screen_width}x{screen_height}")

    parking_window.resizable(False,False)
    
    parking_data= load_parking_data() # to get the parked vehicle info
    space_availability_matrix = load_space_availability_data()

    back_icon1 = PhotoImage(file="back.png")
    # Resize the image to fit within the button
    resized_back_icon1 = back_icon1.subsample(6, 6)  # Adjust the subsample factor as needed

    #action to be taken when back button is clicked
    def back_action():
        parking_window.destroy()
        homescreen()

    # Create back button
    back_button1 = tk.Button(parking_window,  image=resized_back_icon1, compound=tk.TOP,bd=0,command=back_action)
    back_button1.place(x='10',y='10')
    # Create a label for parking vehicle
    label = tk.Label(parking_window, text="Enter Parking Details", font=('calibri', 30, 'bold'))
    label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    # Create a frame to contain details about parking vehicle
    frame_for_entry = tk.Frame(parking_window, bg='grey', width=600, height=300)
    frame_for_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    
    vehicle_id = tk.StringVar()
    vehicle_type = tk.StringVar()

    def entry_action():
        vehicle_id1=vehicle_id.get()
        vehicle_type1=vehicle_type.get()

        if vehicle_id1 == '':
            messagebox.showerror('Error','Please Enter your Vehicle Id ')
        elif vehicle_type1 == '':
            messagebox.showerror('Error','Please Select Vehicle Type')
        else:
            found_slot = False
            for row in range(5):
                for col in range(10):
                    if space_availability_matrix[row][col] == 0:
                        found_slot = True
                        parking_slot_no = row*10 + col+1
                        parking_data.append({'name':current_user['name'],'college_id':current_user['college_id'],'vehicle_id':vehicle_id1,'vehicle_type':vehicle_type1,'slot_no':parking_slot_no,
                                             'entry_time':formatted_time,'leaving_time': None,'left_status': False,'parking_cost':None})
                        messagebox.showinfo('Parking Successfull',f'You can park your vehicle {vehicle_id1} in parking slot {parking_slot_no}.')
                        space_availability_matrix[row][col]= 1
                        save_parking_data(parking_data)
                        save_space_availability_data(space_availability_matrix)
                        parking_window.destroy()
                        homescreen()

                        break
                if found_slot:
                    break
            
            if found_slot == False:
                messagebox.showerror('Error','Parking Space is full')



              

    label_collegeid = tk.Label(frame_for_entry, text="College Id",width=20,font=("bold", 10))
    label_collegeid.place(x=80,y=30)

    college_id = tk.StringVar()
    entry_collegeid = tk.Entry(frame_for_entry,textvariable=college_id,width=40,state="readonly")
    college_id.set(current_user['college_id'])
    entry_collegeid.place(x=300,y=30)

    label_vehicleid = tk.Label(frame_for_entry, text="Vehicle Id",width=20,font=("bold", 10))
    label_vehicleid.place(x=80,y=80)

    entry_vehicleid = tk.Entry(frame_for_entry,textvariable=vehicle_id,width=40)
    entry_vehicleid.place(x=300,y=80)

    label_vehicle_type = tk.Label(frame_for_entry, text="Vehicle Type",width=20,font=("bold", 10))
    label_vehicle_type.place(x=80,y=130)
    type1 =['Bicycle($0.5 per hour)','Motorcycle($0.8 per hour)','Car($1 per hour)']
    dropbox_vehicle_type = tk.OptionMenu(frame_for_entry,vehicle_type,*type1)
    dropbox_vehicle_type.config(width=33,height=1)
    vehicle_type.set('Select Vehicle type')
    dropbox_vehicle_type.place(x=300,y=130)
    label_entry_time = tk.Label(frame_for_entry, text="Entry Time",width=20,font=("bold", 10))
    label_entry_time.place(x=80,y=180)
    entry_time = tk.StringVar()
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime('%H:%M:%S %d-%m-%Y')
    entry_entry_time = tk.Entry(frame_for_entry,textvariable=entry_time,width=40,state="readonly")
    entry_time.set(formatted_time)
    entry_entry_time.place(x=300,y=180)

    login_button = tk.Button(frame_for_entry, text='Park Vehicle', width=20, bg='orange',font=('calibri', 12, 'bold'),command=entry_action)
    login_button.place(x=240, y=230)


    parking_window.mainloop()
    return

def leaving():
    #global parking_window 

    leaving_window = tk.Tk()
    leaving_window.title("Parking Management System")
    # Get the screen width and height
    screen_width = leaving_window.winfo_screenwidth()
    screen_height = leaving_window.winfo_screenheight()
    leaving_window.geometry(f"{screen_width}x{screen_height}")

    leaving_window.resizable(False,False)

    parking_data = load_parking_data() # to get parked vehicle info
    space_availability_matrix = load_space_availability_data()


    back_icon1 = PhotoImage(file="back.png")
    # Resize the image to fit within the button
    resized_back_icon1 = back_icon1.subsample(6, 6)  # Adjust the subsample factor as needed

    #action to be taken when back button is clicked
    def back_action():
        leaving_window.destroy()
        homescreen()

    # Create back button
    back_button1 = tk.Button(leaving_window,  image=resized_back_icon1, compound=tk.TOP,bd=0,command=back_action)
    back_button1.place(x='10',y='10')
    # Create a label for parking vehicle
    label = tk.Label(leaving_window, text="Enter Leaving Vehicle Details", font=('calibri', 30, 'bold'))
    label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Create a frame to contain details about passing vehicle
    frame_for_leaving = tk.Frame(leaving_window, bg='grey', width=600, height=250)
    frame_for_leaving.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    vehicle_id = tk.StringVar()

    def leaving_action():
        vehicle_id1=vehicle_id.get()
        

        if vehicle_id1 == '':
            messagebox.showerror('Error','Please Enter your Vehicle Id ')
        else:
            found_vehicle = False
            count = 0
            for data in parking_data:
                
                if data['left_status'] == False and vehicle_id1== data['vehicle_id']:
                    print('yes loop vitrw aayo')
                    found_vehicle = True
                    entry_datetime = datetime.strptime(data['entry_time'],'%H:%M:%S %d-%m-%Y')
                    time_difference = current_datetime - entry_datetime
                    hour_difference = time_difference.total_seconds()/3600

                    # Use regular expression to extract the bicycle type and cost per hour
                    match = re.match(r"(\w+)\(\$([\d.]+) per hour\)", data['vehicle_type'])
                    vehicle_type = match.group(1)
                    cost_per_hour = float(match.group(2))
                    total_parking_cost = round(hour_difference*cost_per_hour,2)
                    parking_data[count]['left_status'] = True
                    parking_data[count]['leaving_time'] = formatted_time
                    parking_data[count]['parking_cost'] = "$"+str(total_parking_cost)

                    col = (data['slot_no'] -1)%10
                    row = (data['slot_no'] -1)//10
                    print(row)
                    print(col)
                    print(space_availability_matrix[row][col])
                    
                    space_availability_matrix[row][col]=0
                    print(space_availability_matrix[row][col])
                    save_space_availability_data(space_availability_matrix)
                    save_parking_data(parking_data)
                    
                    print(parking_data)
                    messagebox.showinfo('Parking Ticket',f'Name: {data["name"]}\nCollege Id: {data["college_id"]}\nVehicle Id: {data["vehicle_id"]}\nVehicle Type: {vehicle_type}\nSlot No: {data["slot_no"]}\nEntry Time: {data["entry_time"]}\nExit Time: {formatted_time}]\nTotal Charge: ${total_parking_cost}')





                    leaving_window.destroy()
                    homescreen()

                count = count+1
                print(count)

            if not found_vehicle:
                messagebox.showerror('Error',f'There is no vehicle with id {vehicle_id1} parked in parking space.')


    label_collegeid = tk.Label(frame_for_leaving, text="College Id",width=20,font=("bold", 10))
    label_collegeid.place(x=80,y=30)

    college_id = tk.StringVar()
    entry_collegeid = tk.Entry(frame_for_leaving,textvariable=college_id,width=40,state="readonly")
    college_id.set(current_user['college_id'])
    entry_collegeid.place(x=300,y=30)

    label_vehicleid = tk.Label(frame_for_leaving, text="Vehicle Id",width=20,font=("bold", 10))
    label_vehicleid.place(x=80,y=80)

    entry_vehicleid = tk.Entry(frame_for_leaving,textvariable=vehicle_id,width=40)
    entry_vehicleid.place(x=300,y=80)

    label_leaving_time = tk.Label(frame_for_leaving, text="Leaving Time",width=20,font=("bold", 10))
    label_leaving_time.place(x=80,y=130)
    leaving_time = tk.StringVar()
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime('%H:%M:%S %d-%m-%Y')
    entry_leaving_time = tk.Entry(frame_for_leaving,textvariable=leaving_time,width=40,state="readonly")
    leaving_time.set(formatted_time)
    entry_leaving_time.place(x=300,y=130)

    leaving_button = tk.Button(frame_for_leaving, text='Exit Parking', width=20, bg='orange',font=('calibri', 12, 'bold'),command=leaving_action)
    leaving_button.place(x=240, y=180)


    leaving_window.mainloop()


def transaction_report():

    
    report_window = tk.Tk()
    report_window.title("Parking Management System")
    screen_width = report_window.winfo_screenwidth()
    screen_height = report_window.winfo_screenheight()
    report_window.geometry(f"{screen_width}x{screen_height}")
    report_window.resizable(False, False)

    parking_data_report = load_parking_data() # to display transactions

    def back_action():
        report_window.destroy()
        homescreen()

    back_icon1 = PhotoImage(file="back.png")
    resized_back_icon1 = back_icon1.subsample(6, 6)

    back_button1 = tk.Button(report_window, image=resized_back_icon1, compound=tk.TOP, bd=0,command=back_action)
    back_button1.place(x='10', y='10')


    label = tk.Label(report_window, text="Transaction Report", font=('calibri', 30, 'bold'))
    label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

    frame_for_slots = tk.Frame(report_window, width=800, height=600)
    frame_for_slots.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Creating a scrollable table using Treeview
    table_columns = ("Vehicle Id", "College ID", "Name", "Vehicle Type", "Entry Time","Exit Time","Total Charge")
    tree = ttk.Treeview(frame_for_slots, columns=table_columns, show="headings", height=20)

    # settting columns
    for col in table_columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor=tk.CENTER, stretch=tk.NO)  # Adjusting column width 
        #tree.column(col, stretch=tk.NO)  

    
    parking_data_report.reverse()
   
    # adding rowss
    for data in parking_data_report:
        match = re.match(r"(\w+)\(\$([\d.]+) per hour\)", data['vehicle_type'])
        vehicle_type = match.group(1)
        tuple = (data['vehicle_id'],data['college_id'],data['name'],vehicle_type,data['entry_time'],data['leaving_time'],str(data['parking_cost']))
        tree.insert("", "end", values=tuple)

    # Adding a scrollbar to the table
    scrollbar = ttk.Scrollbar(frame_for_slots, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)


    style = ttk.Style()
    style.configure("Treeview.Heading", font=('calibri', 12, 'bold'))
    style.configure("Treeview", rowheight=25, font=('calibri', 12))
    style.map("Treeview", background=[('selected', '#d9d9d9')])

    # Placing(packing) the tree i.e table and scrollbar
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    report_window.mainloop()

    


def homescreen():
    print(current_user)
    global homescreen_window 
    homescreen_window = tk.Tk()
    homescreen_window.title("Parking Management System")
    # Get the screen width and height
    screen_width = homescreen_window.winfo_screenwidth()
    screen_height = homescreen_window.winfo_screenheight()
    homescreen_window.geometry(f"{screen_width}x{screen_height}")

    homescreen_window.resizable(False,False)
    

    def space_availability_action():
        homescreen_window.destroy()
        space_availability()
    
    def logout():
        homescreen_window.destroy()
        mainmenu()

    def parking_action():
        homescreen_window.destroy()
        parking()

    def leaving_action():
        homescreen_window.destroy()
        leaving()

    def transaction_report_action():
        admin_window = tk.Toplevel(homescreen_window)
        screen_width = admin_window.winfo_screenwidth()
        screen_height = admin_window.winfo_screenheight()
        window_width = 400
        window_height = 300
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        admin_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        admin_window.title("admin login")
        admin_window.grab_set()

        label = tk.Label(admin_window, text="Admin Log In", font=('calibri', 16, 'bold'),height=20)
        label.place(relx=0.5,rely=0.15,anchor=tk.CENTER)
        frame_for_login = tk.Frame(admin_window,width=300,height=170,bg='grey')
        frame_for_login.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

        username=tk.StringVar()
        password=tk.StringVar()

        def login_action():
            username1=username.get()
            password1=password.get()
            if username1 == "admin" and password1 == "admin123":
                admin_window.destroy()
                homescreen_window.destroy()
                transaction_report()
            else:
                messagebox.showerror('Error','Username or Password dont match')
        label_name = tk.Label(frame_for_login, text="Username",width=10,font=("bold", 10))
        label_name.place(x='50',y='20')

        entry_name = tk.Entry(frame_for_login,textvariable=username,width=20)
        entry_name.place(x='160',y='20')

        label_password = tk.Label(frame_for_login, text="Password",width=10,font=("bold", 10))
        label_password.place(x='50',y='70')
        bullet="\u2022"

        entry_password = tk.Entry(frame_for_login,textvariable=password,show=bullet,width=20)
        entry_password.place(x='160',y='70')

        login_button = tk.Button(frame_for_login, text='Login',width=10,bg='orange',command=login_action,font=('calibri', 12, 'bold'))
        login_button.place(x='120',y='120')
        


    space_availability_icon = PhotoImage(file='availability1.png')
    parking_icon = PhotoImage(file='parking1.png')
    leaving_icon = PhotoImage(file='leaving1.png')
    report_icon = PhotoImage(file='report1.png')
    logout_icon = PhotoImage(file='logout1.png')
    
    #resizing images
    resized_space_availability_icon = space_availability_icon.subsample(2, 2) 
    resized_parking_icon = parking_icon.subsample(2, 2) 
    resized_leaving_icon = leaving_icon.subsample(2, 2) 
    resized_report_icon = report_icon.subsample(2, 2) 
    resized_logout_icon = logout_icon.subsample(2, 2) 
    # Create availability button
    availability_button = tk.Button(homescreen_window, text="Check Available Slot", image=resized_space_availability_icon, compound=tk.TOP,font=('calibri', 16, 'bold'),command=space_availability_action)
    availability_button.grid(row=0, column=0, padx=10, pady=50)

    # Create parking vehicle button
    parking_button = tk.Button(homescreen_window, text="Parking", image=resized_parking_icon, compound=tk.TOP,font=('calibri', 16, 'bold'),command=parking_action)
    parking_button.grid(row=0, column=1, padx=10, pady=50)

    # Create leaving vehicle button
    leaving_button = tk.Button(homescreen_window, text="Leaving", image=resized_leaving_icon, compound=tk.TOP,font=('calibri', 16, 'bold'),command=leaving_action)
    leaving_button.grid(row=0, column=2, padx=10, pady=50)

    # Create transaction report button
    report_button = tk.Button(homescreen_window, text="Transaction Details", image=resized_report_icon, compound=tk.TOP,font=('calibri', 16, 'bold'),command=transaction_report_action)
    report_button.grid(row=1,column=0, padx=10, pady=50)

    # Create logout button
    logout_button = tk.Button(homescreen_window, text="Logout", image=resized_logout_icon, compound=tk.TOP,font=('calibri', 16, 'bold'),command=logout)
    logout_button.grid(row=1, column=1, padx=10, pady=50)

    homescreen_window.columnconfigure(0,weight=1)
    homescreen_window.columnconfigure(1,weight=1)
    homescreen_window.columnconfigure(2,weight=1)
    #homescreen_window.rowconfigure(0,weight=1)
    #homescreen_window.rowconfigure(1,weight=1)






    homescreen_window.mainloop()


def login_page():
    menu.destroy()
    global login_window 
    login_window = tk.Tk()
    login_window.title("Parking Management System")
    # Get the screen width and height
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    login_window.geometry(f"{screen_width}x{screen_height}")

    login_window.resizable(False,False)
    rgb_tuple = login_window.winfo_rgb(login_window.cget("bg"))
    # Convert RGB values to hexadecimal
    hex_color = "#{:02x}{:02x}{:02x}".format(rgb_tuple[0] // 256, rgb_tuple[1] // 256, rgb_tuple[2] // 256)

    print(hex_color)


    label = tk.Label(login_window, text="Log In", font=('calibri', 30, 'bold'))
    label.place(x='680',y='110')
    frame_for_login = tk.Frame(login_window,width=600,height=200,bg='grey')
    frame_for_login.place(x='450',y='200')

    back_icon = PhotoImage(file="back.png")
    # Resize the image to fit within the button
    resized_back_icon = back_icon.subsample(6, 6)  # Adjust the subsample factor as needed

    #action to be taken when back button is clicked
    def back_action():
        login_window.destroy()
        mainmenu()

    # Create back button
    back_button = tk.Button(login_window,  image=resized_back_icon, compound=tk.TOP,bd=0,command=back_action)
    back_button.place(x='10',y='10')

    global current_user 
    current_user = dict() # to save details about logged user


    collegeid=StringVar()
    password=StringVar()
    connection1=sqlite3.connect("Members_Info.db")
    def login_action():
        collegeid1=collegeid.get()
        password1=password.get()
        if collegeid1 == "":
            messagebox.showerror('Error','Please Enter your College Id')
        elif password1=="":
                messagebox.showerror('Error','Please Enter your Password')
        else:
            #connection1.execute("create table if not exists Login1(regno varchar(20),password varchar(20))")
            #con.execute("insert into Login1 values(?,?)",(name,pword))
            #currentuser=name
            #con.commit()
            d = connection1.execute("select * from register")
            logged_in = False
            for i in d:
                if collegeid1==i[1] and password1==i[5]:
                    logged_in = True
                    current_user['name'] = i[0]
                    current_user['college_id'] = i[1]
                    current_user['post'] = i[2]
                    current_user['gender'] = i[3]
                    current_user['email'] = i[4]
                    current_user['mobile'] = i[6]
                    current_user['department'] = i[7]
                    messagebox.showinfo( "Login Successful", "You are logged in.")
                    login_window.destroy()
                    homescreen()
                    #cur_user=i[0]
            if logged_in==0:
                messagebox.showinfo( "Login Unsucessful", "Collegeid or passsword dont match")
                collegeid.set('')
                password.set("")
    label_name = Label(frame_for_login, text="College Id",width=20,font=("bold", 10))
    label_name.place(x=80,y=30)

    entry_name = Entry(frame_for_login,textvariable=collegeid,width=40)
    entry_name.place(x=300,y=30)

    label_password = Label(frame_for_login, text="Password",width=20,font=("bold", 10))
    label_password.place(x=80,y=80)
    bullet="\u2022"

    entry_password = Entry(frame_for_login,textvariable=password,show=bullet,width=40)
    entry_password.place(x=300,y=80)

    login_button = Button(frame_for_login, text='Login',width=20,bg='orange',command=login_action,font=('calibri', 12, 'bold'))
    login_button.place(x=240,y=130)

    login_window.mainloop()




def register_page():
    menu.destroy()
    global register_window
    register_window = tk.Tk()
    register_window.title("Parking Management System")
    # Get the screen width and height
    screen_width = register_window.winfo_screenwidth()
    screen_height = register_window.winfo_screenheight()
    register_window.geometry(f"{screen_width}x{screen_height}")

    register_window.resizable(False,False)


    label = tk.Label(register_window, text="Registration Form", font=('calibri', 30, 'bold'))
    label.place(x='600',y='50')
    frame_for_register = tk.Frame(register_window,width=600,height=600,bg='grey')
    frame_for_register.place(x='450',y='130')

    back_icon = PhotoImage(file="back.png")
    # Resize the image to fit within the button
    resized_back_icon = back_icon.subsample(6, 6)  # Adjust the subsample factor as needed

    def back_action():
        register_window.destroy()
        mainmenu()
    # Create back button
    back_button = tk.Button(register_window,  image=resized_back_icon, compound=tk.TOP,bd=0,command=back_action)
    back_button.place(x='10',y='10')

    

    name=StringVar()
    collegeid=StringVar()
    email=StringVar()
    password=StringVar()
    repassword = StringVar()
    mobile=StringVar()
    connection2=sqlite3.connect("Members_Info.db")

    def register_action():
        name1=name.get()
        collegeid1=collegeid.get()
        post_value1=post_type.get()
        gender_value1=gender_type.get()
        email1=email.get()
        password1=password.get()
        repassword1 = repassword.get()
        mobile1=mobile.get()
        depart_value1=depart_type.get()
        if name1 == '':
            messagebox.showerror('Error','Please Enter your Name')
        elif collegeid1 == '':
            messagebox.showerror('Error','Please Enter your College Id')
        elif post_value1 == '':
            messagebox.showerror('Error','Please Select your Post')
        elif gender_value1 == '':
            messagebox.showerror('Error','Please Select your Gender')
        elif email1 == '':
            messagebox.showerror('Error','Please Choose your Email')
        elif password1 == '':
            messagebox.showerror('Error','Please Enter your Password')
        elif repassword1 == '':
            messagebox.showerror('Error','Please Re-Enter your Password')
        elif mobile1 == '':
            messagebox.showerror('Error','Please Enter your Mobile')
        elif depart_value1 == '':
            messagebox.showerror('Error','Please Select your Department')
        else:
            if password1 != repassword1:
                messagebox.showerror("Registration Failed", "Passwords do not match")
            else:
                connection2.execute("create table if not exists register(Name text,Collegeid text, Post text,Gender text,Emailid text,Password text,Mobile text,Department text);")
                connection2.execute("insert into register values(?,?,?,?,?,?,?,?)",(name1,collegeid1,post_value1,gender_value1,email1,password1,mobile1,depart_value1))
                connection2.commit()
                p=connection2.execute("select * from register")
                for i in p:
                    print("Username",i[1])
                    print("Password",i[5])

                messagebox.showinfo("Parking Management System","Registered Successfully!")
                #register_window.destroy()

    label_name = Label(frame_for_register, text="Name",width=20,font=("bold", 10))
    label_name.place(x=80,y=30)

    entry_name = Entry(frame_for_register,textvariable=name,width=40)
    entry_name.place(x=300,y=30)

    label_id = Label(frame_for_register, text="College Id",width=20,font=("bold", 10))
    label_id.place(x=80,y=80)

    entry_id = Entry(frame_for_register,textvariable=collegeid,width=40)
    entry_id.place(x=300,y=80)

    label_post = Label(frame_for_register, text="Post",width=20,font=("bold", 10))
    label_post.place(x=80,y=130)
    list1=['STAFF','STUDENT']
    post_type=StringVar()
    droplist_post=OptionMenu(frame_for_register,post_type, *list1)
    droplist_post.config(width=33,height=1)
    post_type.set('Select your Post')
    droplist_post.place(x=300,y=130)                         

    label_gender = Label(frame_for_register, text="Gender",width=20,font=("bold", 10))
    label_gender.place(x=80,y=180)
    list2=['MALE','FEMALE']
    gender_type=StringVar()
    droplist_gender=OptionMenu(frame_for_register,gender_type, *list2)
    droplist_gender.config(width=33,height=1)
    gender_type.set('Select your Gender')
    droplist_gender.place(x=300,y=180)

    label_email = Label(frame_for_register, text="Email-id",width=20,font=("bold", 10))
    label_email.place(x=80,y=230)

    entry_email = Entry(frame_for_register,textvariable=email,width=40)
    entry_email.place(x=300,y=230)

    label_mobile = Label(frame_for_register, text="Mobile Number",width=20,font=("bold", 10))
    label_mobile.place(x=80,y=280)

    entry_mobile = Entry(frame_for_register,textvariable=mobile,width=40)
    entry_mobile.place(x=300,y=280)

    label_depart = Label(frame_for_register, text="Department",width=20,font=("bold", 10))
    label_depart.place(x=80,y=330)

    list3 = ['SMART COMPUTING','HOTEL MANAGEMENT','BUSINESS ADMINISTRATION','KOREAN CULTURE']
    depart_type=StringVar()
    droplist_department=OptionMenu(frame_for_register,depart_type, *list3)
    droplist_department.config(width=33,height=1)
    depart_type.set('Select your Department')
    droplist_department.place(x=300,y=330)

    label_password = Label(frame_for_register, text="Password",width=20,font=("bold", 10))
    label_password.place(x=80,y=380)
    bullet="\u2022"
    entry_password = Entry(frame_for_register,textvariable=password,show=bullet,width=40)
    entry_password.place(x=300,y=380)

    label_repassword = Label(frame_for_register, text="Confirm Password",width=20,font=('calibri', 12))
    label_repassword.place(x=80,y=430)

    entry_repassword = Entry(frame_for_register, textvariable=repassword, show=bullet,width=40)
    entry_repassword.place(x=300,y=430)

    register_button = Button(frame_for_register, text='Register',width=20,bg='orange',command=register_action,font=('calibri', 12, 'bold'))
    register_button.place(x=240,y=480)

    register_window.mainloop()


def mainmenu():
    global menu
    menu = tk.Tk()
    menu.title("Parking Management System")
    # Get the screen width and height
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()
    
    # Set the window dimensions to match the screen
    menu.geometry(f"{screen_width}x{screen_height}")
    #menu.configure(bg="white")  # Set background color
    menu.resizable(False,False)
    # Title Label
    label = tk.Label(menu, text="Parking Management System", font=('calibri', 30, 'bold'))
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=(50, 20))

    # Load button icons
    login_icon = PhotoImage(file="login1.png")
    register_icon = PhotoImage(file="register1.png")
    login_icon_resized = login_icon.subsample(2,2)
    register_page_resized = register_icon.subsample(2,2)

    # Create login button
    login_button = tk.Button(menu, text="Login", image=login_icon_resized, compound=tk.TOP, command=login_page,font=('calibri', 16, 'bold'))
    login_button.grid(row=1, column=0, padx=10, pady=130)

    # Create register button
    register_button = tk.Button(menu, text="Register", image=register_page_resized, compound=tk.TOP, command=register_page,font=('calibri', 16, 'bold'))
    register_button.grid(row=1, column=1, padx=10, pady=130)

    # Configure columns to expand
    menu.columnconfigure(0, weight=1)
    menu.columnconfigure(1, weight=1)
    #menu.columnconfigure(2, weight=1)


    menu.mainloop()

if __name__ == "__main__":
    mainmenu()
