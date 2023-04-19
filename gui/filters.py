import flet 
from flet import *

class AppForm(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return Container(
            height=45,
            bgcolor="#ebebeb",
            border_radius=6,
            padding=8,
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
    
    def card(self):
        return Container(
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
                        height=400,
                        content=Column(
                          controls=[
                            AppForm(),
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
                            ],
                        )
                    )
,                ]
            )
        )
    
    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.filters_title(),
                Divider(height=20, color="transparent"),
                Text("Input file", size=14, weight="bold"),
                self.card(),
            ]
        )