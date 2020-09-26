#!/bin/bash
FLASK_ENV=development FLASK_DEBUG=1 FLASK_APP=kni python -m flask run $*
