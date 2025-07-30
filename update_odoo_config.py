#!/usr/bin/env python3
"""
Script to update Odoo configuration for better Chrome compatibility
"""

import configparser
import os
import shutil
from datetime import datetime

def backup_config(config_path):
    """Create a backup of the current configuration"""
    backup_path = f"{config_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(config_path, backup_path)
    print(f"✓ Configuration backed up to: {backup_path}")
    return backup_path

def update_odoo_config(config_path="/etc/odoo16.conf"):
    """Update Odoo configuration for Chrome compatibility"""
    
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    # Backup original config
    backup_path = backup_config(config_path)
    
    # Read current configuration
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # Ensure [options] section exists
    if 'options' not in config:
        config.add_section('options')
    
    # Chrome compatibility settings
    chrome_settings = {
        'proxy_mode': 'True',
        'workers': '4',  # Adjust based on your server capacity
        'max_cron_threads': '2',
        'db_maxconn': '64',
        'limit_memory_hard': '2684354560',  # 2.5GB
        'limit_memory_soft': '2147483648',  # 2GB
        'limit_request': '8192',
        'limit_time_cpu': '600',
        'limit_time_real': '1200',
        'limit_time_real_cron': '300',
        # Enable server-wide modules for better performance
        'server_wide_modules': 'base,web',
        # Log level for debugging if needed
        'log_level': 'info',
        # Database connection settings
        'db_template': 'template0',
    }
    
    # Apply settings
    for key, value in chrome_settings.items():
        config.set('options', key, value)
        print(f"✓ Set {key} = {value}")
    
    # Write updated configuration
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    
    print(f"\n✓ Configuration updated successfully!")
    print(f"✓ Backup saved to: {backup_path}")
    print("\n📋 Next steps:")
    print("1. Copy the new nginx configuration:")
    print("   sudo cp odoo_nginx_fixed.conf /etc/nginx/sites-available/odoo")
    print("2. Test nginx configuration:")
    print("   sudo nginx -t")
    print("3. Reload nginx:")
    print("   sudo systemctl reload nginx")
    print("4. Restart Odoo:")
    print("   sudo systemctl restart odoo16")
    print("5. Clear browser cache and test in Chrome")
    
    return True

if __name__ == "__main__":
    # Try common Odoo config paths
    config_paths = [
        "/etc/odoo16.conf",
        "/etc/odoo.conf",
        "/opt/odoo/odoo.conf",
        "./odoo.conf"
    ]
    
    config_found = False
    for path in config_paths:
        if os.path.exists(path):
            print(f"Found Odoo configuration: {path}")
            update_odoo_config(path)
            config_found = True
            break
    
    if not config_found:
        print("❌ No Odoo configuration file found in common locations.")
        print("Please specify the correct path to your odoo.conf file.")
        print("Usage: python3 update_odoo_config.py")
        print("Or edit the script to use your custom config path.")