import flet 
from flet import *
import os

controls_dict = {}

class Button(UserControl):
    def __init__(self, btn_name, btn_width, btn_function):
        self.btn_name = btn_name
        self.btn_width = btn_width
        self.btn_function = btn_function
        super().__init__()
    
    def build(self):
        return ElevatedButton(
            on_click=self.btn_function,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(self.btn_name, size=11, weight="bold"),
                ],
            ),
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=6)},
                color={"":"white"},
            ),
            height=48,
            width=self.btn_width,
        )

class Segmentation(UserControl):
    def __init__(self):

        self.btn_callback_files = FilePicker(on_result=self.segmentation_files)
        self.btn_callback_folder = FilePicker(on_result=self.segmentation_folder)
        self.session = []
        super().__init__()

    def return_file_list(self, file_icon, file_name, file_path):
        return Column(
            spacing=1,
            controls=[
                Row(
                    controls=[
                        Icon(file_icon, size=12),
                        Text(file_name, size=13),
                    ]
                ),
                Row(
                    controls=[
                        Text(file_path, size=9,no_wrap=False, color="white54"),
                    ]
                )
            ]
        )

    def segmentation_folder(self, e: FilePickerResultEvent):
        self.session=[]
        if e.path:
            control = controls_dict['files']
            control.content = Column(scroll='auto', expand=True)
            self.session.append(e.path)
            self.update()
            control.content.controls.append(
                Row(
                    controls=[
                        Icon(icons.FOLDER_COPY_ROUNDED, size=12),
                        Text(e.path, size=13),
                    ]
                ),
            )
            control.content.controls.append(
                Container(
                    padding=padding.only(left=18),
                    content=Column(expand=True),
                )
            )
            for file in os.listdir(e.path):
                file_path = os.path.join(e.path + "/" + file)
                control.content.controls[1].content.controls.append(
                    self.return_file_list(icons.FILE_COPY_ROUNDED, file, file_path)
                )
            control.content.update()
        pass

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

    def segmentation_title(self):
        return Container(
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("Brain Tumor Segmentation", size=18, weight="bold"),
                    IconButton(
                        content=Text(
                            "x",
                            weight="bold",
                            size=18,
                        ),
                        on_click=lambda __: self.page.window_close(),
                    )
                ]
            )
        )
    
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
                    Button("Upload File", 260, 
                           lambda __: self.btn_callback_files.pick_files(allow_multiple=False),
                           ),
                    self.btn_callback_files,
                    self.btn_callback_folder,
                    Button("Start Segmentation", 260,
                           lambda __: self.btn_callback_folder.get_directory_path(),
                           ),
                    Button("Save Output", 260,
                           lambda __: self.btn_callback_folder.get_directory_path(),
                           ),
                ]
            )
        )
    
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
    
    def step_three(self):
        return Container(
            height= 380,
            width=420,
            border_radius=6,
            border = border.all(0.8, "white24"),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                spacing=5,
                controls=[
                    Row(
                        spacing=0,
                        controls=[
                            #Image("/Users/lucian/Documents/GitHub/BrainCancerDetection/gui/data/1.jpg"),  
                        ]
                    ),
                ]
            ),

        )
        pass
    #NOTE: Main entry point for the Segmentation page
    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.segmentation_title(),
                #Divider(height=20, color="transparent"),
                #Text("", size=14, weight="bold"),
                self.step_one(),
                
                Divider(height=10, color="transparent"),
                Text("Input file", size=14, weight="bold"),
                self.step_two(),
                Divider(height=10, color="transparent"),
                Text("Before and After", size=14, weight="bold"),
                Row(
                   controls=[
                    self.step_three(),
                    self.step_three(),
                   ]
                ),
                

            ]
        )