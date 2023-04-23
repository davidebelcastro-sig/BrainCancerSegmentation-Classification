import flet as ft
from flet import *

#NOTE: import the pages implemented in the gui folder
import segmentation as seg
import filters as fil
import view as vi 

def main(page: ft.Page):
    #NOTE: this is the main page configuration
    page.title = "Brain Cancer Detection"
    page.window_width = 900
    page.window_height = 850
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_resizable = False
    page.padding = 25
    page.bgcolor = colors.BLACK
    #NOTE: all the following code is for the Navigation Bar implementation
    def changetab(e):
        my_index = e.control.selected_index
        tab_1.visible = True if my_index == 0 else False
        tab_2.visible = True if my_index == 1 else False
        tab_3.visible = True if my_index == 2 else False
        page.update()
    page.navigation_bar = ft.NavigationBar(
        bgcolor = colors.BLACK,
        selected_index=0,
        on_change=changetab,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.ADD_A_PHOTO, label="Segmentation"),
            ft.NavigationDestination(icon=ft.icons.ZOOM_IN, label="3D View"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS,label="Filters"),
        ]
    )
    tab_1 = seg.Segmentation()
    tab_2 = vi.View()
    tab_3 = fil.Filters()
    page.add(Container(content=Column([tab_1,tab_2,tab_3,])),)
#NOTE: this is the main entry point for the application
if __name__ == "__main__":
    ft.app(target=main)