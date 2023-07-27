#include "include/ipv6_HBH.h"

using namespace std;

extern "C" int add_HBH(char* interfaceName, char* serverIP, int port, int option_type, char* apn_value1, char* apn_value2, char* request_path, char* output_path){

    int statusCode;
    HBH hbh(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, request_path, output_path);
    statusCode = hbh();
    return statusCode;

}