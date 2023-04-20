import flet 
from flet import *
from segmentation import Button

class AppForm(UserControl):
    def __init__(self, name: str, end_name: str):
        self.name = name
        self.end_name = end_name
        super().__init__()

    def build(self):
        return Container(
            height=45,
            bgcolor="#ebebeb",
            border_radius=6,
            padding=8,
            alignment=alignment.center_left,
            content=Column(
                spacing=1,
                controls=[
                    TextField(
                        border_color="transparent",
                        height=19,
                        text_size=13,
                        content_padding=5,
                        cursor_color="black",
                        cursor_width=1,
                        cursor_height=18,
                        color="black",
                        suffix_text=self.end_name,
                        suffix_style=TextStyle(color="black"),
                        prefix_text=self.name,
                        prefix_style=TextStyle(color="black"),
                    ),
                ],
            ),
        )

class AppCounter(UserControl):
    def __init__(self):
        super().__init__()
    
    def app_counter_add(self, e):
        count = int(self.app_counter_text.value) + 1
        self.app_counter_text.value = str(count)
        self.app_counter_text.update()

    def app_counter_sub(self, e):
        count = int(self.app_counter_text.value) - 1
        self.app_counter_text.value = str(count)
        self.app_counter_text.update()

    def build(self):
        self.app_counter_text=Text("0", size=12, color='black')
        return Container(
            height=45,
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
    pass

class AppSizeMenu(UserControl):
    def __init__(self):
        super().__init__()
    
    def change_box(self, e):
        for check in self.controls[0].content.controls[:]:
            check.controls[1].content.value=False
            check.controls[1].content.update()

            e.control.value=True
            e.control.update()
        pass
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

    def app_size_main_builder(self, size:str):
        return Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=4,
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

    def build(self):
        return Container(
            height=50,
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

class AppButton(UserControl):
    def __init__(self, function):
        self.function = function
        super().__init__()
    
    def build(self):
        return Container(
            alignment=alignment.center,
            content=ElevatedButton(
                on_click=self.function,
                bgcolor="red",
                color="white",
                height=45,
                content=Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text("Generate new image", size=15, weight="bold"),
                    ]
                ),
                style=ButtonStyle(
                    shape={"": RoundedRectangleBorder(radius=6)},
                ),
            ),
        )

class Filters(UserControl):
    def __init__(self):
        super().__init__()
    
    def filters_title(self):
        return Container(
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("Segmentation Filters", size=18, weight="bold"),
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
                    Button("Upload Image", 260, 
                           lambda __: self.btn_callback_files.pick_files(allow_multiple=False),
                           ),
                    #self.btn_callback_files,
                    #self.btn_callback_folder,
                    Button("Save New Image", 260,
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

        #controls_dict["files"] = self.container

        return self.container
    
    def generate_image(self, e):
        print("generate image")

    def card(self):
        return Container(
            height=420,
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

                            Text("Output destination", size=12, weight="bold"),
                            AppForm('./Downloads/', None),
                            Text("Increment/decrement light", size=12, weight="bold"),
                            AppCounter(),
                            Text("Image without segmented edge ?", size=12, weight="bold"),
                            AppSizeMenu(),
                            Text("Image with only the tumor ?", size=12, weight="bold"),
                            AppSizeMenu(),
                            Divider(height=2, color="transparent"),
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
                            scroll="auto",
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                #TODO where the image will be displayed 
                                #Image("/Users/lucian/Documents/GitHub/BrainCancerDetection/gui/data/1.jpg"),
                            ],
                        )
                    ),                
                ]
            )
        )
    
    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.filters_title(),
                #Divider(height=20, color="transparent"),
                self.step_one(),
                Text("Input file", size=14, weight="bold"),
                self.step_two(),
                Text("Select Options", size=14, weight="bold"),
                self.card(),
            ]
        )