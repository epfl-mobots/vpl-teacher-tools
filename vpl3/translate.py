
# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# translation support (base class for any language)


class Translate:

    def __init__(self):
        self.dicts = {}
        self.language = "en"
        self.init_default_lang()

    def init_default_lang(self):
        self.dicts["en"] = {
            "Advanced Simulator Features": "Advanced Simulator Features",
            "Copy URL": "Copy URL",
            "Developer Tools": "Developer Tools",
            "Edit": "Edit",
            "English": "English",
            "File": "File",
            "French": "French",
            "JSON WebSocket": "JSON WebSocket",
            "Log Display in Dashboard": "Log Display in Dashboard",
            "Login Screen QR Code": "Login Screen QR Code",
            "No Robot": "No Robot",
            "Number of connections:": "Number of connections:",
            "Open Tools in Browser": "Open Tools in Browser",
            "Open tools in browser": "Open tools in browser",
            "Options": "Options",
            "Shortened URLs": "Shortened URLs",
            "Thymio Device Manager": "Thymio Device Manager",
            "VPL Server": "VPL Server",
        }

    def set_dictionary(self, language, dict):
        self.dicts[language] = dict

    def set_translation(self, language, key, translation):
        if language not in self.dicts:
            self.dicts[language] = {
                key: translation
            }
        else:
            self.dicts[language][key] = translation

    def set_language(self, language):
        self.language = language

    def tr(self, key):
        return (self.dicts[self.language][key]
                if self.language in self.dicts
                and key in self.dicts[self.language]
                else key)
