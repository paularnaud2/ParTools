def get_confidential(decrypt_key='', raise_e=True):
    import os.path as p
    import partools as pt

    from . import g
    from .log import log
    from .string import like
    from .file import load_txt
    from .tools import list_to_dict

    if not p.exists(pt.cfg.CFI_PATH):
        log(g.E_CFI)
        if raise_e:
            raise Exception(g.E_CFI)
        else:
            return False
    cfi_list = load_txt(pt.cfg.CFI_PATH)
    cfi = list_to_dict(cfi_list)

    if decrypt_key:
        from cryptography.fernet import Fernet
        fernet = Fernet(decrypt_key)

    for key in cfi:
        v = cfi[key]
        m = like(v, "ENCRYPTED[*]")
        if m and decrypt_key:
            message = m.group(1).encode()
            cfi[key] = fernet.decrypt(message).decode()

    return cfi
