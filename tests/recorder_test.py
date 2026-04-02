#!/usr/bin/env python3

import pytest
import unittest
import importlib
import sys
import os
from unittest import mock
from unittest.mock import patch, MagicMock, Mock

# Add test path to sys.path
test_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.dirname(test_path)
sys.path.insert(0, test_path)
sys.path.insert(0, modules_path)

# Import the config module
import config.main as config


class TestConfigRecorder(unittest.TestCase):
    """Test cases for config recorder commands"""

    @classmethod
    def setUpClass(cls):
        """Set up test class"""
        print('SETUP')
        # Reload the config module to ensure we have the latest version
        importlib.reload(config)

    def setUp(self):
        """Set up each test"""
        pass



    @patch('config.main.get_available_databases')
    def test_recorder_enable_all_success(self, mock_get_dbs):
        """Test successful recorder enable-all command"""
        from click.testing import CliRunner

        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        runner = CliRunner()

        # Mock the database operations directly
        with patch('utilities_common.db.Db') as mock_db_class:
            mock_db_instance = MagicMock()
            mock_cfgdb = MagicMock()
            mock_db_instance.cfgdb = mock_cfgdb
            mock_db_class.return_value = mock_db_instance

            # Mock successful database operation
            mock_cfgdb.set_entry.return_value = None

            result = runner.invoke(
                config.config.commands['recorder'].commands['enable-all'])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Successfully enabled recorder for all", result.output)

    @patch('config.main.get_available_databases')
    def test_recorder_disable_all_success(self, mock_get_dbs):
        """Test successful recorder disable-all command"""
        from click.testing import CliRunner

        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        runner = CliRunner()

        # Mock the database operations directly
        with patch('utilities_common.db.Db') as mock_db_class:
            mock_db_instance = MagicMock()
            mock_cfgdb = MagicMock()
            mock_db_instance.cfgdb = mock_cfgdb
            mock_db_class.return_value = mock_db_instance

            # Mock successful database operation
            mock_cfgdb.set_entry.return_value = None

            result = runner.invoke(
                config.config.commands['recorder'].commands['disable-all'])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Successfully disabled recorder for all", result.output)



    @patch('config.main.get_available_databases')
    def test_recorder_state_config_db_success(self, mock_get_dbs):
        """Test successful recorder state command for CONFIG_DB"""
        from click.testing import CliRunner
        from utilities_common.db import Db


        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        # Create a mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb

        runner = CliRunner()

        # Mock successful database operation
        mock_cfgdb.set_entry.return_value = None

        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['CONFIG_DB', 'enabled'],
            obj=mock_db)

        self.assertEqual(result.exit_code, 0)

        # Verify the database call was made correctly
        mock_cfgdb.set_entry.assert_called_once_with('RECORDER', 'CONFIG_DB', {'state': 'enabled'})

    @patch('config.main.get_available_databases')
    def test_recorder_state_state_db_success(self, mock_get_dbs):
        """Test successful recorder state command for STATE_DB"""
        from click.testing import CliRunner
        from utilities_common.db import Db

        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        # Create a mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb

        runner = CliRunner()

        # Mock successful database operation
        mock_cfgdb.set_entry.return_value = None

        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['STATE_DB', 'disabled'],
            obj=mock_db)

        self.assertEqual(result.exit_code, 0)

        # Verify the database call was made correctly
        mock_cfgdb.set_entry.assert_called_once_with('RECORDER', 'STATE_DB', {'state': 'disabled'})

    @patch('config.main.get_available_databases')
    def test_recorder_state_config_db_failure(self, mock_get_dbs):
        """Test recorder state command failure for CONFIG_DB"""
        from click.testing import CliRunner
        from utilities_common.db import Db


        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        # Create a mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb

        runner = CliRunner()

        # Mock database operation failure
        mock_cfgdb.set_entry.side_effect = Exception("Database operation failed")

        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['CONFIG_DB', 'enabled'],
            obj=mock_db)

        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to set recorder state: Database operation failed", result.output)

    @patch('config.main.get_available_databases')
    def test_recorder_state_state_db_failure(self, mock_get_dbs):
        """Test recorder state command failure for STATE_DB"""
        from click.testing import CliRunner
        from utilities_common.db import Db


        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        # Create a mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb

        runner = CliRunner()

        # Mock database operation failure
        mock_cfgdb.set_entry.side_effect = Exception("Database operation failed")

        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['STATE_DB', 'enabled'],
            obj=mock_db)

        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to set recorder state: Database operation failed", result.output)

    @patch('config.main.get_available_databases')
    def test_recorder_state_invalid_db_type(self, mock_get_dbs):
        """Test recorder state command with invalid database type"""
        from click.testing import CliRunner

        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        # Create a mock Db object
        mock_db = MagicMock()
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb

        runner = CliRunner()

        # Test with invalid database type - should fail due to runtime validation
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['INVALID_DB', 'enabled'],
            obj=mock_db)

        # Should fail due to invalid database type
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error: Database 'INVALID_DB' not found", result.output)


    @patch('config.main.get_available_databases')
    def test_recorder_state_invalid_state(self, mock_get_dbs):
        """Test recorder state command with invalid state"""
        from click.testing import CliRunner

        # Mock the available databases
        mock_get_dbs.return_value = ['CONFIG_DB', 'STATE_DB']

        # Create a mock Db object
        mock_db = MagicMock()
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb

        runner = CliRunner()

        # This test should not be reachable due to click.Choice validation
        # but we need to provide a valid database type to get past the runtime validation
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['CONFIG_DB', 'invalid-state'],
            obj=mock_db)

        # Should fail due to invalid choice
        self.assertNotEqual(result.exit_code, 0)

    def test_recorder_command_structure(self):
        """Test that recorder commands are properly structured"""
        # Verify the recorder group exists
        self.assertIn('recorder', config.config.commands)

        # Verify the state command exists
        self.assertIn('state', config.config.commands['recorder'].commands)

        # Verify the enable-all command exists
        self.assertIn('enable-all', config.config.commands['recorder'].commands)

        # Verify the disable-all command exists
        self.assertIn('disable-all', config.config.commands['recorder'].commands)

    def test_recorder_help_texts(self):
        """Test that recorder commands have proper help text"""
        from click.testing import CliRunner

        runner = CliRunner()

        # Test recorder group help
        result = runner.invoke(config.config.commands['recorder'], ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Redis recorder service management", result.output)

        # Test state command help
        result = runner.invoke(config.config.commands['recorder'].commands['state'], ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configure recorder state in the specified database", result.output)

        # Test enable-all command help
        result = runner.invoke(config.config.commands['recorder'].commands['enable-all'], ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Enable recorder for all databases", result.output)

        # Test disable-all command help
        result = runner.invoke(config.config.commands['recorder'].commands['disable-all'], ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Disable recorder for all databases", result.output)

    @classmethod
    def tearDownClass(cls):
        """Clean up test class"""
        print('TEARDOWN')


if __name__ == '__main__':
    unittest.main()
