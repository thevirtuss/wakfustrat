import bleach
import markdown


def generate_html(text):
    """
    Generate the HTML based on markdown.
    """
    md = markdown.Markdown(extensions=['markdown.extensions.toc'], output_format='html5')
    html = md.convert(bleach.clean(text))
    return html, md.toc
