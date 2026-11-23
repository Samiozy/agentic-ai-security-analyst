"""Check whether the own-lab FTP service permits anonymous login; no file access."""
import ftplib
from guardrails.scope import check_target
from schemas.finding import Finding

def check_anonymous_ftp(host: str, port: int=21) -> list[dict]:
    check_target(host,port)
    try:
        # ftplib.FTP(host=...) would connect immediately; connect only AFTER scope check.
        with ftplib.FTP() as ftp:
            ftp.connect(host,port,timeout=4)
            try:
                reply = ftp.login(user="anonymous",passwd="lab-check@example.invalid")
                return [Finding(f"{host}:{port}","anonymous_ftp","anonymous_ftp_enabled",
                    "Anonymous login accepted",reply,"medium").to_dict()]
            except ftplib.error_perm as exc:
                return [Finding(f"{host}:{port}","anonymous_ftp","anonymous_ftp_denied",
                    "Anonymous login refused",str(exc)).to_dict()]
    except (OSError,EOFError,ftplib.all_errors) as exc:
        return [Finding(f"{host}:{port}","anonymous_ftp","ftp_unavailable",
            "FTP check did not complete",str(exc)).to_dict()]
