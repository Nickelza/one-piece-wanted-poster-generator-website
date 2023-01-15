import streamlit as st
import io
import os
from wantedposter.wantedposter import WantedPoster


HIDE_ST_STYLE = """
	<style>
    #MainMenu {visibility: hidden;} 
	footer {visibility: hidden;} 
	header {visibility: hidden;} 
	.css-91z34k{padding: 1rem 1rem 1rem !important;}
	.css-76z9jo {display: none !important;}
	.css-fg4pbf {text-align: center;}
    .css-1vq4p4l {padding: 3rem 1rem 1rem;}
	</style>
	"""


class RunWantedPosterWebsite:
    def __init__(self) -> None:
        # Page initialization
        self.file_uploaded = None
        self.body()
        self.sidebar()


    def body(self):
        # Set web page layout
        st.set_page_config(page_title='One Piece wanted poster generator',
                           page_icon='./assets/favicon.ico', layout="centered")
        st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

        st.subheader('One Piece wanted poster generator')

        # Image import
        self.file_uploaded = st.file_uploader(
            'Choose the image to use to generate the poster', type=['png', 'jpg', 'jpeg', 'gif', 'svg'])

        # Username
        self.name = st.text_input(
            'Name', placeholder='Enter the name that will be used to create the poster')
        self.surname = st.text_input(
            'Surname', placeholder='Enter the surname that will be used to create the poster')

        if (len(self.name) + len(self.surname)) > 16:
            st.warning("WARNING: For reasons of space, the length of the name added to that of the surname must not be greater than 16. If you do not want the name displayed on the poster to be different from the one inserted, make sure that the length of the name added to that of the surname is less than 16.")

        # Bounty
        self.bounty = st.number_input(
            'Bounty', min_value=0, max_value=1000000000000000, step=1)

        # Other option
        with st.expander("Other option"):
            # Sub-section alignment
            st.caption('Image alignment')

            col_horizontal_align, col_vertical_align = st.columns(2)
            with col_horizontal_align:
                self.horizontal_align = st.selectbox(
                    'Horizontal align', options=('center', 'left', 'right'))
            with col_vertical_align:
                self.vertical_align = st.selectbox(
                    'Vertical align', options=('center', 'top', 'bottom'))

            # Sub-section filter
            st.caption('Image filter')

            st.info(
                'The higher the value of the slider, the more sensitive the image will be to the nuances of the paper.')
            self.transparency = st.slider(
                'Tranparency', min_value=0, max_value=255, value=55)


    def sidebar(self):
        with st.sidebar:
            # Set the image that will be printed on the poster
            if self.file_uploaded is not None:
                self.file_uploaded = io.BytesIO(self.file_uploaded.getvalue())

            # Generate the poster
            wanted_poster = WantedPoster(
                self.file_uploaded, self.name, self.surname, self.bounty)
            wanted_poster_path = wanted_poster.generate(
                None, self.vertical_align, self.horizontal_align, True, 255 - self.transparency)

            # Show poster preview
            st.image(wanted_poster_path)

            # Warning message
            if self.name == '' and self.surname == '':
                st.warning(
                    'Both the first and last name are empty are you sure you want to proceed anyway?')
            if self.bounty == 0:
                st.warning(
                    'The bounty is 0 are you sure you want to proceed anyway?')

            # Download poster
            with open(wanted_poster_path, "rb") as portrait:
                file_name = 'wanted_poster'
                if self.name != '':
                    file_name = file_name + '_' + self.name
                if self.surname != '':
                    file_name = file_name + '_' + self.surname
                file_name += '.png'
                st.download_button(
                    label="Download image", data=portrait, file_name=file_name, mime="image/png")

            # Delete poster from the site's memory
            current_dir = os.getcwd()
            for file in os.listdir(current_dir):
                if file.endswith(".jpg"):
                    os.remove(file)
