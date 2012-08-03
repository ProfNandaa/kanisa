from django.forms.util import ErrorList

from kanisa import conf
from kanisa.forms import KanisaBaseForm, BootstrapDateField
from kanisa.widgets import EpicWidget
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from kanisa.models import (SermonSeries,
                           Sermon,
                           SermonSpeaker)


class SermonSeriesForm(KanisaBaseForm):
    class Meta:
        model = SermonSeries
        widgets = {'details': EpicWidget(), }


class SermonSpeakerForm(KanisaBaseForm):
    class Meta:
        model = SermonSpeaker


class SermonForm(KanisaBaseForm):
    date = BootstrapDateField()

    class Meta:
        model = Sermon
        widgets = {'details': EpicWidget(), }

    def clean(self):
        super(SermonForm, self).clean()
        cleaned_data = self.cleaned_data

        if u'mp3' in self.files:
            if hasattr(self.files['mp3'], 'temporary_file_path'):
                audio = MP3(self.files['mp3'].temporary_file_path())
            else:
                # You probably need to set FILE_UPLOAD_HANDLERS to
                # django.core.files.uploadhandler.TemporaryFileUploadHandler
                audio = None

            if not audio or not audio.info or audio.info.sketchy:
                errors = ErrorList([u'Please upload a valid MP3.'])
                self._errors["mp3"] = errors
                del cleaned_data["mp3"]
            else:
                audio = EasyID3(self.files['mp3'].temporary_file_path())
                audio['title'] = cleaned_data['title']
                audio['artist'] = unicode(cleaned_data['speaker'])

                if not cleaned_data['series']:
                    album_title = 'Sermons from %s' % conf.KANISA_CHURCH_NAME
                else:
                    album_title = unicode(cleaned_data['series'])
                audio['album'] = album_title

                audio['albumartistsort'] = conf.KANISA_CHURCH_NAME
                audio['organization'] = conf.KANISA_CHURCH_NAME
                audio['genre'] = 'Speech'

                # Not sure if this date format is right - the MP3
                # players I've got to test with don't show anything
                # more than the year.
                audio['date'] = cleaned_data['date'].strftime('%Y%m%d')

                audio.save()

        return cleaned_data
