# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from flask import request
from wtforms import ValidationError
from datetime import datetime
from wtforms.validators import DataRequired, StopValidation


class ValidateTime:
    def __init__(self, message=None):
        if not message:
            message = 'Bitte geben Sie die Zeit im Format HH:MM:SS an.'
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message)
        if len(field.data) < 7:
            raise ValidationError(self.message)
        if field.data[-3:-2] != ':' or field.data[-6:-5] != ':':
            raise ValidationError(self.message)
        try:
            test = int(field.data[-8:-6]) + int(field.data[-5:-3]) + int(field.data[-2:])
        except ValueError:
            raise ValidationError(self.message)


class ValidateFloat:
    def __init__(self, message=None):
        if not message:
            message = 'Bitte geben Sie eine Fließkommazahl an'
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message)
        data = field.data.replace(',', '.')
        try:
            data = float(data)
        except ValueError:
            raise ValidationError(self.message)


class ValidateMimeType:
    def __init__(self, mimetypes, allow_empty=False, message=None):
        if not message:
            message = 'select proper mimetype'
        self.message = message
        self.mimetypes = mimetypes
        self.allow_empty = allow_empty

    def __call__(self, form, field):
        data = request.files.get(field.name)
        if not data and not self.allow_empty:
            raise ValidationError(self.message)
        if self.allow_empty:
            return
        if not data.filename:
            raise ValidationError(self.message)
        if data.content_type not in self.mimetypes and data.filename:
            raise ValidationError(self.message)


class ValidateDate:
    def __init__(self, message=None):
        self.message = message
        if not message:
            message = 'select proper date'

    def __call__(self, form, field):
        if field.data:
            try:
                datetime.strptime(field.data.strip(), '%d.%m.%Y').date()
            except ValueError:
                raise ValidationError(self.message)


class ValidateMultiDate:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data:
            dates = field.data.split(',')
            for date_str in dates:
                try:
                    datetime.strptime(date_str.strip() + str(datetime.now().year), '%d.%m.%Y').date()
                except ValueError:
                    raise ValidationError(self.message)


class ValidateDateRange:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message)
        dates = field.data.split(' - ')
        if len(dates) != 2:
            raise ValidationError(self.message)
        for date_str in dates:
            try:
                datetime.strptime(date_str, '%d.%m.%Y').date()
            except ValueError:
                raise ValidationError(self.message)


class ValidateDateTimeRange:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message)
        dates = field.data.split(' - ')
        if len(dates) != 2:
            raise ValidationError(self.message)
        for date_str in dates:
            try:
                datetime.strptime(date_str, '%d.%m.%Y, %H:%M')
            except ValueError:
                raise ValidationError(self.message)


class DataRequiredIf(DataRequired):
    def __init__(self, other_field_name, other_field_values, *args, **kwargs):
        self.other_field_name = other_field_name
        self.other_field_values = other_field_values
        super(DataRequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data in self.other_field_values:
            super(DataRequiredIf, self).__call__(form, field)
        else:
            field.errors = []
            raise StopValidation()

