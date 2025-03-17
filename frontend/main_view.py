from googleapiclient.discovery import build
import flet as ft
import pandas as pd

def obtener_info_video_app(api_key, max_results=5):    
    # Crear cliente
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request para obtener videos populares
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        chart="mostPopular",
        
        maxResults=max_results,
        regionCode="US",  # Puedes cambiar la región si lo deseas
        videoCategoryId="10" # Music
    )
    response = request.execute()

    # Verificamos que haya datos
    if not response['items']:
        print("No se encontraron videos populares")
        return []

    videos_info = []

    for video in response['items']:
        datos_app = {
            "title": video['snippet'].get('title', ''),
            "thumbnail": video['snippet']['thumbnails']['high']['url'],
            "channel_title": video['snippet'].get('channelTitle', ''),
            "published_at": video['snippet'].get('publishedAt', ''),
            "duration": video['contentDetails'].get('duration', 'PT0M0S'),
            "view_count": int(video['statistics'].get('viewCount', 0)),
            "like_count": int(video['statistics'].get('likeCount', 0)),
        }
        videos_info.append(datos_app)
    
    return videos_info

api_key = "AIzaSyDhUFUrs5MbqkG_6RaRIWhIFWcyOEK8qhE"

res = obtener_info_video_app(api_key, max_results=10)
    
df = pd.DataFrame(res)

print(df)

# User Interface responsive
class UI:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def songs_list(self):
        
        self.songs_list = ft.GridView(
            expand=True,child_aspect_ratio=1.65,
            horizontal=True,
        )
        
        for index, row in df.iterrows():
            song_card = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=9,
                        border_radius=12,
                        image_fit=ft.ImageFit.FILL,
                        image_src=row['thumbnail'],
                    ),
                    ft.Text(row['title'], weight=ft.FontWeight.BOLD),
                    #ft.Text(row['channel_title']),
                    #ft.Text(row['published_at']),
                    #ft.Text(f"Views: {row['view_count']}"),
                    #ft.Text(f"Likes: {row['like_count']}"),
                ]
            )
            self.songs_list.controls.append(song_card)
        
        return self.songs_list
           
    def build_fab(self):
        return ft.FloatingActionButton(
            icon=ft.icons.SEARCH,
            bgcolor=ft.colors.BLUE_GREY_700,
            shape=ft.RoundedRectangleBorder(radius=25),
            tooltip="Buscar",
            on_click=lambda e: self.on_search_click(),
        )

    def build_ui(self):
        return ft.Stack(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Quick a song",
                            size=14
                        )
                    ]
                ),
                self.songs_list(),
                ft.Container(
                    content=self.build_fab(),
                    alignment=ft.alignment.bottom_right,
                    margin=ft.margin.only(right=20, bottom=20),
                ),
            ],
        )

    def on_search_click(self):
        print("Search clicked!")

# Sidebar responsive
class Sidebar:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_index = 1 

    def build_nav_rail(self):
        return ft.NavigationRail(
            selected_index=self.selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=130,
            expand=True,
            bgcolor="transparent",
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME,
                    label="Home",
                    padding=ft.padding.only(top=20, bottom=10),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.LIBRARY_MUSIC_OUTLINED,
                    selected_icon=ft.icons.LIBRARY_MUSIC,
                    label="Library",
                    padding=ft.padding.only(top=10, bottom=10),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.HISTORY_OUTLINED,
                    selected_icon=ft.icons.HISTORY,
                    label="Historial",
                    padding=ft.padding.only(top=10, bottom=20),
                ),
            ],
            on_change=self.on_nav_change,
        )
        
    def build_settings_nav_rail(self):
        return ft.NavigationRail(
            label_type=ft.NavigationRailLabelType.ALL,
            bgcolor="transparent",
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS,
                    selected_icon=ft.icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=lambda e: self.on_settings_click(),
        )
            
    def build_sidebar(self):
        main_nav_rail = self.build_nav_rail()
        settings_nav_rail = self.build_settings_nav_rail()

        return ft.Container(
            width=130,
            height=self.page.height,
            margin=ft.margin.only(top=-10, bottom=-8, left=-15),
            #border=ft.border.all(0.5, "white70"),
            padding=ft.padding.only(top=35, left=20, right=20),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            gradient=ft.RadialGradient(
                center=ft.Alignment(-0.5, -0.8),
                radius=3,
                colors=[
                    "#33354a", "#2f3143", "#2f3143", "#292b3c",
                    "#222331", "#222331", "#1a1a25", "#1a1b26",
                    "#1a1b26", "#21222f", "#1d1e2a",
                ],
            ),
            alignment=ft.alignment.top_left,
            content=ft.Column(
                controls=[
                    main_nav_rail, 
                    ft.Container(expand=True), 
                    ft.Container(
                        content=settings_nav_rail,              
                        height=100,
                    )  
                ],
                expand=True,
            ),
        )   

    def on_nav_change(self, e):
        self.selected_index = e.control.selected_index
        print(f"Selected index: {self.selected_index}")
        self.page.update()

    def on_settings_click(self):
        # Temporal... luego se añade la vista de settings
        print("Settings clicked!")

def main(page: ft.Page):
    def on_resize(e):
        sidebar.height = page.height
        fab_container = ui.controls[0] 
        if page.width < 300:
            fab_container.margin = ft.margin.only(right=10, bottom=10)
        else:
            fab_container.margin = ft.margin.only(right=20, bottom=20)
        page.update()

    page.title = "Jif Tube"
    page.bgcolor = "#1a1b26"
    page.window_resizable = True

    sidebar_instance = Sidebar(page)
    sidebar = sidebar_instance.build_sidebar()
    ui_instance = UI(page)
    ui = ui_instance.build_ui()
    
    page.add(
        ft.Row(
            controls=[
                sidebar,
                ft.Container(
                    content=ui,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

    on_resize(None)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)