import io
import flet as ft
from PIL import Image


def main(page: ft.Page):
    page.title = "Image Resizer and Compressor"
    page.theme_mode = ft.ThemeMode.DARK  # Default theme
    page.padding = 20
    page.window_width = 600  # Fixed window width
    page.window_height = 500  # Increased window height to accommodate progress bar and status
    page.window_resizable = False  # Disable window resizing

    # Function to toggle theme, chnaging the theme between light mode and dark mode.
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon.name = ft.icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon.name = ft.icons.DARK_MODE
        page.update()

    # Function to update status and progress bar
    def update_status(message, progress=None):
        status_text.value = message
        if progress is not None:
            progress_bar.value = progress
        page.update()

    # Function to handle image processing
    def process_image(img_path, width, height, quality):
        try:
            update_status("Processing image...", 0.5)  # Show progress

            img = Image.open(img_path)

            # Resize image
            new_size = (int(width), int(height))
            resized_img = img.resize(new_size, Image.ANTIALIAS)

            # Compress image
            byte_arr = io.BytesIO()
            resized_img.save(byte_arr, format='JPEG', quality=int(quality))
            byte_arr = byte_arr.getvalue()

            # Save the processed image to a variable
            page.processed_image = byte_arr

            update_status("Image processed successfully!", 1.0)  # Complete progress
        except Exception as error:
            update_status(f"Error: {str(error)}", 0.0)  # Reset progress on error


    # Function to handle file picker for opening images
    global image_path
    def open_image(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            img_path = selected_file.path
            global image_path
            image_path = img_path
            page.image_path = img_path  # Save the image path for later use

            # Open the image and get its dimensions
            img = Image.open(img_path)
            width, height = img.size

            # Fill the input fields with the image's dimensions and default quality
            width_input.value = str(width)
            height_input.value = str(height)
            quality_input.value = "85"  # Default quality

            update_status("Image loaded successfully.")  # Update status
            page.update()

    # Function to handle saving the image
    def save_image(e):
        if hasattr(page, "processed_image"):
            save_path = f"{image_path}(Compressed).jpg"
            with open(save_path, "wb") as file:
                file.write(page.processed_image)
            update_status(f"Image saved as {save_path}")  # Update status

    # Function to handle resizing and compressing
    def resize_and_compress(e):
        if hasattr(page, "image_path"):
            process_image(page.image_path, width_input.value, height_input.value, quality_input.value)

    # File picker
    file_picker = ft.FilePicker(on_result=open_image)
    page.overlay.append(file_picker)

    # Input fields
    width_input = ft.TextField(label="Width", value="", width=150, expand=True)
    height_input = ft.TextField(label="Height", value="", width=150, expand=True)
    quality_input = ft.TextField(label="Quality (1-100)", value="", width=150, expand=True)

    # Theme toggle icon
    theme_icon = ft.IconButton(
        icon=ft.icons.DARK_MODE,  # Default icon for light theme
        on_click=toggle_theme,
        tooltip="Toggle Theme",
    )

    # Progress bar
    progress_bar = ft.ProgressBar(value=0, width=400)

    # Status text
    status_text = ft.Text("Ready", size=16, color=ft.colors.GREY_600)

    # Buttons
    open_button = ft.ElevatedButton("Open Image", on_click=lambda _: file_picker.pick_files())
    save_button = ft.ElevatedButton("Save Image", on_click=save_image)
    resize_button = ft.ElevatedButton("Resize and Compress", on_click=resize_and_compress)

    # Layout
    page.add(
        ft.Column(
            [
                # Title in top center
                ft.Row(
                    [
                        ft.Text("Image Resizer and Compressor", size=24, weight=ft.FontWeight.BOLD, expand=False),
                        theme_icon,  # Theme toggle icon in the top-right corner
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
                # Input fields and buttons
                ft.Row(
                    [
                        ft.Column(
                            [
                                width_input,
                                height_input,
                                quality_input,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        open_button,
                        save_button,
                        resize_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Divider(),
                # Progress bar and status in bottom center
                ft.Column(
                    [
                        progress_bar,
                        status_text,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=20,
            expand=False,
        )
    )

ft.app(target=main)
