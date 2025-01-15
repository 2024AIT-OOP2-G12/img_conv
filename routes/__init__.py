from .change import change_bp
from .login import login_bp


# Blueprintをリストとしてまとめる
blueprints = [
  change_bp,
  login_bp
]
