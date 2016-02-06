#!/bin/bash
date > $OPENSHIFT_REPO_DIR/wsgi/fiddly/log.txt
cd $OPENSHIFT_REPO_DIR/wsgi/fiddly/   && python $OPENSHIFT_REPO_DIR/wsgi/fiddly/feedlyApiTest.py
