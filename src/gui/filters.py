import os
import shutil
from flet import *
import cv2
from datetime import datetime

#NOTE: import the button class and the script that runs the filters
from src.gui.segmentation import Button
from src.filter import main

controls_dict = {}
data = []
image=[]
history = []
save = []
'''
Class for the counter segment 
'''
class AppCounter(UserControl):
    '''
    Initialize the class
    '''
    def __init__(self):
        super().__init__()
    '''
    Add values to the app counter
    ''' 
    def app_counter_add(self, e):
        count = int(self.app_counter_text.value) + 10
        self.app_counter_text.value = str(count)
        self.app_counter_text.update()
    '''
    Decrement values from the app counter
    '''
    def app_counter_sub(self, e):
        count = int(self.app_counter_text.value) - 10
        self.app_counter_text.value = str(count)
        self.app_counter_text.update()
    '''
    Builds the counter segment
    '''
    def build(self):
        self.app_counter_text=Text("0", size=12, color='black')
        return Container(
            height=35,
            border_radius=6,
            bgcolor="#ebebeb",
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    IconButton(
                        icon=icons.ADD_ROUNDED,
                        icon_size=15,
                        icon_color="black",
                        on_click=lambda e: self.app_counter_add(e),
                    ),
                    self.app_counter_text,
                    IconButton(
                        icon=icons.REMOVE_ROUNDED,
                        icon_size=15,
                        icon_color="black",
                        on_click=lambda e: self.app_counter_sub(e)
                    ),
                ],
            ),
        )
'''
Class for the Menu segment
'''
class AppSizeMenu(UserControl):
    '''
    Initialize the class
    '''
    def __init__(self):
        super().__init__()
    '''
    Change the box based on the box selected by the user
    '''
    def change_box(self, e):
        for check in self.controls[0].content.controls[:]:
            check.controls[1].content.value=False
            check.controls[1].content.update()

            e.control.value=True
            e.control.update()
        pass
    '''
    Returns the Container for the segment
    '''
    def app_size_container(self):
        return Container(
            border_radius=30,
            width=25,
            height=25,
            border=border.all(2,"black"),
            alignment=alignment.center,
            content=Checkbox(
                fill_color="Transparent",
                check_color="black",
                on_change=lambda e:self.change_box(e),
            ),
        )
    '''
    Returns the Column for the segment
    '''
    def app_size_main_builder(self, size:str):
        return Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=1,
            controls=[
                Text(
                    value=size,
                    size=9,
                    color="black",
                    weight="bold",
                ),
                self.app_size_container()
            ]
        )
    '''
    Builds the menu segment
    '''
    def build(self):
        return Container(
            height=45,
            border_radius=6,
            bgcolor="#ebebeb",
            content=Row(
                alignment=MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    self.app_size_main_builder("Yes"),
                    self.app_size_main_builder("No"),
                ],
            )
        )
'''
Class for the button
'''
class AppButton(UserControl):
    '''
    Initialize the class
    '''
    def __init__(self, function):
        self.function = function
        super().__init__()
    '''
    Builds the button
    '''
    def build(self):
        return Container(
            alignment=alignment.center,
            content=ElevatedButton(
                on_click=self.function,
                bgcolor="orange",
                color="white",
                height=45,
                content=Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text("Generate Image", size=13, weight="bold"),
                    ]
                ),
                style=ButtonStyle(
                    shape={"": RoundedRectangleBorder(radius=6)},
                ),
            ),
        )
