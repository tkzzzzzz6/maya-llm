#!/usr/bin/env python3
"""
生成自签名 SSL 证书
用于开发和测试环境
生产环境请使用 Let's Encrypt 或购买正式证书
"""

from OpenSSL import crypto
import os

def generate_self_signed_cert(
    cert_dir="./ssl_config/certs",
    cert_file="server.crt",
    key_file="server.key",
    days_valid=365,
    country="CN",
    state="Beijing",
    city="Beijing",
    organization="MAYA-LLM",
    common_name="localhost"
):
    """
    生成自签名证书
    
    参数:
        cert_dir: 证书保存目录
        cert_file: 证书文件名
        key_file: 私钥文件名
        days_valid: 证书有效期（天）
        country: 国家代码
        state: 省/州
        city: 城市
        organization: 组织名称
        common_name: 域名或IP（重要！）
    """
    
    # 创建目录
    os.makedirs(cert_dir, exist_ok=True)
    
    # 生成密钥对
    print("🔑 正在生成 RSA 密钥对...")
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    
    # 生成证书
    print("📜 正在生成自签名证书...")
    cert = crypto.X509()
    cert.get_subject().C = country
    cert.get_subject().ST = state
    cert.get_subject().L = city
    cert.get_subject().O = organization
    cert.get_subject().CN = common_name
    
    # 添加 SAN (Subject Alternative Name) 扩展
    # 支持多个域名/IP
    san_list = [
        b"DNS:localhost",
        b"DNS:127.0.0.1",
        b"IP:127.0.0.1",
        b"IP:0.0.0.0",
    ]
    
    # 如果 common_name 不是 localhost，添加到 SAN
    if common_name != "localhost":
        san_list.append(f"DNS:{common_name}".encode())
        # 如果是 IP 地址
        if common_name.replace('.', '').isdigit():
            san_list.append(f"IP:{common_name}".encode())
    
    cert.add_extensions([
        crypto.X509Extension(b"subjectAltName", False, b",".join(san_list)),
        crypto.X509Extension(b"basicConstraints", True, b"CA:FALSE"),
        crypto.X509Extension(b"keyUsage", True, b"digitalSignature,keyEncipherment"),
        crypto.X509Extension(b"extendedKeyUsage", True, b"serverAuth"),
    ])
    
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(days_valid * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    
    # 保存证书和私钥
    cert_path = os.path.join(cert_dir, cert_file)
    key_path = os.path.join(cert_dir, key_file)
    
    print(f"💾 保存证书到: {cert_path}")
    with open(cert_path, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    print(f"💾 保存私钥到: {key_path}")
    with open(key_path, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    
    print("\n" + "="*60)
    print("✅ SSL 证书生成成功！")
    print("="*60)
    print(f"📁 证书文件: {cert_path}")
    print(f"🔐 私钥文件: {key_path}")
    print(f"⏰ 有效期: {days_valid} 天")
    print(f"🌐 域名/IP: {common_name}")
    print("\n⚠️  这是自签名证书，浏览器会显示安全警告")
    print("   开发环境可以忽略警告并继续")
    print("   生产环境请使用 Let's Encrypt 或购买正式证书")
    print("="*60)
    
    return cert_path, key_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='生成自签名 SSL 证书')
    parser.add_argument('--domain', default='localhost', help='域名或IP地址 (默认: localhost)')
    parser.add_argument('--days', type=int, default=365, help='有效期天数 (默认: 365)')
    parser.add_argument('--org', default='MAYA-LLM', help='组织名称')
    
    args = parser.parse_args()
    
    print("="*60)
    print("🔒 SSL 证书生成工具")
    print("="*60)
    print(f"📍 域名/IP: {args.domain}")
    print(f"⏰ 有效期: {args.days} 天")
    print(f"🏢 组织: {args.org}")
    print("="*60 + "\n")
    
    generate_self_signed_cert(
        common_name=args.domain,
        days_valid=args.days,
        organization=args.org
    )

