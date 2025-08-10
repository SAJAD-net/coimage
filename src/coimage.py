import io
import flet as ft
from PIL import Image


def main(page: ft.Page):
    page.title = "CoImage (Image Resizer, Compressor and Rotator)"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 600
    page.window_height = 550
    page.window_resizable = False

    # Function to toggle theme
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
    def process_image(img_path, width, height, quality, rotation_angle):
        try:
            update_status("Processing image...", 0.5)

            img = Image.open(img_path)

            # Rotate image if angle is specified
            if rotation_angle != 0:
                img = img.rotate(rotation_angle, expand=True)

            # Resize image
            new_size = (int(width), int(height))
            resized_img = img.resize(new_size, Image.LANCZOS)

            # Compress image
            byte_arr = io.BytesIO()
            resized_img.save(byte_arr, format='JPEG', quality=int(quality))
            byte_arr = byte_arr.getvalue()

            # Save the processed image to a variable
            page.processed_image = byte_arr

            update_status("Image processed successfully!", 1.0)
        except Exception as error:
            update_status(f"Error: {str(error)}", 0.0)

    # Function to handle file picker for opening images
    global image_path
    def open_image(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            img_path = selected_file.path
            global image_path
            image_path = img_path
            page.image_path = img_path

            # Open the image and get its dimensions
            img = Image.open(img_path)
            width, height = img.size

            # Fill the input fields with the image's dimensions and default values
            width_input.value = str(width)
            height_input.value = str(height)
            quality_input.value = "85"
            rotation_slider.value = 0  # Reset rotation angle
            rotation_display.value = "0°"  # Reset rotation display

            update_status("Image loaded successfully.")
            page.update()

    # Function to handle saving the image
    def save_image(e):
        if hasattr(page, "processed_image"):
            save_path = f"{image_path}(Compressed).jpg"
            with open(save_path, "wb") as file:
                file.write(page.processed_image)
            update_status(f"Image saved as {save_path}")

    # Function to handle resizing, compressing and rotating
    def resize_compress_rotate(e):
        if hasattr(page, "image_path"):
            process_image(
                page.image_path,
                width_input.value,
                height_input.value,
                quality_input.value,
                rotation_slider.value
            )

    # Function to update rotation display
    def update_rotation_display(e):
        rotation_display.value = f"{int(rotation_slider.value)}°"
        page.update()

    # File picker
    file_picker = ft.FilePicker(on_result=open_image)
    page.overlay.append(file_picker)

    # Input fields
    width_input = ft.TextField(label="Width", value="", width=150, expand=True)
    height_input = ft.TextField(label="Height", value="", width=150, expand=True)
    quality_input = ft.TextField(label="Quality (1-100)", value="", width=150, expand=True)

    # Rotation controls
    rotation_slider = ft.Slider(
        min=0,
        max=360,
        divisions=8,
        label="{value}°",
        width=300,
        on_change=update_rotation_display
    )
    rotation_display = ft.Text("0°", size=16)

    # Quick rotation buttons
    rotate_left_button = ft.IconButton(
        icon=ft.icons.ROTATE_LEFT,
        on_click=lambda e: set_rotation(-90),
        tooltip="Rotate Left 90°"
    )
    rotate_right_button = ft.IconButton(
        icon=ft.icons.ROTATE_RIGHT,
        on_click=lambda e: set_rotation(90),
        tooltip="Rotate Right 90°"
    )

    def set_rotation(angle_change):
        new_angle = (rotation_slider.value + angle_change) % 360
        rotation_slider.value = new_angle
        rotation_display.value = f"{int(new_angle)}°"
        page.update()

    # Theme toggle icon
    theme_icon = ft.IconButton(
        icon=ft.icons.DARK_MODE,
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
    process_button = ft.ElevatedButton("Process Image", on_click=resize_compress_rotate)

    # Layout
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("CoImage (Image Resizer, Compressor and Rotator)", size=24, weight=ft.FontWeight.BOLD),
                        theme_icon,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
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
                        process_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Divider(),
                # Rotation controls
                ft.Column(
                    [
                        ft.Text("Image Rotation", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                rotate_left_button,
                                rotation_slider,
                                rotate_right_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        ft.Text("Current Rotation:", size=14),
                        rotation_display,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(),
                # Progress bar and status
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
