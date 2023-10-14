import os
from flet import *
import shutil
import cv2
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

#NOTE: import the script that runs the brain tumor segmentation
from src import run
controls_dict = {}
save = []

class Button(UserControl):
    """This class is used to create the buttons that will be used in the application."""

    def __init__(self, btn_name, btn_width, btn_function, btn_color):
        """Initiliaze the button with the parameters."""
        self.btn_name = btn_name
        self.btn_width = btn_width
        self.btn_function = btn_function
        self.btn_color = btn_color
        super().__init__()
 
    def build(self):
        """Builds the button with the parameters passed in the constructor."""
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

class Segmentation(UserControl):
    """This class is used to create the Segmentation page."""

    def __init__(self):
        """Initialize the file and folder picker buttons and the session list."""
        self.btn_callback_files = FilePicker(on_result=self.segmentation_files)
        self.btn_callback_folder = FilePicker(on_result=self.segmentation_folder)
        self.session = []
        super().__init__()
  
    def segmentation_folder(self, e: FilePickerResultEvent):
        """Saves the output image in a selected folder."""
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

    #NOTE: update path
    def convert(self, array):
        """Saves the image in the tmp folder."""
        directory = settings.path_to_tmp  
        now = datetime.now()
        file_name = now.strftime("%H:%M:%S")
        t = f"{file_name}.png"
        path = directory + "/" + t
        cv2.imwrite(path, array)
        return path

    def start_segmentation(self):
        """Starts the segmentation process of the image after the user has selected the image and clicked on the button."""
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
            final, probablita, area, tumor_type = run.main(file_to_segment)
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

    def return_file_list(self, file_icon, file_name, file_path):
        """Appends the file to the file list."""
        return Column(
            spacing=1,
            controls=[
                Row(controls=[Icon(file_icon, size=12),Text(file_name, size=13),]),
                Row(controls=[Text(file_path, size=9,no_wrap=False, color="white54"),])
            ]
        )

    def error_msg(self, type, msg):
        """Returns the error msg."""
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
    
    #NOTE: update path
    def clean_directory(self):
        """Cleans the tmp directory of the png files generated."""
        directory = settings.path_to_tmp
        skip_directory = 'err' 
        for root, dirs, files in os.walk(directory): 
            if skip_directory in dirs:
                    dirs.remove(skip_directory) # skip the directory 
            for file in files:
                if file.endswith(".png"):
                        os.remove(os.path.join(root, file))

    def return_stats(self, icon, name, value):
        """Appends the stats text to the container that will be displayed.""" 
        value = value
        self.column = Column(
            spacing=1,
            controls=[
                Row(controls=[Icon(icon, size=12),Text(name, size=13),]),
                Row(controls=[Text(value, size=9,no_wrap=False, color="white54"),])
            ]
        )
        return self.column
    
    def append_image(self, file_path):
        """Appends the image to the container that will be displayed."""
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

    def segmentation_files(self, e: FilePickerResultEvent):
        """Adds images to the view and the file to the file list."""
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

    def segmentation_title(self):
        """Builds the title for the page."""
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

    def step_one(self):
        """Builds the buttons for UI."""
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
                    Button("Clean Directory", 150,lambda __: self.clean_directory(),"red"),
                ]
            )
        ) 

    def step_two(self):
        """Builds the container for the file list."""
        self.container = Container(
            height=60,
            border=border.all(0.8, "white24"),
            border_radius=6,
            padding=12,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )
        controls_dict["files"] = self.container
        return self.container

    def step_three(self, title):
        """Builds the container for the before and after images."""
        self.title = title
        self.container = Container(
            height= 360,
            width=420,
            border_radius=6,
            border = border.all(0.8, "white24"),
        )
        controls_dict[self.title] = self.container
        return self.container

    def step_four(self, title):
        """Builds the container for the stats of the segmentation."""
        self.container = Container(
            height=60,
            width=275,
            border=border.all(0.8, "white24"),
            border_radius=6,
            padding=12,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )
        controls_dict[title] = self.container
        return self.container
    
    def build(self):
        """Main entry point for the view, builds the UI and returns the root control."""
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
                Text("Stats and Tumor Type", size=16, weight="bold"),
                Row(controls=[self.step_four("probabilita"),self.step_four("area"), self.step_four("tumor_type")]),
                Divider(height=50, color="transparent"),
            ]
        )