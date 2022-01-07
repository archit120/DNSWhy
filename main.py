from network import *

def create_simple_query(target_domain: str, recursion = False, id=1):
    return Message(Header(id, 0, 0, 0, 0, recursion, 0, 0, 0, 1, 0, 0, 0), 
        [Question(target_domain, QType.A, QClass.IN)], [], [], [])

def resolve(target_domain: str, server: str, root_server = "198.41.0.4") :
    print("Asking {0} for {1}".format(server, target_domain))
    reply = send_receive_message(server, create_simple_query(target_domain))
    if len(reply.answers):

        print("Found answers for target domain. Total {0} answers found".format(len(reply.answers)))
        ipAddresses = []
        alias = None
        for answer in reply.answers:
            if isinstance(answer.rData, ARData):
                ipAddresses.append(answer.rData.ipAddress)
            else:
                alias = answer.rData.alias
            
        if len(ipAddresses) > 0:
            print("Answer found!")
            print("\n".join(ipAddresses))
            return ipAddresses
        
        print("Found a CNAME record. Reasking root server for the new alias")
        return resolve(alias, root_server)
    else:
        print("No answer records found. Looking at authoritative records")
        authority_records = {}
        for authority in reply.authority:
            if hasattr(authority.rData, 'namespace'):
                authority_records[authority.rData.namespace] = None
        for additional in reply.additional:
            if hasattr(additional.rData, 'ipAddress') and additional.name in authority_records:
                authority_records[additional.name] = additional.rData.ipAddress
        print("Found {0} valid authoritative servers. Re-querying the first one with IP present".format(len(authority_records)))
        for key, val in authority_records.items():
            if val is not None:
                print("Name: {0}, IP: {1}".format(key, val))
                return resolve(target_domain, val)
        
        print("IP for none of the authoritative servers included in additional records. Querying for its IP first")
        key = list(authority_records.keys())[0]
        ipServer = resolve(key, root_server)[0]
        return resolve(target_domain, ipServer)


if __name__ == "__main__":
    server = "198.41.0.4"
    target_domain = "www.facebook.com"
    message = resolve(target_domain, server)
    
