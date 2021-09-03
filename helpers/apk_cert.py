#!/usr/bin/env python3

import subprocess

KEYTOOL_PATH = 'keytool'

def get_sha256_cert_fingerprint(apk):
    apk_cert = subprocess.Popen(
        KEYTOOL_PATH + ' -printcert -jarfile ' + apk, shell=True, stdout=subprocess.PIPE
    ).stdout.read().decode()
    return apk_cert.split('SHA256: ')[1].split('\n')[0]