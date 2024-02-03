import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRect, QPoint

class Ui_Image_Check(object):
    def setupUi(self, Image_Check):
        if Image_Check.objectName():
            Image_Check.setObjectName(u"Image_Check")
        Image_Check.resize(700, 680)

        # Initialize square_position attribute
        self.square_position = QPoint(390,360)

        # Image label
        self.imageLabel = QLabel(Image_Check)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setGeometry(QRect(0, 0, 488, 680))  # Set the size to the window size
        pixmap = QPixmap("card_images/(0ae3920d-0360-48f8-8172-6bb6666ba22c)_7ee52536-8cfa-482b-874e-094c0a081894.jpg")  # Replace with your image path
        self.imageLabel.setPixmap(pixmap)

        # Frame label
        self.movinWindow = QLabel(Image_Check)
        self.movinWindow.setObjectName(u"movinWindow")
        self.movinWindow.setGeometry(QRect(390,360, 75, 75))
        self.movinWindow.setStyleSheet("background-color: transparent; border: 2px solid white;")  # Set background to transparent
        self.movinWindow.setFrameShape(QFrame.Box)
        self.movinWindow.setLineWidth(5)
        self.movinWindow.setMidLineWidth(0)

        # Connect mouse events to handle square movement
        self.movinWindow.mousePressEvent = self.square_mouse_press
        self.movinWindow.mouseMoveEvent = self.square_mouse_move
        self.movinWindow.mouseReleaseEvent = self.square_mouse_release

        # Label for displaying the cropped part of the image
        self.croppedImageLabel = QLabel(Image_Check)
        self.croppedImageLabel.setObjectName(u"croppedImageLabel")
        self.croppedImageLabel.setGeometry(QRect(500, 300, 75, 75))  # Adjust position and size as needed

        # Buttons
        self.saveButton = QPushButton("Save Cropped Image", Image_Check)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setGeometry(QRect(500, 500, 150, 30))
        self.saveButton.clicked.connect(self.save_cropped_image)

        self.changeImageButton = QPushButton("Change Full Image", Image_Check)
        self.changeImageButton.setObjectName(u"changeImageButton")
        self.changeImageButton.setGeometry(QRect(500, 600, 150, 30))
        self.changeImageButton.clicked.connect(self.change_full_image)

        # Other UI elements
        self.cropPreview = QLabel(Image_Check)  # Added preview label
        self.cropPreview.setObjectName(u"cropPreview")
        self.cropPreview.setGeometry(QRect(10, 20, 100, 50))
        self.cropPreview.setAlignment(Qt.AlignCenter)

        # Set initial index for the images
        self.current_image_index = 0

        self.retranslateUi(Image_Check)

        # Set your folder paths here
        self.full_image_folder = "card_images/"
        self.cropped_image_folder = "set_symbols/"

        # Initialize the save path for the cropped image
        self.cropped_image_name = "(0ae3920d-0360-48f8-8172-6bb6666ba22c)_7ee52536-8cfa-482b-874e-094c0a081894.jpg"

    # Add the following functions for handling mouse events

    def square_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def square_mouse_move(self, event):
        if hasattr(self, 'offset'):
            new_position = event.pos() - self.offset
            self.square_position = self.movinWindow.pos() + new_position
            self.movinWindow.move(self.square_position)

            # Update the preview label based on the square position
            self.update_preview_label()

            # Update the cropped image label
            self.update_cropped_image_label()

    def square_mouse_release(self, event):
        if hasattr(self, 'offset'):
            del self.offset

    def update_preview_label(self):
        # Use self.square_position to update the content of the preview label
        self.square_position
        # self.cropPreview.setText('')

    def update_cropped_image_label(self):
        # Get the rectangle corresponding to the movable window
        movable_window_rect = QRect(self.square_position.x(), self.square_position.y(), self.movinWindow.width(), self.movinWindow.height())

        # Get the pixmap of the original image
        original_pixmap = self.imageLabel.pixmap()

        # Crop the original pixmap based on the movable window rectangle
        cropped_pixmap = original_pixmap.copy(movable_window_rect)

        # Set the cropped pixmap to the croppedImageLabel
        self.croppedImageLabel.setPixmap(cropped_pixmap)

    def save_cropped_image(self):
        # Get the rectangle corresponding to the movable window
        movable_window_rect = QRect(self.square_position.x(), self.square_position.y(), self.movinWindow.width(), self.movinWindow.height())

        # Get the pixmap of the original image
        original_pixmap = self.imageLabel.pixmap()

        # Crop the original pixmap based on the movable window rectangle
        cropped_pixmap = original_pixmap.copy(movable_window_rect)

        # Construct the save path for the cropped image
        save_path = os.path.join(self.cropped_image_folder, os.path.basename(self.cropped_image_name))

        # Save the cropped image
        cropped_pixmap.save(save_path)

    def change_full_image(self):
        # List all files in the folder
        full_image_files = [f for f in os.listdir(self.full_image_folder) if os.path.isfile(os.path.join(self.full_image_folder, f))]

        if self.current_image_index < len(full_image_files):
            # Get the next image file
            next_image_file = full_image_files[self.current_image_index]

            # Construct the full path of the next image
            next_image_path = os.path.join(self.full_image_folder, next_image_file)

            # Set the new image to the imageLabel
            new_pixmap = QPixmap(next_image_path)
            self.imageLabel.setPixmap(new_pixmap)

            # Reset the movable window position
            self.movinWindow.move(390,360)

            # Update the cropped image label
            self.update_cropped_image_label()

            # Increment the current image index for the next time
            self.current_image_index += 1

            # Update the save path for the cropped image
            self.cropped_image_name = next_image_file
        else:
            print("No more images in the folder.")

    def retranslateUi(self, Image_Check):
        Image_Check.setWindowTitle("Image Check")
        # ... (You can add translations for other UI elements here)

# Main function to set up and run the application
def main():
    app = QApplication([])

    # Create the main window
    main_window = QMainWindow()
    ui = Ui_Image_Check()
    ui.setupUi(main_window)

    # Show the main window
    main_window.show()

    # Run the application
    sys.exit(app.exec_())

# Run the application if the script is executed
if __name__ == "__main__":
    main()
