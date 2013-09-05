# -*- coding: utf-8 -*-
# Copyright (c) 2011-2013 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="django-inplaceedit-extra-fields",
    version="0.1.0",
    author="Pablo Martin",
    author_email="goinnn@gmail.com",
    description="Django application that adds other useful fields to Django inplace edit",
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license="LGPL 3",
    keywords="django,inplace,inline edit,inline form,inline,inplace edit,inplace form,ajax,tinymce,autocomplete,thumbnail",
    url='https://github.com/goinnn/django-inplaceedit-extra-fields',
    packages=('inplaceeditform_extra_fields', ),
    include_package_data=True,
    zip_safe=False,
)
