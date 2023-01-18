import io
import os

import streamlit as st
from wantedposter.wantedposter import WantedPoster, VerticalAlignment, HorizontalAlignment

import constants as c


def main() -> None:
    """
    Main function
    :return: None
    """

    # BODY
    # Set web page layout
    st.set_page_config(page_title='Wanted Poster',
                       page_icon='./assets/favicon.ico', layout="centered")
    st.markdown(c.HIDE_ST_STYLE, unsafe_allow_html=True)

    st.subheader('One Piece Wanted Poster Generator')
    st.info('Open and resize the sidebar to view the generated poster')

    # Image import
    file_uploaded = st.file_uploader(
        'Select the image to use as portrait', type=['png', 'jpg', 'jpeg'])

    # First name
    first_name = st.text_input(
        'First Name', placeholder='Enter the first name')
    last_name = st.text_input(
        'Last Name', placeholder='Enter the last name')

    if (len(first_name) + len(last_name)) > c.FULL_NAME_MAX_LENGTH:
        st.warning(
            f"The first name and last name combined must be less than {c.FULL_NAME_MAX_LENGTH} characters."
            "If it is longer, the text will trimmed")

    # Bounty
    bounty_str = st.text_input(
        'Bounty', placeholder="Enter the bounty (Max. 999.999.999.999.999)")

    bounty = 0
    if bounty_str != '':
        try:
            belly = get_belly_from_string(bounty_str)
            if belly >= c.BOUNTY_MAX_VALUE or belly < 0:
                st.warning(f"The bounty must be between 0 and {get_belly_formatted(c.BOUNTY_MAX_VALUE)}")
            else:
                bounty = belly
        except ValueError:
            st.warning(f"The bounty must be a number, separated by commas or dots")

    # Other options
    with st.expander("More Options"):
        # Subsection alignment
        st.caption('Portrait alignment')

        col_horizontal_align, col_vertical_align = st.columns(2)
        with col_horizontal_align:
            horizontal_align = st.selectbox(
                'Horizontal alignment', options=('Center', 'Left', 'Right'))
        with col_vertical_align:
            vertical_align = st.selectbox(
                'Vertical alignment', options=('Center', 'Top', 'Bottom'))

        # Subsection filter

        # Set default transparency
        if file_uploaded is None:
            default_transparency = 0
        else:
            default_transparency = c.OPTIMAL_TRANSPARENCY

        st.info(f'Set the portrait transparency (optimal is {c.OPTIMAL_TRANSPARENCY})')
        transparency = st.slider('Transparency', min_value=0, max_value=255, value=default_transparency)

    # SIDE BAR
    with st.sidebar:
        # Set the image that will be printed on the poster
        if file_uploaded is not None:
            file_uploaded = io.BytesIO(file_uploaded.getvalue())

        # Generate the poster
        wanted_poster = WantedPoster(file_uploaded, first_name, last_name, bounty)
        transparency = 255 - transparency  # Invert the transparency
        vertical_align_enum = VerticalAlignment(vertical_align.upper())
        horizontal_align_enum = HorizontalAlignment(horizontal_align.upper())

        wanted_poster_path = wanted_poster.generate(portrait_vertical_align=vertical_align_enum,
                                                    portrait_horizontal_align=horizontal_align_enum,
                                                    should_make_portrait_transparent=True,
                                                    portrait_transparency_value=transparency)

        # Show poster preview
        st.image(wanted_poster_path)

        # Download poster
        with open(wanted_poster_path, "rb") as portrait:
            file_name = 'wanted_poster'
            if first_name != '':
                file_name = file_name + '_' + first_name
            if last_name != '':
                file_name = file_name + '_' + last_name
            file_name += '.jpg'
            st.download_button(label="Download image", data=portrait, file_name=file_name, mime="image/jpg")

        # Delete poster
        current_dir = os.getcwd()
        for file in os.listdir(current_dir):
            if file.endswith(".jpg"):
                os.remove(file)


def get_belly_from_string(amount_str: str) -> int:
    """
    Get the belly amount
    :param amount_str: The amount which can be separated by dots or commas
    :return: The amount without dots or commas
    """
    return int(amount_str.strip().replace(',', '').replace('.', ''))


def get_belly_formatted(belly: int) -> str:
    """
    Returns a formatted string of the belly
    :param belly: The belly to format e.g. 1000000
    :return: The formatted belly e.g. 1,000,000
    """

    return '{0:,}'.format(belly)


if __name__ == '__main__':
    main()
