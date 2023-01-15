# Custom style to edit the page
HIDE_ST_STYLE = '<style>'
# Hide Streamlit default header and footer
HIDE_ST_STYLE += """
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} 
    """
# Reduce overhead empty space in the main area
HIDE_ST_STYLE += """
    .css-91z34k{padding: 1rem 1rem 1rem !important;}
    """
# Remove overhead empty space in the sidebar
HIDE_ST_STYLE += """
    .css-1vq4p4l {padding: 3rem 1rem 1rem !important;}
    """
# Center download button in the sidebar
HIDE_ST_STYLE += """
    [data-testid=stSidebar] {text-align: center !important;}
    """
# End style
HIDE_ST_STYLE += '</style>'

DEFAULT_VERTICAL_ALIGNMENT = 'Center'
DEFAULT_HORIZONTAL_ALIGNMENT = 'Center'
OPTIMAL_TRANSPARENCY = 55

FULL_NAME_MAX_LENGTH = 16
BOUNTY_MAX_VALUE = 1_000_000_000_000_000
