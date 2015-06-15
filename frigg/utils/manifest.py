from manifesto import Manifest


class AppManifest(Manifest):
    def cache(self):
        return [
            '/offline.html',
            '//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css',
            '//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/fonts/fontawesome-webfont.ttf?v=4.3.0',
            '//fonts.googleapis.com/css?family=Lato:700,400,300,100',
            '//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/fonts/fontawesome-webfont.woff2?v=4.3.0'
        ]

    def network(self):
        return ['*']

    def fallback(self):
        return [
            ('/', '/offline.html'),
        ]
