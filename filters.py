import flet 
from flet import *
from segmentation import Button
import filter
import cv2
from datetime import datetime

controls_dict = {}
data = []
image=[]
class AppCounter(UserControl):
    def __init__(self):
        super().__init__()
    
    def app_counter_add(self, e):
        count = int(self.app_counter_text.value) + 10
        self.app_counter_text.value = str(count)
        self.app_counter_text.update()

    def app_counter_sub(self, e):
        count = int(self.app_counter_text.value) - 10
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
                    self.app_size_main_builder("Pass"),
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
        self.btn_callback_files = FilePicker(on_result=self.segmentation_files)
        self.btn_callback_folder = FilePicker(on_result=None)
        self.session = []
        super().__init__()
    
    def filters_title(self):
        return Container(
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("Segmentation Filters", size=18, weight="bold"),
                    IconButton(
                        content=Text("x",
                            weight="bold",
                            size=18,
                        ),
                        on_click=lambda __: self.page.window_close(),
                    )
                ]
            )
        )
    def return_file_list(self, file_icon, file_name, file_path):
        return Column(
            spacing=1,
            controls=[
                Row(controls=[Icon(file_icon, size=12),Text(file_name, size=13),]),
                Row(controls=[Text(file_path, size=9,no_wrap=False, color="white54"),])
            ]
        )
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
                           lambda __: self.btn_callback_files.pick_files(allow_multiple=False),"black"
                           ),
                    self.btn_callback_files,
                    #self.btn_callback_folder,
                    Button("Save New Image", 260,
                           lambda __: self.btn_callback_folder.get_directory_path(),"black"
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
    def convert(self, array):
        dir = '/Users/lucian/Documents/GitHub/BrainCancerDetection/tmp/filters'
        now = datetime.now()
        file_name = now.strftime("%H:%M:%S")
        t = f"{file_name}.png"
        path = dir + "/" + t
        cv2.imwrite(path, array)
        return path
    def generate_image(self, e):
        stuff = data[-1]
        data_list = []
        c = []
        for d in stuff:
            if not isinstance(d, Text):
                if not isinstance(d, Divider):
                    if not isinstance(d, AppButton):
                        data_list.append(d.controls[0].content)
        
        for p in data_list:
            for item in p.controls[:]:
                if isinstance(item, Text):
                    c.append(item.value)
                if isinstance(item, Column):
                    for checks in item.controls[:]:
                        if isinstance(checks, Container):
                            if checks.content.value == True:
                                ans = str(item.controls[0].value)
                                c.append(ans)

        result = filter.main(c, self.session[-1])
        path = self.convert(result)
        
        image[-1].controls.append(
            Container(
                width=400,
                height=400,
                image_src=path,
                image_fit='cover',
                border_radius=8,
        )
        )
        image[-1].update()


    def card(self):
        self.container = Container(
            height=450,
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
                            Text("Increment/decrement light", size=12, weight="bold"),
                            AppCounter(),
                            Text("Image with colored segmentation ?", size=12, weight="bold"),
                            AppSizeMenu(),
                            Text("Image with only the tumor ?", size=12, weight="bold"),
                            AppSizeMenu(),
                            Text("Image without segmentation ?", size=12, weight="bold"),
                            AppSizeMenu(),
                            Divider(height=15, color="transparent"),
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
                            scroll = 'auto',
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[]
                        )
                    ),                
                ]
            )
        )
        instance = self.container.content.controls[0].content.controls[:]
        p=self.container.content.controls[2].content
        data.append(instance)
        image.append(p)
        return self.container
    
    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                self.filters_title(),
                self.step_one(),
                Text("Input file", size=16, weight="bold"),
                self.step_two(),
                Text("Select Options", size=16, weight="bold"),
                self.card(),
            ]
        )