"""Idempotently prepare local MCP TLS and handoff credentials. Never prints tokens."""
from datetime import datetime, timedelta, timezone
from ipaddress import ip_address, ip_network
import argparse
import json
from pathlib import Path
import secrets
import sys

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from insights.cli import protect_directory
from insights.mcp_http import MCPSettings, PRIVATE_NETWORKS


def write_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',required=True)
    parser.add_argument('--port',type=int,default=3037)
    parser.add_argument('--allow-network',required=True,action='append')
    args = parser.parse_args()
    address = ip_address(args.host)
    networks = [ip_network(value,strict=True) for value in args.allow_network]
    if address.version!=4 or not any(address in network for network in PRIVATE_NETWORKS):
        parser.error('one RFC1918 IPv4 address required')
    if not 1024<=args.port<=65535 or not networks or not any(address in network for network in networks):
        parser.error('invalid MCP port or network')
    if any(not any(network.subnet_of(private) for private in PRIVATE_NETWORKS) for network in networks):
        parser.error('only private client networks allowed')
    private = ROOT/'.secrets'
    protect_directory(private)
    profile = private/'mcp-server.json'
    if profile.exists():
        existing = MCPSettings.load(profile)
        if (existing.host,existing.port,existing.allowed_networks)!=(args.host,args.port,tuple(args.allow_network)):
            raise ValueError('existing MCP profile differs; refusing to overwrite credentials or certificates')
        print(json.dumps({'status':'ALREADY_PREPARED','url':f'https://{args.host}:{args.port}/mcp'}))
        return
    assets = ['mcp-ca.key','mcp-server.key','mcp-server.crt','mcp-client.json','mcp-client-config.json']
    if any((private/name).exists() for name in assets):
        raise ValueError('partial MCP provision exists; inspect it instead of overwriting')
    if not (private/'agent.json').is_file():
        raise ValueError('initialize the local data service first')
    now = datetime.now(timezone.utc)
    ca_key = rsa.generate_private_key(public_exponent=65537,key_size=3072)
    server_key = rsa.generate_private_key(public_exponent=65537,key_size=3072)
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Complaint Insights Local MCP CA')])
    ca = (x509.CertificateBuilder().subject_name(ca_name).issuer_name(ca_name).public_key(ca_key.public_key())
          .serial_number(x509.random_serial_number()).not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=1095))
          .add_extension(x509.BasicConstraints(ca=True,path_length=0),critical=True)
          .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()),critical=False)
          .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),critical=False)
          .add_extension(x509.KeyUsage(False,False,False,False,False,True,True,False,False),critical=True)
          .sign(ca_key,hashes.SHA256()))
    server_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,args.host)])
    certificate = (x509.CertificateBuilder().subject_name(server_name).issuer_name(ca.subject).public_key(server_key.public_key())
          .serial_number(x509.random_serial_number()).not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=365))
          .add_extension(x509.SubjectAlternativeName([x509.IPAddress(address)]),critical=False)
          .add_extension(x509.BasicConstraints(ca=False,path_length=None),critical=True)
          .add_extension(x509.SubjectKeyIdentifier.from_public_key(server_key.public_key()),critical=False)
          .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),critical=False)
          .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),critical=False)
          .add_extension(x509.KeyUsage(True,False,True,False,False,False,False,False,False),critical=True)
          .sign(ca_key,hashes.SHA256()))
    for filename,key in [('mcp-ca.key',ca_key),('mcp-server.key',server_key)]:
        (private/filename).write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    (private/'mcp-server.crt').write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    (ROOT/'config/mcp-ca.crt').write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    (private/'mcp-ca.crt').write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    token = secrets.token_urlsafe(48)
    endpoint = f'https://{args.host}:{args.port}/mcp'
    write_json(profile,{'host':args.host,'port':args.port,'allowed_networks':args.allow_network,'tokens':{'handoff-agent':token},
                        'certificate':str(private/'mcp-server.crt'),'private_key':str(private/'mcp-server.key'),
                        'api_credentials':str(private/'agent.json')})
    write_json(private/'mcp-client.json',{'url':endpoint,'bearer_token':token,'ca_file':'mcp-ca.crt','source_id':'development-local'})
    write_json(private/'mcp-client-config.json',{'mcpServers':{'complaint-insights':{'url':endpoint,'headers':{'Authorization':'Bearer '+token}}}})
    public = {'url':endpoint,'transport':'streamable-http','allowed_networks':args.allow_network,
              'ca_certificate':'mcp-ca.crt','ca_sha256':ca.fingerprint(hashes.SHA256()).hex(),
              'server_certificate_sha256':certificate.fingerprint(hashes.SHA256()).hex(),
              'server_certificate_expires_at':certificate.not_valid_after_utc.isoformat(),
              'credentials_file':'.secrets/mcp-client.json'}
    write_json(ROOT/'config/mcp-endpoint.json',public)
    MCPSettings.load(profile)
    print(json.dumps({'status':'PREPARED',**public},ensure_ascii=False))


if __name__=='__main__':
    main()
