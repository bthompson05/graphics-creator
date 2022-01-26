import os
from PIL import Image
import cv2


class CropSquareImages:

    def __init__(self, file):
        # sets file for access throughout class
        self.file = file
        # The coordinates defining the square selected will be kept in this list.
        self.select_coords = []
        # While we are in the process of selecting a region, this flag is True.
        self.selecting = False
        self.image = cv2.imread(file)

    def make_thumbnail_for_preview(self):

        # opening image to resize to scale with cv2
        image = Image.open(str(self.file))
        width, height = image.size
        # sets the largest length to the variable largest
        if width > height:
            largest = width
        else:
            largest = width
        # work out the scale of the largest side from 900 to original size
        self.scale = largest / 900
        # rescales to fit smaller canvas
        display_size = (round(width / self.scale), round(height / self.scale))
        # scales to fit smaller canvas and exports image for later use
        new_img = image.resize(display_size)
        new_img.save("scaled_down.png")



    def get_square_coords(self, x, y, cx, cy):
        """
        Get the diagonally-opposite coordinates of the square.
        (cx, cy) are the coordinates of the square centre.
        (x, y) is a selected point to which the largest square is to be matched.

        """

        # Selected square edge half-length; don't stray outside the image boundary.
        a = max(abs(cx-x), abs(cy-y))
        a = min(a, self.w-cx, cx, self.h-cy, cy)
        return cx-a, cy-a, cx+a, cy+a


    def region_selection(self, event, x, y, flags, param):
        """Callback function to handle mouse events related to region selection."""

        if event == cv2.EVENT_LBUTTONDOWN:
            # Left mouse button down: begin the selection.
            # The first coordinate pair is the centre of the square.
            self.select_coords = [(x, y)]
            self.selecting = True

        elif event == cv2.EVENT_MOUSEMOVE and self.selecting:
            # If we're dragging the selection square, update it.
            self.image = self.clone.copy()
            x0, y0, x1, y1 = self.get_square_coords(x, y, *self.select_coords[0])
            cv2.rectangle(self.image, (x0, y0), (x1, y1), (0, 255, 0), 2)

        elif event == cv2.EVENT_LBUTTONUP:
            # Left mouse button up: the selection has been made.
            self.select_coords.append((x, y))
            self.selecting = False

    def main_func(self):

        self.make_thumbnail_for_preview()
        # Load the image and get its filename without path and dimensions.
        filename = str("scaled_down.png")
        basename = os.path.basename(filename)
        self.image = cv2.imread(filename)
        self.h, self.w = self.image.shape[:2]
        # Store a clone of the original image (without selected region annotation).
        self.clone = self.image.copy()
        # Name the main image window after the image filename.
        cv2.namedWindow(basename)
        cv2.setMouseCallback(basename, self.region_selection)

        # Keep looping and listening for user input until 'c' is pressed.
        while True:
            # Display the image and wait for a keypress
            cv2.imshow(basename, self.image)
            key = cv2.waitKey(1) & 0xFF
            # If 's' is pressed, break from the loop and handle any region selection.
            if key == ord("s"):
                break

        # Did we make a selection?
        if len(self.select_coords) == 2:
            cx, cy = self.select_coords[0]
            x, y = self.select_coords[1]
            x0, y0, x1, y1 = self.get_square_coords(x, y, cx, cy)
            # Crop the image to the selected region and display in a new window.
            cropped_image = self.clone[y0:y1, x0:x1]

        # sets the cropped coords back to full scale
        coors = (round(x0 * self.scale), round(y0 * self.scale), round(x1 * self.scale), round(y1 * self.scale))
        # loads in image, crops to fit the square bounds and saves to a new file
        image = Image.open(self.file)
        im_crop = image.crop((coors))

        # closes all windows
        cv2.destroyAllWindows()
        os.remove("scaled_down.png")
        return im_crop
