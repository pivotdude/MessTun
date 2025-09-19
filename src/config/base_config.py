import yaml
from typing import Dict, Any

class BaseConfig:
  """Base class for configuration management"""
  
  def __init__(self, config_file: str = "config.yml"):
    self.config_file = config_file
    self._config = self._load_config()
  
  def _load_config(self) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
      with open(self.config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}
    except FileNotFoundError:
      raise FileNotFoundError(f"Config file {self.config_file} not found")
    except yaml.YAMLError as e:
      raise ValueError(f"Error parsing config file: {e}")
    

  def get_config_value_safe(self, key: str, default_value: Any = None) -> Any:
    """Safe getting of configuration value by key with default value return
    
    Args:
      key: Key in 'section.subsection' format or just 'section'
      default_value: Default value if key not found (default None)
        
    Returns:
      Configuration value or default value if key not found
        
    Raises:
      ValueError: If key validation failed
    """
    try:
      return self.get_config_value(key)
    except KeyError:
      return default_value
  
  def get_config_value(self, key: str) -> Any:
      """Getting configuration value by key with validation
      
      Args:
          key: Key in 'section.subsection' format or just 'section'
          default: Default value if key not found
          
      Returns:
          Configuration value or default value
      """
      # Call validation for requested key
      self._validate_config_key(key)
      
      keys = key.split('.')
      value = self._config
      
      for k in keys:
        if isinstance(value, dict) and k in value:
          value = value[k]
        else:
          raise KeyError(f"Config key '{key}' not found in configuration")
      
      return value
  
  def _validate_config_key(self, key: str) -> None:
    """Validation of specific configuration key
    
    Args:
      key: Key for validation
        
    Raises:
      ValueError: If key validation failed
    """
    if not key:
      raise ValueError("Config key cannot be empty")
    
    if not isinstance(key, str):
      raise ValueError(f"Config key must be a string, got {type(key).__name__}")
    
    # Check for invalid characters
    invalid_chars = ['\n', '\r', '\t', ' ']
    if any(char in key for char in invalid_chars):
      raise ValueError(f"Config key '{key}' contains invalid characters (whitespace/newlines)")
    
    # Check key format
    if key.startswith('.') or key.endswith('.'):
      raise ValueError(f"Config key '{key}' cannot start or end with dot")
    
    # Check for consecutive dots
    if '..' in key:
      raise ValueError(f"Config key '{key}' cannot contain consecutive dots")
    
    # Check key length
    if len(key) > 100:
      raise ValueError(f"Config key '{key}' is too long (max 100 characters)")
    
    # Check for empty sections between dots
    sections = key.split('.')
    if any(not section.strip() for section in sections):
      raise ValueError(f"Config key '{key}' contains empty sections")
  