# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import redturtle.exporter.rer


class RedturtleExporterRerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=redturtle.exporter.rer)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'redturtle.exporter.rer:default')


REDTURTLE_EXPORTER_RER_FIXTURE = RedturtleExporterRerLayer()


REDTURTLE_EXPORTER_RER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_EXPORTER_RER_FIXTURE,),
    name='RedturtleExporterRerLayer:IntegrationTesting'
)


REDTURTLE_EXPORTER_RER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_EXPORTER_RER_FIXTURE,),
    name='RedturtleExporterRerLayer:FunctionalTesting'
)


REDTURTLE_EXPORTER_RER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        REDTURTLE_EXPORTER_RER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='RedturtleExporterRerLayer:AcceptanceTesting'
)
