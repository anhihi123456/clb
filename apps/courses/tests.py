from django.test import TestCase
from apps.courses.embed_utils import (
    extract_youtube_info,
    extract_gdrive_info,
    extract_gform_info,
    parse_media_url,
    EmbedParseError,
)


class EmbedUtilsTestCase(TestCase):
    def test_youtube_watch_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s"
        info = extract_youtube_info(url)
        self.assertEqual(info['provider'], 'youtube')
        self.assertEqual(info['external_id'], 'dQw4w9WgXcQ')
        self.assertEqual(info['embed_url'], 'https://www.youtube.com/embed/dQw4w9WgXcQ?enablejsapi=1&rel=0')

    def test_youtube_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ?si=abcdef"
        info = extract_youtube_info(url)
        self.assertEqual(info['external_id'], 'dQw4w9WgXcQ')

    def test_youtube_shorts_and_iframe(self):
        iframe_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0"></iframe>'
        info = extract_youtube_info(iframe_html)
        self.assertEqual(info['external_id'], 'dQw4w9WgXcQ')

    def test_gdrive_file_url(self):
        url = "https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing"
        info = extract_gdrive_info(url)
        self.assertEqual(info['provider'], 'gdrive')
        self.assertEqual(info['external_id'], '1A2B3C4D5E6F7G8H9I0J')
        self.assertEqual(info['embed_url'], 'https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/preview')

    def test_gslides_url(self):
        url = "https://docs.google.com/presentation/d/1XyZ_PresentationId123/edit#slide=id.p"
        info = extract_gdrive_info(url)
        self.assertEqual(info['provider'], 'gslides')
        self.assertEqual(info['external_id'], '1XyZ_PresentationId123')
        self.assertIn('embed', info['embed_url'])

    def test_gform_url(self):
        url = "https://docs.google.com/forms/d/e/1FAIpQLScFormId123/viewform?usp=sf_link"
        info = extract_gform_info(url)
        self.assertEqual(info['provider'], 'gforms')
        self.assertEqual(info['embed_url'], 'https://docs.google.com/forms/d/e/1FAIpQLScFormId123/viewform?embedded=true')

    def test_invalid_urls_raise_error(self):
        with self.assertRaises(EmbedParseError):
            extract_youtube_info("https://vimeo.com/1234567")
        with self.assertRaises(EmbedParseError):
            extract_gdrive_info("https://dropbox.com/s/12345/file.pdf")
        with self.assertRaises(EmbedParseError):
            parse_media_url("https://malicious-site.com/hack.js")
