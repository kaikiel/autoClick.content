# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from autoClick.content.testing import AUTOCLICK_CONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that autoClick.content is properly installed."""

    layer = AUTOCLICK_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if autoClick.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'autoClick.content'))

    def test_browserlayer(self):
        """Test that IAutoclickContentLayer is registered."""
        from autoClick.content.interfaces import (
            IAutoclickContentLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IAutoclickContentLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = AUTOCLICK_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['autoClick.content'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if autoClick.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'autoClick.content'))

    def test_browserlayer_removed(self):
        """Test that IAutoclickContentLayer is removed."""
        from autoClick.content.interfaces import \
            IAutoclickContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IAutoclickContentLayer,
            utils.registered_layers())
