import shutil

import requests
import telebot
from loguru import logger
import os
import time

from telebot import types
from telebot.types import InputFile
from img_proc import Img


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def handle_text_message(self, command, chat_id):
        """
        Handles commands sent to the Telegram bot with the inclusion of chat ID.

        Args:
        - command (str): The command sent to the bot.
        - chat_id (int): The unique identifier for the chat.

        Returns:
        - str: The response message.
        """

        def start_command():
            return (
                f"👋 Welcome to Max-Python-Project bot! 🐍✨\n\n"
                f"Your chat ID is {chat_id}.\n\n"
                f"🚀 **Getting Started:** Please *upload an image* 🖼️ and *specify the desired action* in the "
                f"image's caption."
                f"Actions include: *Blur*, *Contour*, *Rotate*, *Salt_n_Pepper*, *Concat*, *Segment*, and *Predict "
                f"Objects*."
                f"Example: Upload an image with the caption 'Blur' to soften the image.\n\n"
                f"✨ **Bot Options:**\n"
                f"- *Blur* 🔍: Soften the image.\n"
                f"- *Contour* 📐: Highlight the edges in the image.\n"
                f"- *Rotate* 🔄: Rotate the image by a specified angle.\n"
                f"- *Salt_n_Pepper* 🧂: Add a salt and pepper noise effect.\n"
                f"- *Concat* 🧩: Combine multiple images together.\n"
                f"- *Segment* 🎨: Segment the image into different parts based on colors or features.\n"
                f"- *Predict* 🔭: Identify and label objects in the image.\n\n"
                f"For further assistance or to explore more features, type /help 💬."
            )

        def help_command():
            return (
                f"Looking for assistance? Here's how to use Max-Python-Project bot more effectively: 🐍✨\n\n"
                f"1. **Image Upload:** Begin by uploading an image 🖼️ you wish to manipulate. Make sure to attach the "
                f"image using the paperclip icon in Telegram.\n\n"
                f"2. **Define Action:** When uploading an image, please include the action you'd like to perform in the "
                f"image's caption."
                f"The available actions are: Blur (to soften the image), Contour (to highlight edges), Rotate (to "
                f"rotate"
                f"the image), Salt_n_Pepper (to add noise), Concat (to combine images), and Segment (to divide the "
                f"image"
                f"based on features or colors).\n\n"
                f"3. **Explore Bot Options:** The bot offers several image manipulation options:\n"
                f"- Blur 🔍: Applies a softening effect to your image.\n"
                f"- Contour 📐: Emphasizes the edges within your image.\n"
                f"- Rotate 🔄: Rotates your image by a given angle.\n"
                f"- Salt_n_Pepper 🧂: Adds a 'salt and pepper' type of noise to your image.\n"
                f"- Concat 🧩: Merges multiple images into one.\n"
                f"- Segment 🎨: Segregates your image into parts based on distinct features or colors.\n\n"
                f"If you need more information or assistance with a specific command, feel free to ask! 💬"
            )

        def action_not_valid_message():
            return (
                f"⚠️ The action you've specified is not valid. Please make sure to include a valid action in your "
                f"image's caption. \n\n"
                f"Here's a list of all valid actions you can request:\n"
                f"- *Blur* 🔍: Soften the image.\n"
                f"- *Contour* 📐: Highlight the edges in the image.\n"
                f"- *Rotate* 🔄: Rotate the image by a specified angle.\n"
                f"- *Salt_n_Pepper* 🧂: Add a 'salt and pepper' noise effect.\n"
                f"- *Concat* 🧩: Combine multiple images together.\n"
                f"- *Segment* 🎨: Segment the image into different parts based on colors or features.\n\n"
                f"Please upload your image again with the correct action in the caption. For more help, type /help 💬."
            )

        def caption_not_defined_message():
            return (
                "⚠️ It seems like you didn't specify an action in your image's caption. 🖼️\n\n"
                "Please upload your image again and include the desired action in the caption. "
                "Here are the actions you can specify:\n\n"
                "- *Blur* 🔍: To soften the image.\n"
                "- *Contour* 📐: To highlight the edges in the image.\n"
                "- *Rotate* 🔄: To rotate the image by a specified angle.\n"
                "- *Salt_n_Pepper* 🧂: To add a salt and pepper noise effect.\n"
                "- *Concat* 🧩: To combine multiple images together.\n"
                "- *Segment* 🎨: To segment the image into different parts based on colors or features.\n\n"
                "Make sure to include the action (e.g., 'Blur', 'Rotate') in the caption of your image upload. 📝"
            )

        def about_command():
            return (
                f"Max-Python-Project is a Telegram bot designed for image manipulation. "
                f"Developed with Python, it utilizes advanced algorithms to apply filters, "
                f"transform images, and provide various image editing features. "
                f"Your chat ID is {chat_id}."
            )

        def error_message():
            return (
                f"Some error... Sorry"
            )

        def default_command():
            return f"I'm not sure how to handle that command, {chat_id}. Try /help for more information."

        # Mapping commands to their corresponding functions
        switcher = {
            '/start': start_command,
            '/help': help_command,
            '/about': about_command,
            'error': error_message,
            'action_not_valid': action_not_valid_message,
            'caption_not_defined': caption_not_defined_message
        }

        # Get the function from switcher dictionary
        func = switcher.get(command, default_command)

        # Execute the function and return its response
        return func()

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        if self.is_current_msg_photo(msg):
            logger.info(msg['photo'])
            file_path = self.download_user_photo(msg)
        else:
            self.send_text(msg['chat']['id'], self.handle_text_message(msg['text'], msg['chat']['id']))


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


