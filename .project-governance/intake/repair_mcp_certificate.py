"""Repair the first, not-yet-handed-off certificate's RFC5280 extensions.

Keep private keys and access tokens unchanged; preserve failed public evidence.
"""
from pathlib import Path
import json
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization

root=Path(__file__).resolve().parents[2]
private=root/'.secrets'
backup=root/'.runtime/tls-before-repair'
backup.mkdir(exist_ok=True)
ca_path=root/'config/mcp-ca.crt'
server_path=private/'mcp-server.crt'
ca=x509.load_pem_x509_certificate(ca_path.read_bytes())
server=x509.load_pem_x509_certificate(server_path.read_bytes())
ca_key=serialization.load_pem_private_key((private/'mcp-ca.key').read_bytes(),password=None)
server_key=serialization.load_pem_private_key((private/'mcp-server.key').read_bytes(),password=None)
for path in [ca_path,server_path,root/'config/mcp-endpoint.json']:
    destination=backup/path.name
    if destination.exists(): raise ValueError('refusing to overwrite first failed certificate evidence')
    destination.write_bytes(path.read_bytes())

def repaired(certificate,key,issuer_key):
    builder=(x509.CertificateBuilder().subject_name(certificate.subject).issuer_name(certificate.issuer)
             .public_key(key.public_key()).serial_number(x509.random_serial_number())
             .not_valid_before(certificate.not_valid_before_utc).not_valid_after(certificate.not_valid_after_utc))
    for extension in certificate.extensions:
        if not isinstance(extension.value,(x509.SubjectKeyIdentifier,x509.AuthorityKeyIdentifier)):
            builder=builder.add_extension(extension.value,critical=extension.critical)
    return (builder.add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()),critical=False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(issuer_key.public_key()),critical=False)
            .sign(issuer_key,hashes.SHA256()))

ca=repaired(ca,ca_key,ca_key)
server=repaired(server,server_key,ca_key)
for path in [ca_path,private/'mcp-ca.crt']:
    path.write_bytes(ca.public_bytes(serialization.Encoding.PEM))
server_path.write_bytes(server.public_bytes(serialization.Encoding.PEM))
endpoint=json.loads((root/'config/mcp-endpoint.json').read_text(encoding='utf-8'))
endpoint['ca_sha256']=ca.fingerprint(hashes.SHA256()).hex()
endpoint['server_certificate_sha256']=server.fingerprint(hashes.SHA256()).hex()
(root/'config/mcp-endpoint.json').write_text(json.dumps(endpoint,indent=2),encoding='utf-8')
print(json.dumps({'status':'CERTIFICATES_REPAIRED','ca_sha256':endpoint['ca_sha256'],'server_certificate_sha256':endpoint['server_certificate_sha256']}))
