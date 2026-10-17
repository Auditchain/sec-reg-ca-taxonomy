"""Reg CA filing merkle tree, version 1 (regca:FilingMerkleTreeVersion1Member).

Computes the merkle root of a Reg CA filing held in the LucaSuite JSON format, and checks a chain of filings.

Method
  1. Every fact of the filing is written as a JSON object with the keys
       concept     the concept's full name, namespace + "#" + local name
       entity      the reporting entity, as the filing records it
       period      the period, as the filing records it ("YYYY-MM-DD" or "YYYY-MM-DD | YYYY-MM-DD")
       dimensions  an object: dimension full name -> member full name, or the typed value as a string
       unit        the unit, as the filing records it
       decimals    the rounding, as the filing records it
       value       the value, as the filing records it: a string as it is, a number exactly as written in the
                   filing's JSON text (for example 9.1e-7), not re-formatted
     Keys whose value is empty are left out. Every value is a string (dimensions: an object of strings).
     The full specification is tools/merkle-method-v1.md.
  2. The object is serialized under RFC 8785 (JSON Canonicalization Scheme).
  3. Each leaf is SHA-256(0x00 || canonical JSON), as a leaf hash under RFC 6962.
  4. The leaves are sorted in ascending order of their 32 bytes.
  5. The root is the RFC 6962 Merkle Tree Hash of the sorted leaves:
     interior node = SHA-256(0x01 || left || right), split at the largest power of two smaller than n.
  6. Excluded from the root: the facts of regca:FilingMerkleRoot and regca:FilingMerkleRootMethod, and every fact
     that has a value on regca:FilingAnchorIdentifierTypedAxis (the table of anchors). They are written after the
     root is computed and anchored.

Usage
  python3 regca_merkle.py root  <filing.json>
  python3 regca_merkle.py proof <filing.json> <FactID>      # inclusion proof of one fact
  python3 regca_merkle.py chain <filing1.json> <filing2.json> ...   # in filing order
"""
import hashlib, json, sys

EXCLUDED_CONCEPTS = {'regca:FilingMerkleRoot', 'regca:FilingMerkleRootMethod'}
ANCHOR_AXIS = 'regca:FilingAnchorIdentifierTypedAxis'
SHA = lambda b: hashlib.sha256(b).digest()


def jcs(obj):
    """RFC 8785 for objects whose leaves are strings (the only kind written here): keys sorted by UTF-16 code units,
    no whitespace, UTF-8, non-ASCII characters as they are."""
    def order(o):
        if isinstance(o, dict):
            return {k: order(o[k]) for k in sorted(o, key=lambda k: k.encode('utf-16-be'))}
        return o
    return json.dumps(order(obj), separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def text(v):
    """A fact value as text: a string as it is, a number as written (see load), a boolean as true or false."""
    if v is True or v is False:
        return 'true' if v else 'false'
    return str(v)


def namespaces(model):
    return {b['NamespacePrefix']: b['NamespaceIdentifier'] for b in model['BaseInformation'] if b.get('NamespacePrefix')}


def full(qname, ns):
    if not qname or ':' not in qname:
        return qname
    p, l = qname.split(':', 1)
    return ns.get(p, p) + '#' + l


def canonical_facts(model, include_excluded=False):
    ns = namespaces(model)
    dims = {}
    for d in model.get('Facts-Dimensions', []):
        dims.setdefault(d['FactID'], []).append(d)
    out = []
    for f in model.get('Facts', []):
        fd = dims.get(f['FactID'], [])
        if not include_excluded and (f['ConceptAspect'] in EXCLUDED_CONCEPTS or any(d['Dimension'] == ANCHOR_AXIS for d in fd)):
            continue
        o = {'concept': full(f['ConceptAspect'], ns), 'entity': f.get('ReportingEntityAspect', ''),
             'period': f.get('CalendarPeriodAspect', ''), 'unit': f.get('Units', ''), 'decimals': f.get('Rounding', ''),
             'value': '' if f.get('FactValue') is None else text(f['FactValue'])}
        if fd:
            o['dimensions'] = {full(d['Dimension'], ns): (full(d['Member'], ns) if d.get('Member') else text(d['Value']))
                               for d in fd}
        o = {k: v for k, v in o.items() if v not in ('', {}, None)}
        out.append((f['FactID'], o))
    return out


def leaf(o):
    return SHA(b'\x00' + jcs(o))


def mth(leaves):
    n = len(leaves)
    if n == 0:
        return SHA(b'')
    if n == 1:
        return leaves[0]
    k = 1
    while k * 2 < n:
        k *= 2
    return SHA(b'\x01' + mth(leaves[:k]) + mth(leaves[k:]))


def root(model):
    leaves = sorted(leaf(o) for _, o in canonical_facts(model))
    return mth(leaves).hex(), len(leaves)


def proof(model, fact_id):
    """RFC 6962 audit path for one fact: list of (side, hash) from the leaf up."""
    facts = canonical_facts(model)
    leaves = sorted(leaf(o) for _, o in facts)
    target = leaf(dict(facts)[fact_id])
    m = leaves.index(target)
    path = []

    def walk(lv, m):
        n = len(lv)
        if n == 1:
            return
        k = 1
        while k * 2 < n:
            k *= 2
        if m < k:
            walk(lv[:k], m)
            path.append(('right', mth(lv[k:]).hex()))
        else:
            walk(lv[k:], m - k)
            path.append(('left', mth(lv[:k]).hex()))
    walk(leaves, m)
    return target.hex(), path


def verify_proof(leaf_hex, path, root_hex):
    h = bytes.fromhex(leaf_hex)
    for side, sib in path:
        s = bytes.fromhex(sib)
        h = SHA(b'\x01' + (s + h if side == 'left' else h + s))
    return h.hex() == root_hex


def fact_value(model, concept):
    v = [f['FactValue'] for f in model.get('Facts', []) if f['ConceptAspect'] == concept]
    return v[0] if v else None


class Literal(str):
    """A JSON number kept as the text written in the file."""


def load(path):
    """Read a filing, keeping every number as the text written in the file (the method takes numbers as written)."""
    return json.load(open(path, encoding='utf-8'), parse_float=Literal, parse_int=Literal)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'root':
        m = load(sys.argv[2])
        r, n = root(m)
        print(r, n, 'facts', 'reported:', fact_value(m, 'regca:FilingMerkleRoot'))
    elif cmd == 'proof':
        m = load(sys.argv[2])
        lh, p = proof(m, sys.argv[3])
        r, _ = root(m)
        print(json.dumps({'leaf': lh, 'path': p, 'root': r, 'verifies': verify_proof(lh, p, r)}, indent=1))
    elif cmd == 'chain':
        prev = prev_date = None
        for p in sys.argv[2:]:
            m = load(p)
            r, n = root(m)
            rep = fact_value(m, 'regca:FilingMerkleRoot')
            link = fact_value(m, 'regca:PreviousFilingMerkleRoot')
            link_date = fact_value(m, 'regca:PreviousFilingDate')
            if prev is None and link is None:
                state = '(first)'
            elif link == prev and link_date == prev_date:
                state = 'ok'
            else:
                state = f'BROKEN (reports {link} of {link_date})'
            print(f'{p}: root {r} ({n} facts) reported {"ok" if rep == r else "MISMATCH " + str(rep)}; previous {state}')
            prev, prev_date = r, fact_value(m, 'regca:DocumentDate')
