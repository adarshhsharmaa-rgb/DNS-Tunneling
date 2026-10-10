import socket, random, time, sys

domains = [l.strip() for l in open(sys.argv[1]) if l.strip()]
for _ in range(4000):
    d = random.choice(domains)
    try:
        socket.gethostbyname(d)
        if random.random() < 0.3:
            socket.gethostbyname("www." + d)   # extra realistic variety
    except Exception:
        pass
    time.sleep(random.uniform(0.001, 0.01))