def _if_media_group_ready(media_group_id):
    photos_path = 'photos'
    media_files = []

    try:
        files = os.listdir(photos_path)

        if len(files) == 3 and any(media_group_id in file for file in files):
            for file in files:
                if file.endswith(('.jpg', '.png')):
                    media_files.append(os.path.join(photos_path, file))

            if len(media_files) == 2:
                return media_files
            else:
                return False
        else:
            return False
    except Exception as e:
        return f"Error: {e}"


def clear_photos_folder():
    photos_path = 'photos'

    try:
        if os.path.exists(photos_path):
            for filename in os.listdir(photos_path):
                file_path = os.path.join(photos_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            print("All files in 'photos' folder have been cleared.")
        else:
            print("'photos' folder does not exist.")
    except Exception as e:
        print(f"Error: {e}")


class ImageProcessingBot(Bot):
    def __init__(self, token, telegram_chat_url):
        super().__init__(token, telegram_chat_url)
        self.actions = ['blur', 'contour', 'rotate', 'salt_n_pepper', 'concat', 'segment', 'predict']

    def _validate_action(self, action):
        return action in self.actions

    def handle_message(self, msg):
        chat_id = msg['chat']['id']
        if 'text' in msg:
            self.send_text(chat_id, self.handle_text_message(msg['text'], chat_id))
            return

        caption = msg.get('caption')
        media_group_id = msg.get('media_group_id')

        if not caption:
            group = _if_media_group_ready(media_group_id)
            logger.info(_if_media_group_ready)
            if group:
                first_image = Img(group[0])
                second_image = Img(group[1])
                first_image.handle_filter('concat', other_img=second_image)
                filtered_image = first_image.save_img()
                self.send_photo(chat_id, filtered_image)
                clear_photos_folder()
                return

            self.send_text(chat_id, self.handle_text_message('caption_not_defined', chat_id))
        elif self._validate_action(caption.lower()):
            if caption.lower() == 'concat':
                media_group_file = open('photos/' + media_group_id, 'w')
                media_group_file.close()
            if caption.lower() == 'predict':
                single_file_path = self.download_user_photo(msg)
                logger.info('predict method ' + single_file_path)
            else:
                if self.is_current_msg_photo(msg):
                    try:
                        single_file_path = self.download_user_photo(msg)
                        img = Img(single_file_path)
                        img.handle_filter(caption.lower())
                        filtered_image_path = img.save_img()
                        self.send_photo(chat_id, filtered_image_path)
                        clear_photos_folder()
                    except Exception as err:
                        self.send_text(chat_id, self.handle_text_message('error', chat_id))
        else:
            self.send_text(chat_id, self.handle_text_message('action_not_valid', chat_id))
