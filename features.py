import math, collections
from collections import deque, defaultdict

def entropy(s):
    if not s: return 0.0
    c = collections.Counter(s)
    n = len(s)
    return -sum((v/n) * math.log2(v/n) for v in c.values())

QTYPES = {1: 0, 28: 1, 16: 2, 10: 3, 5: 4, 15: 5}   # A, AAAA, TXT, NULL, CNAME, MX

class ClientWindow:
    """Keeps the last N query timestamps per client for timing features."""
    def __init__(self, n=10):
        self.w = defaultdict(lambda: deque(maxlen=n))
    def update(self, client, ts):
        d = self.w[client]
        d.append(ts)
        if len(d) < 2:
            return 0.0, 1
        gaps = [d[i+1] - d[i] for i in range(len(d)-1)]
        return sum(gaps) / len(gaps), len(d)

def extract(qname, qtype, ts, client, win, resp_len=0):
    name = qname.rstrip(".").lower()
    labels = name.split(".")
    sub = ".".join(labels[:-2]) if len(labels) > 2 else labels[0]
    mean_gap, wcount = win.update(client, ts)
    letters = sum(ch.isalpha() for ch in sub)
    digits = sum(ch.isdigit() for ch in sub)
    return {
        "name_len": len(name),
        "sub_len": len(sub),
        "n_labels": len(labels),
        "max_label_len": max(len(l) for l in labels),
        "entropy": entropy(sub),
        "digit_ratio": digits / max(len(sub), 1),
        "unique_ratio": len(set(sub)) / max(len(sub), 1),
        "vowel_ratio": sum(ch in "aeiou" for ch in sub) / max(letters, 1),
        "qtype": QTYPES.get(qtype, 9),
        "mean_gap": mean_gap,
        "win_count": wcount,
        "resp_len": resp_len,
    }

FEATURE_NAMES = ["name_len", "sub_len", "n_labels", "max_label_len", "entropy",
                 "digit_ratio", "unique_ratio", "vowel_ratio", "qtype",
                 "mean_gap", "win_count", "resp_len"]
