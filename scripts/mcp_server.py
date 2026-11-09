"""Optional stdio entry point; the remote service is insights.cli mcp."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from insights.mcp_server import create_server

if __name__ == '__main__':
    create_server().run(transport='stdio')
