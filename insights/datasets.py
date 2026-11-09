"""Public read contracts for the bounded source-record catalogue."""
from enum import Enum

from .source import TABLES

Dataset = Enum('Dataset', {table.name: table.name for table in TABLES}, type=str)
DESCRIPTIONS = {
    'mailboxes': '邮箱账号元数据',
    'folders': '文件夹元数据及目录状态',
    'messages': '原始邮件完整数据库行，包含正文和邮件头；不是附件文件本体',
    'attachments': '附件元数据；local_path 是源机器路径，文件没有复制',
    'imap_reconcile_archive': '归档快照和旧邮件映射；不计入当前邮件总数',
    'InboundMail': '业务入站邮件及 sourcePk 关联',
    'MailAiArtifact': '完整 AI 产物，包含未挂到当前邮件的孤立记录',
    'MailIssueBinding': '源问题绑定原始记录；正式汇总仅采用 AI 分类规则',
    'TaxonomyCandidate': '动态问题类型候选及源状态',
    'IssueTypeProposal': '问题类型提案及源状态',
    'TaxonomyCandidateSupport': '候选与邮件的支持关系',
    'IssueTypeRegistry': '源端问题类型注册表；空表是合法结果',
    'IssueTypeAlias': '源端问题类型别名；空表是合法结果',
    'IssueGroupLifecycle': '问题组生命周期；空表是合法结果',
}


def dataset_catalog():
    return [{'table': table.name, 'domain': table.domain, 'key_field': table.key,
             'description': DESCRIPTIONS[table.name]} for table in TABLES]
