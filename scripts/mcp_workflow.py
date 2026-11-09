"""A runnable eleven-tool walkthrough; obtain record IDs from real list results."""
import argparse
import json
from pathlib import Path
from mcp_protocol_client import ProtocolClient


def main():
    parser = argparse.ArgumentParser(description='实际返回ID驱动的11工具接入检查，不输出客户内容')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--start', default='2026-10-29')
    parser.add_argument('--end', default='2026-10-30')
    args = parser.parse_args()
    client = ProtocolClient(args.config)
    client.initialize()
    checked, skipped = [], []
    def call(name, params=None):
        result = client.call(name, params)
        checked.append(name)
        return result
    call('get_data_guide')
    state = call('get_sync_status')
    call('get_capabilities')
    call('list_taxonomy', {'limit':1})
    call('query_daily_statistics', {'start':args.start,'end':args.end,'level':3,'limit':1})
    mails = call('list_mails', {'start':args.start,'end':args.end,'limit':1})
    if mails['items']:
        call('get_mail_detail', {'mail_pk':mails['items'][0]['mail_pk']})
    else:
        skipped.append('get_mail_detail: 所选日期无邮件，请换有数据的区间')
    call('get_report_context', {'start':args.start,'end':args.end,'limit':1})
    call('list_source_tables')
    records = call('list_source_records', {'table':'messages','limit':1})
    if records['items']:
        call('get_source_record', {'table':'messages','record_key':records['items'][0]['record_key']})
    else:
        skipped.append('get_source_record: messages副本为空')
    print(json.dumps({'checked_tools':checked,'skipped':skipped,'source_id':state['source']['source_id'],
                      'data_version':state['source']['data_version'],'customer_content_printed':False},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
