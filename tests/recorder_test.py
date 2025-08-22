#!/usr/bin/env python3

import pytest
import unittest
import importlib
import sys
import os
from unittest import mock
from unittest.mock import patch, MagicMock

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

    def test_recorder_state_config_db_success(self):
        """Test successful recorder state command for config-db"""
        from click.testing import CliRunner
        from utilities_common.db import Db
        
        runner = CliRunner()
        
        # Create a proper mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb
        
        # Mock successful database operation
        mock_cfgdb.set_entry.return_value = None
        
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['config-db', 'enabled'],
            obj=mock_db)
        
        self.assertEqual(result.exit_code, 0)
        mock_cfgdb.set_entry.assert_called_once_with('RECORDER', 'config_db', {'state': 'enabled'})

    def test_recorder_state_state_db_success(self):
        """Test successful recorder state command for state-db"""
        from click.testing import CliRunner
        from utilities_common.db import Db
        
        runner = CliRunner()
        
        # Create a proper mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb
        
        # Mock successful database operation
        mock_cfgdb.set_entry.return_value = None
        
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['state-db', 'disabled'],
            obj=mock_db)
        
        self.assertEqual(result.exit_code, 0)
        mock_cfgdb.set_entry.assert_called_once_with('RECORDER', 'state_db', {'state': 'disabled'})

    def test_recorder_state_config_db_failure(self):
        """Test recorder state command failure for config-db"""
        from click.testing import CliRunner
        from utilities_common.db import Db
        
        runner = CliRunner()
        
        # Create a proper mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb
        
        # Mock database operation failure
        mock_cfgdb.set_entry.side_effect = Exception("Database operation failed")
        
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['config-db', 'enabled'],
            obj=mock_db)
        
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to set recorder state: Database operation failed", result.output)

    def test_recorder_state_state_db_failure(self):
        """Test recorder state command failure for state-db"""
        from click.testing import CliRunner
        from utilities_common.db import Db
        
        runner = CliRunner()
        
        # Create a proper mock Db object
        mock_db = MagicMock(spec=Db)
        mock_cfgdb = MagicMock()
        mock_db.cfgdb = mock_cfgdb
        
        # Mock database operation failure
        mock_cfgdb.set_entry.side_effect = Exception("Database operation failed")
        
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['state-db', 'disabled'],
            obj=mock_db)
        
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to set recorder state: Database operation failed", result.output)

    def test_recorder_state_invalid_db_type(self):
        """Test recorder state command with invalid database type"""
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # This test should not be reachable due to click.Choice validation,
        # but it's good to have for future extensibility
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['invalid-db', 'enabled'])
        
        # Should fail due to invalid choice
        self.assertNotEqual(result.exit_code, 0)

    def test_recorder_state_invalid_state(self):
        """Test recorder state command with invalid state"""
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # This test should not be reachable due to click.Choice validation
        result = runner.invoke(
            config.config.commands['recorder'].commands['state'],
            ['config-db', 'invalid-state'])
        
        # Should fail due to invalid choice
        self.assertNotEqual(result.exit_code, 0)

    def test_recorder_command_structure(self):
        """Test that recorder commands are properly structured"""
        # Verify the recorder group exists
        self.assertIn('recorder', config.config.commands)
        
        # Verify only the state command exists (start/stop were removed)
        self.assertIn('state', config.config.commands['recorder'].commands)
        self.assertNotIn('start', config.config.commands['recorder'].commands)
        self.assertNotIn('stop', config.config.commands['recorder'].commands)

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

    @classmethod
    def tearDownClass(cls):
        """Clean up test class"""
        print('TEARDOWN')


if __name__ == '__main__':
    unittest.main()
