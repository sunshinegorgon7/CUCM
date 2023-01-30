#!/usr/bin/python3

import paramiko
from paramiko_expect import SSHClientInteraction
import sys, traceback
from shutil import copyfile

def main():

        UNKNOWN = 3
        OK = 0
        WARNING = 1
        CRITICAL = 2

        PUB = "1.1.1.1"
        SUB = "2.2.2.2"
        un = "readuser"
        pw = "readuserpass"
        PROMPT = "admin:"

        try:
                with open('/usr/local/nagios/libexec/check_sip/pub_sip_status','w') as pss:
                        client = paramiko.SSHClient()
                        client.load_system_host_keys()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(hostname=PUB,
                                                username=un, password=pw)
                        with SSHClientInteraction(client, timeout=60, display=False) as interact:
                                                interact.expect(PROMPT)
                                                interact.send('show risdb query sip')
                                                interact.expect(PROMPT, timeout=20)
                                                cmd_output_ls = interact.current_output_clean
                        client.close()
                        pss.write(cmd_output_ls)
                copyfile('/usr/local/nagios/libexec/check_sip/pub_sip_status','/usr/local/nagios/libexec/check_sip/pub_sip_status_nagios')

                with open('/usr/local/nagios/libexec/check_sip/sub_sip_status','w') as sss:
                        client.connect(hostname=SUB,
                                                username=un, password=pw)
                        with SSHClientInteraction(client, timeout=60, display=False) as interact:
                                                interact.expect(PROMPT)
                                                interact.send('show risdb query sip')
                                                interact.expect(PROMPT, timeout=20)
                                                cmd_output_ls = interact.current_output_clean
                        client.close()
                        sss.write(cmd_output_ls)
                copyfile('/usr/local/nagios/libexec/check_sip/sub_sip_status','/usr/local/nagios/libexec/check_sip/sub_sip_status_nagios')

        except Exception:
                traceback.print_exc()

if __name__ == '__main__':
        main()
