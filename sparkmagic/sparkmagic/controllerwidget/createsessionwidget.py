# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.
import json

import sparkmagic.utils.configuration as conf
from sparkmagic.utils.constants import LANG_SCALA, LANG_PYTHON
from sparkmagic.controllerwidget.abstractmenuwidget import AbstractMenuWidget
import sparkmagic.utils.configuration as conf

class CreateSessionWidget(AbstractMenuWidget):
    def __init__(self, spark_controller, ipywidget_factory, ipython_display, endpoint, refresh_method):
        # This is nested
        super(CreateSessionWidget, self).__init__(spark_controller, ipywidget_factory, ipython_display, True)

        self.refresh_method = refresh_method
        self.endpoint = endpoint

        self.session_widget = self.ipywidget_factory.get_text(
            description='Name:',
            value='session-name'
        )
        self.lang_widget = self.ipywidget_factory.get_toggle_buttons(
            description='Language:',
            options=[LANG_SCALA, LANG_PYTHON],
        )
        self.properties = self.ipywidget_factory.get_text(
            description='Properties:',
            value=json.dumps(conf.session_configs())
        )
        self.submit_widget = self.ipywidget_factory.get_submit_button(
            description='Create Session'
        )

        self.children = [self.ipywidget_factory.get_html(value="<br />", width="600px"), 
                         self.session_widget, self.lang_widget, self.properties,
                         self.ipywidget_factory.get_html(value="<br />", width="600px"), self.submit_widget]

        for child in self.children:
            child.parent_widget = self

    def run(self):
        try:
            properties_json = self.properties.value
            if properties_json.strip() != "":
                conf.override(conf.session_configs.__name__, json.loads(self.properties.value))
        except ValueError as e:
            self.ipython_display.send_error("Session properties must be a valid JSON string. Error:\n{}".format(e))
            return

        language = self.lang_widget.value
        alias = self.session_widget.value
        skip = False
        properties = conf.get_session_properties(language)
        properties["name"]= alias
        properties["conf"]["spark.kubernetes.file.upload.path"] =  conf.s3_bucket()
        properties["conf"]["spark.hadoop.fs.s3a.access.key"] =  conf.s3_access_key()
        properties["conf"]["spark.hadoop.fs.s3a.secret.key"] = conf.s3_secret_key()
		
        try:
            self.spark_controller.add_session(alias, self.endpoint, skip, properties)
        except ValueError as e:
            self.ipython_display.send_error("""Could not add session with
name:
    {}
properties:
    {}

due to error: '{}'""".format(alias, properties, e))
            return

        self.refresh_method()
