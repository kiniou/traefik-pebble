import re
import sys
import dns.resolver
import dns.name

def init(_id, cfg):
    return True


def deinit(_id):
    return True


def inform_super(_id, qstate, superqstate, qdata):
    return True


def get_traefik_ip(qstate):
    ip_address = None
    resolver = dns.resolver.Resolver(configure=True)
    resolver.timeout = 1
    resolver.lifetime = 1
    qname = dns.name.from_text('traefik')
    result = resolver.query(qname,raise_on_no_answer=False)
    if result.rrset:
        ip_address = next(iter([ip.address for ip in result.rrset.items]))
    return ip_address


def operate(_id, event, qstate, qdata):
    if (event == MODULE_EVENT_NEW) or (event == MODULE_EVENT_PASS):
        msg = DNSMessage(qstate.qinfo.qname_str, RR_TYPE_A, RR_CLASS_IN, PKT_QR | PKT_RA | PKT_AA)
        ip_address = get_traefik_ip(qstate)

        if ip_address is not None:
            # append RR
            if (qstate.qinfo.qtype == RR_TYPE_A) or (qstate.qinfo.qtype == RR_TYPE_ANY):
                msg.answer.append("%s 10 IN A %s" % (qstate.qinfo.qname_str, ip_address))

            # set qstate.return_msg
            if not msg.set_return_msg(qstate):
                qstate.ext_state[id] = MODULE_ERROR
                return True

            #we don't need validation, result is valid
            qstate.return_msg.rep.security = 2

            qstate.return_rcode = RCODE_NOERROR
            qstate.ext_state[_id] = MODULE_FINISHED
            return True
        else:  # Pass on the unknown query to the iterator
            log_info("Could not find ip for %s",
                        qstate.qinfo.qname_str)
            qstate.ext_state[_id] = MODULE_WAIT_MODULE
            return True

    elif event == MODULE_EVENT_MODDONE:  # the iterator has finished
        # we don't need modify result
        qstate.ext_state[_id] = MODULE_FINISHED
        return True

    log_err("pythonmod: Unknown event")
    qstate.ext_state[_id] = MODULE_ERROR
    return True
