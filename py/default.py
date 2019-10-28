#! /usr/bin/env python3

import google.auth as auth

adc, project = auth.default ();
print (project)
