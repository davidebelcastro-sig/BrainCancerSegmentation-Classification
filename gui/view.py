import flet 
from flet import *

class View(UserControl):
    def __init__(self):
        super().__init__()
    
    def view_title(self):
        return Container(
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("3D View", size=18, weight="bold"),
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
    
    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.view_title(),
            ]
        )