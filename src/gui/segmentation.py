import os
from flet import *
import shutil
import cv2
from datetime import datetime

#NOTE: import the script that runs the brain tumor segmentation
from src import run
controls_dict = {}
save = []

'''
This class is used to create the buttons that will be used in the application.
'''
class Button(UserControl):
    '''
    Initiliaze the button with the parameters
    '''
    def __init__(self, btn_name, btn_width, btn_function, btn_color):
        self.btn_name = btn_name
        self.btn_width = btn_width
        self.btn_function = btn_function
        self.btn_color = btn_color
        super().__init__()
    '''
    Builds the button with the parameters passed in the constructor
    '''
    def build(self):
        return ElevatedButton(
            on_click=self.btn_function,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[Text(self.btn_name, size=13, weight="bold")],
            ),
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=6)},
                color={"":"white"},
                bgcolor={"": self.btn_color},
            ),
            height=48,
            width=self.btn_width,
        )
'''
This class is used to create the Segmentation page.
'''
class Segmentation(UserControl):
    '''
    Initialize the file and folder picker buttons and the session list
    '''
    def __init__(self):
        self.btn_callback_files = FilePicker(on_result=self.segmentation_files)
        self.btn_callback_folder = FilePicker(on_result=self.segmentation_folder)
        self.session = []
        super().__init__()
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
            except Exception as e:
                print("Failed to save file")
    '''
    Saves the image in the tmp folder
    #NOTE: update the path to the tmp folder
    '''
    def convert(self, array):
        dir = "./tmp"   
        now = datetime.now()
        file_name = now.strftime("%H:%M:%S")
        t = f"{file_name}.png"
        path = dir + "/" + t
        cv2.imwrite(path, array)
        return path
    '''
    Starts the segmentation process of the image after the user has selected the image and clicked on the button
    '''
    def start_segmentation(self):
    	
        if len(self.session) == 0:
            control = controls_dict['files']
            control.content = Column(
                scroll='auto',
                expand=True,
            )
            self.update()
            control.content.controls.append(self.error_msg("Error", "Please upload a file"))
            control.content.update()
        else:
            print("Starting process")
            file_to_segment = self.session[0]
            final, probablita, area,tumor_type = run.main(file_to_segment)
            if probablita == 0 and area == 0:
                path = "./tmp/err/error_image.png"
                view = controls_dict['After']
                view_probabilita = controls_dict['probabilita']
                view_area = controls_dict['area']
                view_area.content = Column()
                view_probabilita.content = Column()
                view_type = controls_dict['tumor_type']
                view_type.content = Column()
                view.content = Column()

                self.update()
                view_area.content.controls.append(self.return_stats("bar_chart", "Tumor Area", "Tumor not found"))
                view_probabilita.content.controls.append(self.return_stats("bar_chart", "Tumor Probability", "Tumor not found"))
                view_type.content.controls.append(self.return_stats("bar_chart", "Tumor Type", "Tumor not found"))
                view.content.controls.append(self.append_image(path))
                view.content.update()
                view_probabilita.content.update()
                view_area.content.update()
                view_type.content.update()
            else:
                #print("Tumor type: ", tumor_type)
                path = self.convert(final) 
                view = controls_dict['After']
                view_probabilita = controls_dict['probabilita']
                view_area = controls_dict['area']
                view_area.content = Column()
                view_probabilita.content = Column()
                view_type = controls_dict['tumor_type']
                view_type.content = Column()
                view.content = Column()
                self.update()
                view.content.controls.append(self.append_image(path))
                view_probabilita.content.controls.append(self.return_stats("bar_chart", "Tumor Probability", str(probablita)+"%"))
                view_area.content.controls.append(self.return_stats("bar_chart", "Tumor Area ", str(area*100)+"%"))
                view_type.content.controls.append(self.return_stats("bar_chart", "Tumor Type", tumor_type))
                save.append(path)
                view.content.update()
                view_probabilita.content.update()
                view_area.content.update()
                view_type.content.update()

        
    '''
    Appends the file to the file list
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
    Returns the error msg
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
    Cleans the tmp directory of the png files generated 
    #NOTE: update the path to the tmp folder
    '''
    def clean_directory(self):
        dir = "./tmp"
        skip_directory = 'err' 
        for root, dirs, files in os.walk(dir): 
            if skip_directory in dirs:
                    dirs.remove(skip_directory) # skip the directory 
            for file in files:
                if file.endswith(".png"):
                        os.remove(os.path.join(root, file))
    '''
    Appends the stats text to the container that will be displayed
    '''
    def return_stats(self, icon, name, value):
        value = value
        self.column = Column(
            spacing=1,
            controls=[
                Row(controls=[Icon(icon, size=12),Text(name, size=13),]),
                Row(controls=[Text(value, size=9,no_wrap=False, color="white54"),])
            ]
        )
        return self.column
    '''
    Appends the image to the container that will be displayed
    '''
    def append_image(self, file_path):
        if file_path.endswith('mat'):
            path = run.load_image_nii(file_path)
        else:
            path = file_path
        self.column =Column(
            alignment=CrossAxisAlignment.CENTER,
            horizontal_alignment=MainAxisAlignment.CENTER,
            controls=[Image(path, height=350, width=430, fit="contain")]
        )
        return self.column
    '''
    Adds images to the view and the file to the file list
    '''
    def segmentation_files(self, e: FilePickerResultEvent):
        self.session=[]
        if e.files:
            control = controls_dict['files']
            control.content = Column(scroll='auto',expand=True)
            view = controls_dict['Before']
            t = controls_dict['After']
            view.content = Column()
            t.content = Column()
            self.update()
            for file in e.files:
                self.session.append(file.path)
                control.content.controls.append(self.return_file_list(icons.FILE_COPY_ROUNDED, file.name, file.path))
                view.content.controls.append(self.append_image(file.path))
                control.content.update()
                view.content.update()
        else:
            # do nothing =(
            pass
    '''
    Builds the title for the page
    '''
    def segmentation_title(self):
        return Container(
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("Brain Tumor Segmentation and Classification", size=18, weight="bold"),
                    IconButton(content=Text("x",weight="bold",size=18),on_click=lambda __: self.page.window_close())
                ]
            )
        ) 
    '''
    Builds the buttons for UI
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
                    Button("Upload File", 160,lambda __: self.btn_callback_files.pick_files(allow_multiple=False, allowed_extensions = ["png", "jpg", "jpeg", "mat"]),"blue"),
                    Button("Start", 200,lambda __: self.start_segmentation(),"green"),
                    Button("Save Output Image", 200,lambda __: self.btn_callback_folder.get_directory_path(),"blue"),
                    Button("Clean", 150,lambda __: self.clean_directory(),"red"),
                ]
            )
        ) 
    '''
    Builds the container for the file list
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
    Builds the container for the before and after images
    '''
    def step_three(self, title):
        self.title = title
        self.container = Container(
            height= 360,
            width=420,
            border_radius=6,
            border = border.all(0.8, "white24"),
        )
        controls_dict[self.title] = self.container
        return self.container
    '''
    Builds the container for the stats of the segmentation
    '''
    def step_four(self, title):
        self.container = Container(
            height=60,
            width=420,
            border=border.all(0.8, "white24"),
            border_radius=6,
            padding=12,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )
        controls_dict[title] = self.container
        return self.container
    


    
    '''
    Main entry point for the view, builds the UI and returns the root control.
    '''
    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.segmentation_title(),
                self.step_one(),
                Text("Input File", size=16, weight="bold"),
                self.step_two(),
                Text("Before and After", size=16, weight="bold"),
                Row(controls=[self.step_three("Before"),self.step_three("After")]),
                Text("Stats", size=16, weight="bold"),
                Row(controls=[self.step_four("probabilita"),self.step_four("area")]),
                Text("Type", size=16, weight="bold"),
                Row(controls=[self.step_four("tumor_type"),]),
                Divider(height=50, color="transparent"),
            ]
        )
