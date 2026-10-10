from dnslib import DNSRecord, QTYPE, RR, TXT, A
from dnslib.server import DNSServer, BaseResolver
import random, string

class R(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        q = request.q
        if q.qtype == QTYPE.TXT:
            data = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(40, 180)))
            reply.add_answer(RR(q.qname, QTYPE.TXT, rdata=TXT(data), ttl=0))
        else:
            reply.add_answer(RR(q.qname, QTYPE.A, rdata=A("10.0.0.1"), ttl=0))
        return reply

DNSServer(R(), port=5353, address="127.0.0.1").start()