'''
Class for the filters
'''
class Filters(UserControl):
    '''
    Initialize the class with the file pickers and the session list
    '''
    def __init__(self):
        self.btn_callback_files = FilePicker(on_result=self.segmentation_files)
        self.btn_callback_folder = FilePicker(on_result=self.segmentation_folder)
        self.session = []
        super().__init__()
    '''
    Returns the title for the page
    '''   
    def filters_title(self):
        return Container(
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("Segmentation Filters", size=18, weight="bold"),
                    IconButton(
                        content=Text("x",
                            weight="bold",
                            size=18,
                        ),
                        on_click=lambda __: self.page.window_close(),
                    )
                ]
            )
        )
    '''
    Returns the file list for the container 
    '''   
    def return_file_list(self, file_icon, file_name, file_path):
        return Column(
            spacing=1,
            controls=[
                Row(controls=[Icon(file_icon, size=12),Text(file_name, size=13),]),
                Row(controls=[Text(file_path, size=9,no_wrap=False, color="white54"),])
            ]
        )
    '''
    Returns the file selected by the user
    '''   
    def segmentation_files(self, e: FilePickerResultEvent):
        self.session=[]
        if e.files:
            control = controls_dict['files']
            control.content = Column(
                scroll='auto',
                expand=True,
            )
            self.update()
            for file in e.files:
                self.session.append(file.path)
                control.content.controls.append(
                    self.return_file_list(
                        icons.FILE_COPY_ROUNDED, file.name, file.path
                    )
                )
                control.content.update()
        else:
            pass
    '''
    Returns the error message 
    '''   
    def error_msg(self, type, msg):
        if type == 'Error':
            icon = icons.ERROR_OUTLINE
            text = 'Error message'
            col = "red"
        elif type == 'Success':
            icon = icons.CHECK_CIRCLE_OUTLINE
            text = 'Success message'
            col = "green"
        else:
            pass
        self.column = Column(
            spacing=1,
            controls=[
                Row(controls=[Icon(icon, size=12),Text(text, size=13, color=col)]),
                Row(controls=[Text(msg, size=9,no_wrap=False, color="white54"),])
            ]
        )
        return self.column
    '''
    Returns the buttons that can be selected by the user 
    to upload  files, start segmentation etc..
    '''   
    def step_one(self):
        return Container(
            height=80,
            border=border.all(0.8, "white24"),
            border_radius=6,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    self.btn_callback_files,
                    self.btn_callback_folder,
                    Button("Upload Image", 240, 
                           lambda __: self.btn_callback_files.pick_files(allow_multiple=False,allowed_extensions = ["png", "jpg", "jpeg"]),"blue"
                           ),
                    Button("Save Ouput Image", 240,
                           lambda __: self.btn_callback_folder.get_directory_path(),"blue"
                           ),
                    Button("Clean", 150,lambda __: self.clean_directory(),"red"),
                ]
            )
        )
    '''
    returns the container that shows the file selected
    '''   
    def step_two(self):
        self.container = Container(
            height=60,
            border=border.all(0.8, "white24"),
            border_radius=6,
            padding=12,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )

        controls_dict["files"] = self.container

        return self.container
    '''
    Cleans the tmp directory of the png files generated
    #NOTE: update the path to the tmp folder
    '''
    def clean_directory(self):
        dir = './tmp'
        skip_directory = 'err'
        for root, dirs, files in os.walk(dir):
                if skip_directory in dirs:
                    dirs.remove(skip_directory) # skip the directory
                for file in files:
                    if file.endswith(".png"):
                        os.remove(os.path.join(root, file))
    '''
    Converts the image returned by the  script
    to  a png file
    #NOTE: update the path to the tmp folder
    '''   
    def convert(self, array):
        dir = './tmp/filters'
        now = datetime.now()
        file_name = now.strftime("%H:%M:%S")
        t = f"{file_name}.png"
        path = dir + "/" + t
        cv2.imwrite(path, array)
        return path
    '''
    Generates the output image by calling
    the filters script and running it
    '''  
    def generate_image(self, e):
        stuff = data[-1]
        data_list = []
        c = []
        for d in stuff:
            if not isinstance(d, Text):
                if not isinstance(d, Divider):
                    if not isinstance(d, AppButton):
                        data_list.append(d.controls[0].content)   
        for p in data_list:
            for item in p.controls[:]:
                if isinstance(item, Text):
                    c.append(item.value)
                if isinstance(item, Column):
                    for checks in item.controls[:]:
                        if isinstance(checks, Container):
                            if checks.content.value == True:
                                ans = str(item.controls[0].value)
                                c.append(ans)
        if len(self.session) == 0:
            control = controls_dict['files']
            control.content = Column(
                scroll='auto',
                expand=True,
            )
            self.update()
            control.content.controls.append(self.error_msg("Error", "Please upload an image"))
            control.content.update()
        else:
            result = main(c, self.session[-1])
            if type(result) == str:
                control = controls_dict['error']
                control.content = Column(
                    scroll='auto',  
                    expand=True,
                )
                self.update()
                control.content.controls.append(self.error_msg("Error", result))
                control.content.update()
            else:
                path = self.convert(result)
                image[-1].controls.append(
                    Container(
                        width=400,
                        height=400,
                        image_src=path,
                        image_fit='cover',
                        border_radius=8,)
                )
                image[-1].update()
                history.append(path)
                control = controls_dict['error']
                control.content = Column(
                    scroll='auto',  
                    expand=True,
                )
                self.update()
                control.content.controls.append(self.error_msg("Success", "Congratulations, your image has been generated!"))
                control.content.update()
                save.append(path) 
    '''
    Saves the output image in a selected folder
    '''
    def segmentation_folder(self, e: FilePickerResultEvent):
        if e.path:
            try:
                path = save[-1]
                now = datetime.now()
                file_name = now.strftime("%H_%M_%S")
                t = f"{file_name}.png"
                dir = e.path + "/" + t
                shutil.copy(path, dir)
                control = controls_dict['error']
                control.content = Column(
                    scroll='auto',
                    expand=True,
                )
                self.update()
                control.content.controls.append(self.error_msg("Success", "Congratulations, your image has been saved at the selected location : " + dir))
                control.content.update()
            except Exception as e:
                print("Failed to save file")
    '''
    Returns the card that contains
    the filters selection and output image
    '''
    def card(self):
        self.container = Container(
            height=400,
            border=border.all(0.8, "white24"),
            border_radius=6,
            padding=10,
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Container(
                        width=280,
                        #height=400,
                        content=Column(
                          controls=[
                            Text("Increment/decrement light", size=12, weight="bold"),
                            AppCounter(),
                            Text("Color inside segmentation", size=12, weight="bold"),
                            AppSizeMenu(),
                            Text("Get only the tumor", size=12, weight="bold"),
                            AppSizeMenu(),
                            Text("Without segmentation", size=12, weight="bold"),
                            AppSizeMenu(),
                            Divider(height=0, color="transparent"),
                            AppButton(lambda e: self.generate_image(e)),
                          ]  
                        ),
                    ),
                    VerticalDivider(
                        width=40,
                        color="white"
                    ),
                    Container(
                        width=400,
                        height=400,
                        content=Column(
                            scroll = 'auto',
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[]
                        )
                    ),                
                ]
            )
        )
        instance = self.container.content.controls[0].content.controls[:]
        p=self.container.content.controls[2].content
        data.append(instance)
        image.append(p)
        return self.container
    '''
    Returns the error container that contains
    the error/success message
    '''
    def error(self):
        self.container = Container(
            height=60,
            border=border.all(0.8, "white24"),
            border_radius=6,
            padding=12,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )

        controls_dict["error"] = self.container

        return self.container
    '''
    Builds the filters view 
    '''
    def build(self):
        self.column = Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.filters_title(),
                self.step_one(),
                Text("Input File", size=16, weight="bold"),
                self.step_two(),
                Text("Select Options", size=16, weight="bold"),
                self.card(),
                self.error(),
            ]
        )
        return self.column
