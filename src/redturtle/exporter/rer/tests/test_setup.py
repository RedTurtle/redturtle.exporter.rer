# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.exporter.rer.testing import REDTURTLE_EXPORTER_RER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that redturtle.exporter.rer is properly installed."""

    layer = REDTURTLE_EXPORTER_RER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if redturtle.exporter.rer is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'redturtle.exporter.rer'))

    def test_browserlayer(self):
        """Test that IRedturtleExporterRerLayer is registered."""
        from redturtle.exporter.rer.interfaces import (
            IRedturtleExporterRerLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRedturtleExporterRerLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = REDTURTLE_EXPORTER_RER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get(userid=TEST_USER_ID).getRoles()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['redturtle.exporter.rer'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if redturtle.exporter.rer is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'redturtle.exporter.rer'))

    def test_browserlayer_removed(self):
        """Test that IRedturtleExporterRerLayer is removed."""
        from redturtle.exporter.rer.interfaces import \
            IRedturtleExporterRerLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IRedturtleExporterRerLayer,
           utils.registered_layers())
