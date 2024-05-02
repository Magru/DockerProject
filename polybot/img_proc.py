from pathlib import Path
from matplotlib.image import imread, imsave
import random
from loguru import logger


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self, direction='clockwise'):
        """
        Rotate the image in the specified direction.

        :param direction: 'clockwise' or 'counterclockwise'
        """

        # Transpose the image for both directions
        self._transpose()

        if direction == 'clockwise':
            # For clockwise rotation, reverse the rows after transposing
            self._reverse_rows()
        elif direction == 'counterclockwise':
            # For counterclockwise rotation, reverse the columns (the whole image here) after transposing
            self._reverse_columns()

    def salt_n_pepper(self):
        """
        Add salt and pepper noise to the image based on the specified algorithm. (see comments below)
        """
        height = len(self.data)
        width = len(self.data[0])

        for i in range(height):
            for j in range(width):
                rand = random.random()
                if rand < 0.2:
                    self.data[i][j] = 255  # Set to maximum intensity for 'salt'
                elif rand > 0.8:
                    self.data[i][j] = 0  # Set to minimum intensity for 'pepper'
                # If the random number is between 0.2 and 0.8, do nothing (keep the original pixel value)

    def concat(self, other_img, direction='horizontal'):
        """
        Concatenate self with another Img instance either horizontally or vertically.

        :param other_img: Another instance of Img to concatenate with.
        :param direction: The direction of concatenation ('horizontal' or 'vertical').
        :raises RuntimeError: If the dimensions of the images are not compatible.
        """
        if direction == 'horizontal':
            if len(self.data) != len(other_img.data):
                raise RuntimeError("Images have different heights, so they cannot be concatenated horizontally.")
            concatenated_data = [row_self + row_other for row_self, row_other in zip(self.data, other_img.data)]

        elif direction == 'vertical':
            # Check if widths of the two images are equal
            if any(len(row_self) != len(row_other) for row_self, row_other in zip(self.data, other_img.data)):
                raise RuntimeError("Images have different widths, so they cannot be concatenated vertically.")
            # Concatenate the whole of other_img.data to self.data
            concatenated_data = self.data + other_img.data

        else:
            raise ValueError("Unsupported direction for concatenation. Please choose 'horizontal' or 'vertical'.")

        # Store the concatenated image data
        self.data = concatenated_data

    def segment(self):
        """
        Segment the image by setting pixel values to white (255) if their intensity is greater than 100,
        or to black (0) otherwise.
        """
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = 255 if self.data[i][j] > 100 else 0

    def handle_filter(self, filter_name, **kwargs):
        """
        Dynamically executes a filter method based on its name.

        Args:
        - filter_name (str): The name of the filter method to run.
        - **kwargs: Optional keyword arguments to pass to the filter method.

        Returns:
        - The result of the filter method, if any.

        Raises:
        - AttributeError: If the specified filter method does not exist.
        """
        # Dynamically fetch the method by name
        method = getattr(self, filter_name, None)

        if not method:
            raise AttributeError(f"Filter method '{filter_name}' not found.")

        # Call the method if it exists, passing any additional keyword arguments
        return method(**kwargs)

    def clear(self):
        self._remove_filtered_image()
        self._remove_original_image()

    def _transpose(self):
        """
        Transpose the image (swap rows with columns).
        """
        self.data = list(map(list, zip(*self.data)))

    def _reverse_rows(self):
        """
        Reverse each row in the image.
        """
        self.data = [row[::-1] for row in self.data]

    def _reverse_columns(self):
        """
        Reverse each column in the image.
        This can be done by reversing the entire image.
        """
        self.data.reverse()

    def _remove_original_image(self):
        """
        Removes the original image file.
        """
        if self.path.exists():
            self.path.unlink()
            print(f"Removed original image: {self.path}")
        else:
            print(f"Original image file does not exist: {self.path}")

    def _remove_filtered_image(self):
        """
        Removes the filtered image file.
        """
        filtered_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        if filtered_path.exists():
            filtered_path.unlink()
            print(f"Removed filtered image: {filtered_path}")
        else:
            print(f"Filtered image file does not exist: {filtered_path}")
