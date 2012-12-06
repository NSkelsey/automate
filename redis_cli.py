import redis
import random
rconn = redis.StrictRedis(host='50.17.215.201', port=6379, db=0, password="reallylongandhardtoguesspassword")
c = "CMDS"


def find_solution(img):
    print 'finding a solution to captcha'
    ps = rconn.pubsub()
    _id = random.randint(0, pow(2,17))
    print _id
    rconn.publish(c, str(_id) + img) # I am listening here for the solution
    ps.subscribe(str(_id))
    solution = ""
    for m in ps.listen():
        if m['type'] == 'message':
            solution = m.get('data')
            break
    print solution
    return solution
