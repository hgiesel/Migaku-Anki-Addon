from collections import OrderedDict
from typing import List
import re

from . util import addon_path, addon_web_uri


class FieldOption:
    
    def __init__(self, value: str, label: str):
        self.value = value
        self.label = label


class FieldSetting:

    def __init__(self, name: str, label: str, options: List[FieldOption]):
        self.name = name
        self.label = label
        self.options = options


class Language:

    BRACKET_REMOVE_RE = re.compile(r'\[.*?\](?![^<]*>)')

    def __init__(self, code: str, name_en: str, name_native: str, fields: List[str], field_settings: List[FieldSetting]):
        self.code = code
        self.name_en = name_en
        self.name_native = name_native
        self.fields = fields
        self.field_settings = field_settings

    def __repr__(self):
        return F'<Language {self.code}>'

    def file_path(self, *path_parts):
        return addon_path('languages', self.code, *path_parts)

    def web_uri(self, *path_parts):
        return addon_web_uri('languages', self.code, *path_parts)

    def add_syntax(self, text, on_done):
        raise NotImplementedError

    def remove_syntax(self, text):
        return self.BRACKET_REMOVE_RE.sub('', text)


class LanguagesMeta(type):

    def __new__(mcls, name, bases, attrs):
        mcls.entries = OrderedDict()

        for name, lang in attrs.items():
            if isinstance(lang, Language):
                mcls.entries[lang.code] = lang

        return super().__new__(mcls, name, bases, attrs)

    def __iter__(mcls):
        return (mcls.entries[code] for code in mcls.entries.keys())

    def __getitem__(mcls, key):
        return mcls.entries[key]

    def __len__(mcls):
        return len(mcls.entries)


class Languages(metaclass=LanguagesMeta):

    Japanese = Language(
        name_en='Japanese',
        name_native='日本語',
        code='ja',
        fields=[
            'Word',
            'Sentence',
            'Definitions',
            'Translation',
            'Word Audio',
            'Sentence Audio',
            'Image',
            'Is Vocabulary Card',
            'Is Audio Card',
        ],
        field_settings=[
            FieldSetting('popup', 'Popup', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
            ]),
            FieldSetting('furigana', 'Furigana', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
                FieldOption('hidden', 'Hidden'),
            ]),
            FieldSetting('pitch-coloring', 'Pitch Coloring', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
            ]),
            FieldSetting('pitch-shapes', 'Pitch Shapes', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
            ]),
        ],
    )

    ChineseSimplified = Language(
        name_en='Chinese Simplified',
        name_native='汉语',
        code='zh_CN',
        fields=[
            'Word',
            'Sentence',
            'Definitions',
            'Translation',
            'Word Audio',
            'Sentence Audio',
            'Image',
            'Sentence Variant',
            'Is Vocabulary Card',
            'Is Audio Card',
        ],
        field_settings=[
            FieldSetting('reading', 'Reading', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
                FieldOption('hidden', 'Hidden'),
            ]),
            FieldSetting('reading-type', 'Reading Type', [
                FieldOption('pinyin', 'Pinyin'),
                FieldOption('bopomofo', 'Bopomofo'),
            ]),
            FieldSetting('tone-coloring', 'Tone Coloring', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
            ]),
        ],
    )

    ChineseTraditional = Language(
        name_en='Chinese Traditional',
        name_native='漢語',
        code='zh_TW',
        fields=[
            'Word',
            'Sentence',
            'Definitions',
            'Translation',
            'Word Audio',
            'Sentence Audio',
            'Image',
            'Sentence Variant',
            'Is Vocabulary Card',
            'Is Audio Card',
        ],
        field_settings=[
            FieldSetting('popup', 'Popup', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
            ]),
            FieldSetting('reading', 'Reading', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
                FieldOption('hidden', 'Hidden'),
            ]),
            FieldSetting('reading-type', 'Reading Type', [
                FieldOption('bopomofo', 'Bopomofo'),
                FieldOption('pinyin', 'Pinyin'),
            ]),
            FieldSetting('tone-coloring', 'Tone Coloring', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
            ]),
        ],
    )

    German = Language(
        name_en='German',
        name_native='Deutsch',
        code='de',
        fields=[
            'Word',
            'Sentence',
            'Definitions',
            'Translation',
            'Word Audio',
            'Sentence Audio',
            'Image',
            'Is Vocabulary Card',
            'Is Audio Card',
        ],
        field_settings=[
            FieldSetting('popup', 'Popup', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
            ]),
            FieldSetting('gender-coloring', 'Gender Coloring', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
            ])
        ],
    )

    Spanish = Language(
        name_en='Spanish',
        name_native='Español',
        code='es',
        fields=[
            'Word',
            'Sentence',
            'Definitions',
            'Translation',
            'Word Audio',
            'Sentence Audio',
            'Image',
            'Is Vocabulary Card',
            'Is Audio Card',
        ],
        field_settings=[
            FieldSetting('popup', 'Popup', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
            ]),
            FieldSetting('gender-coloring', 'Gender Coloring', [
                FieldOption('no', 'Disabled'),
                FieldOption('yes', 'Enabled'),
                FieldOption('hover', 'On Hover'),
            ])
        ],
    )

    @classmethod
    def by_idx(cls, idx):
        return list(cls)[idx]
