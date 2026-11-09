"""Build a token-free handoff from a schema fetched from the running MCP."""
import argparse
import json
from pathlib import Path
import shutil
from mcp_portal_materials import build


def main():
    parser=argparse.ArgumentParser(description='构建无凭据MCP接收人材料')
    parser.add_argument('--schema-file',type=Path,required=True,help='运行中tools/list的result JSON')
    parser.add_argument('--replace-legacy-private-archive',action='store_true',help='将旧.secrets/mcp-handoff.zip替换为同一无令牌材料')
    args=parser.parse_args()
    schema=json.loads(args.schema_file.read_text(encoding='utf-8-sig'))
    result=build(schema)
    if args.replace_legacy_private_archive:
        root=Path(__file__).resolve().parents[1]
        shutil.copyfile(result['archive'],root/'.secrets/mcp-handoff.zip')
        result['legacy_archive_replaced_with_token_free_kit']=True
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__': main()
