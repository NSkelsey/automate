from boto.ec2.connection import EC2Connection
import boto
from time import sleep
from fabric.api import *
from datetime import datetime

UV_URL = "http://speakupuva.uservoice.com/forums/11875-speakupuva/suggestions/3249267-towels-in-bathrooms-to-replace-paper-towels"
ami_id = "ami-c3a222aa" #selenebox3

def reset_ip(instance):
    pass


def launch_fleet(conn, num):
    print "launching %s instances" % num
    reservation = conn.run_instances(ami_id, instance_type="t1.micro", min_count=num, max_count=num, key_name='mbk6wm')
    print "reservation id: %s" % reservation.id
    sleep(5)
    for i in reservation.instances:
        print "\tId: %s, State: %s" % (i.id, i.state)
    print "Instances launched: %s" % num
    return reservation

def stop_fleet(conn, reservation=None):
    if reservation is not None:
        print "stopping %s" % (str(reservation.instances))
        reservation.stop_all()
        for ins in reservation.instances:
            ins.terminate()
        sleep(5)
        for ins in reservation.instances:
            print "\t id: %s state: %s" % (ins.id, ins.state)
    else:
        print "no reservation given stopping all with ami-id: %s" % ami_id
        counter = 0
        for reservs in conn.get_all_instances():
            for ins in reservs.instances:
                if ins.state == "running" and ins.image_id == ami_id:
                    print "\tterminating id: %s" % ins.id
                    ins.terminate()
                    counter += 1
        print "Instances killed %s " % counter

#ensures hosts are up
def make_host_list(instances):
    li = []
    for ins in instances:
        ins.update()
        ctr = 1
        while ins.state != 'running' and ins.ip_address is None:
                print "\tWaiting on %s State: %s" % (ins.id, ins.state)
                sleep(10)
                ins.update()
                ctr += 1
                if ctr > 6:
                    print "instance dead"
                    break
        if ctr > 6:
            break
        s = "ubuntu@" + ins.ip_address
        li.append(s)
    return li

@task
@parallel
def uname():
    run("uname -s")

@task
@parallel
def change_drive_by():
    run("nohup Xvfb :15 -ac -screen 0 1024x768x8 &", pty=False)
    sleep(3)
    url = UV_URL
    type = "uv"
    numIterations = 5
    with settings(warn_only=True):
        run("export DISPLAY=:15; python ~/automate/seleneuv.py %s %s %s" % (url, numIterations, type))

@task
@parallel
def update_repo():
    run("rm -rf ~/automate")
    run("git clone --quiet https://github.com/NSkelsey/automate.git")

def run_fabric(conn, instances, func):
    host_str = make_host_list(r.instances)
    print host_str
    env.hosts = host_str
    env.key_filename = '/home/ubuntu/.ssh/blog.pem'
    ################################################
    #env.key_filename = '/Users/skelsey/.ssh/blog.pem'
    execute(func)

def tally_states(conn):
    dct = {}
    li = conn.get_all_instance_status()
    for stats in li:
        if dct.get(stats.state_name) is None:
            dct[stats.state_name] = 1
        else:
            i = dct.get(stats.state_name)
            dct[stats.state_name] = i + 1
    print dct

#####################################
# REVIEW MAIN BEFORE RUNNING DAMNIT #
#####################################
if __name__ == "__main__":

    conn = EC2Connection('AKIAIERYI27USRA2RILQ', 'bx65KNYwzfcqlUUxGcXrG935DGh4BsBkPwFtcMKf')
    ####################################
    #conn = boto.connect_ec2()

    for i in range(7):
        if (i != -1):
            r = launch_fleet(conn, 5) # launches x number of instances
            sleep(120) # inorder to give amazon time to think
        else:
            r = conn.get_all_instances()[-1] #helpful to get last reservation lauched  
        print datetime.now()          

        print "="*50
        print "Doing stuff with instances"

        run_fabric(conn, r.instances, uname)
        run_fabric(conn, r.instances, update_repo)
        run_fabric(conn, r.instances, change_drive_by)
        
        sleep(2)
        print datetime.now()
        print "="*50
        print "Stopping...."

        stop_fleet(conn,r) # without r it will stop all instances with ami-id
        tally_states(conn) # will state how many instances are in an active state
        print "Sleeping"
    stop_fleet(conn,)
    tally_states(conn)

