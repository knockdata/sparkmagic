# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.
from sparkmagic.controllerwidget.abstractmenuwidget import AbstractMenuWidget
from sparkmagic.controllerwidget.attachsessionwidget import AttachSessionWidget
from sparkmagic.controllerwidget.managesessionwidget import ManageSessionWidget
from sparkmagic.controllerwidget.createsessionwidget import CreateSessionWidget
from sparkmagic.livyclientlib.endpoint import Endpoint
from sparkmagic.utils.constants import LANGS_SUPPORTED
import sparkmagic.utils.configuration as conf


class MagicsControllerWidget(AbstractMenuWidget):
    def __init__(self, spark_controller, ipywidget_factory, ipython_display, endpoints=None):
        super(MagicsControllerWidget, self).__init__(spark_controller, ipywidget_factory, ipython_display)

        self.endpoint = self._get_default_endpoint()

        self._refresh()

    def run(self):
        pass

    @staticmethod
    def _get_default_endpoint():
        endpoint_config = getattr(conf, 'kernel_credentials')()
        if all([p in endpoint_config for p in ["url", "password", "username"]]) and endpoint_config["url"] != "":
            user = endpoint_config["username"]
            passwd = endpoint_config["password"]
            
            authentication = endpoint_config.get("auth", None)
            if authentication is None:
                authentication = conf.get_auth_value(user, passwd)

            default_endpoint = Endpoint(
                username=user,
                password=passwd,
                auth=authentication,
                url=endpoint_config["url"],
                implicitly_added=True)

        return default_endpoint

    def _refresh(self):
        self.attach_session = AttachSessionWidget(self.spark_controller, self.ipywidget_factory, self.ipython_display, self.endpoint,
                                                  self._refresh)
        self.manage_session = ManageSessionWidget(self.spark_controller, self.ipywidget_factory, self.ipython_display, self.endpoint,
                                                  self._refresh)
        self.create_session = CreateSessionWidget(self.spark_controller, self.ipywidget_factory, self.ipython_display,
                                                  self.endpoint, self._refresh)

        self.tabs = self.ipywidget_factory.get_tab(children=[self.attach_session,self.create_session,self.manage_session])

        self.tabs.set_title(0, "Attach Session")
        self.tabs.set_title(1, "Create Session")
        self.tabs.set_title(2, "Delete Session")

        self.children = [self.tabs]

        for child in self.children:
            child.parent_widget = self
