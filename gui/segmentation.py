import flet 
from flet import *

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
    pass

class Segmentation(UserControl):
    def __init__(self):
        super().__init__()

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
                    Button("Upload File(s)", 260, None),
                    Button("Upload Folder", 260, None),
                ]
            )
        )
    #! Main entry point for the Segmentation page
    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.segmentation_title(),
                self.step_one(),
            ]
        )