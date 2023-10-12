import flet as ft
from flet import colors, Column, Container
#NOTE: import the pages view implemented in the gui folder
from src.gui.segmentation import Segmentation
from src.gui.filters import Filters

def main(page: ft.Page):
    """Main function for the application, this is where the page is created."""
    page.title = "Brain Cancer Segmentation"
    page.window_width = 900
    page.window_height = 910
    page.padding = 25
    page.bgcolor = colors.BLACK
    
    def changetab(e):
        """Change the tab when the user clicks on the navigation bar."""
        my_index = e.control.selected_index
        tab_1.visible = True if my_index == 0 else False
        tab_2.visible = True if my_index == 1 else False
        page.update()

    page.navigation_bar = ft.NavigationBar(
        bgcolor = colors.BLACK,
        selected_index=0,
        on_change=changetab,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.ADD_A_PHOTO, label="Segmentation & Classification"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS,label="Segmentation Filters"),
        ]
    )

    seg = Segmentation()
    fil = Filters()
    tab_1 = seg
    tab_2 = fil
    page.add(Container(content=Column([tab_1,tab_2])))
    
if __name__ == "__main__":
    """Main entry point for the application, this is where the page is created and the main function is called."""
    ft.app(target=main)