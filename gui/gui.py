import flet as ft
from flet import *

import segmentation as seg

def main(page: ft.Page):
    #* Window settings
    page.title = "Brain Cancer Detection"
    page.window_width = 900
    page.window_height = 820
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.padding = 25
    #NOTE: all the following code is for the Navigation Bar implementation
    def changetab(e):
        my_index = e.control.selected_index
        tab_1.visible = True if my_index == 0 else False
        tab_2.visible = True if my_index == 1 else False
        tab_3.visible = True if my_index == 2 else False
        page.update()
    
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=changetab,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.ADD_A_PHOTO, label="Segmentation"),
            ft.NavigationDestination(icon=ft.icons.ZOOM_IN, label="3D View"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS,label="Settings"),
        ]
    )

    tab_1 = seg.Segmentation()
    tab_2 = Text("Tab 2",size=30,visible=False)
    tab_3 = Text("Tab 3",size=30,visible=False)

    page.add(
        Container(
        content=Column([
            tab_1,
            tab_2,
            tab_3
        ])
    )
    )

#NOTE: this is the main entry point for the application
if __name__ == "__main__":
    ft.app(target=main)