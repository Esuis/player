#include <stdlib.h>
#include <iostream>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <errno.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <netinet/in.h>
#include <netinet/ip6.h>
#include <linux/ipv6.h>
#include <arpa/inet.h>
#include <fstream>
#include <byteswap.h>
#include <sstream>

using namespace std;

class HBH
{
public:

    // ip, file path
    string serverIP;
    string request_path;

    // port, ip
    int port;
    char ip[128];

    void* svraddr = NULL;
    int error = -1, svraddr_len;
    int ret = 0;
    int m_sock = 0;
    struct sockaddr_in6 svraddr_6;

    struct addrinfo* result;

    const struct sockaddr* sa;
    socklen_t maxlen = 128;

    string interfaceName;

    //HBH defination variable
    void* extbuf;
    socklen_t extlen;
    int currentlen;
    void* databuf;
    int offset;
    
    int option_type;

    char* apn_value1_char;
    char* apn_value2_char;
    char* apn_value3_char;

    int apn_value1;
    int apn_value2;
    int apn_value3;

    string myrequest;

    int statusCode;

    // save file
    char buffer[4096];
    ssize_t bytesRead;
    bool headerEnded = false;
    string output_path;



    // interface_name, IP, port, option type, 64 bit apn value, request file path, output file path
    HBH(char* interfaceName, char* serverIP, int port, int option_type, char* apn_value1, char* apn_value2, char* apn_value3, char* request_path, char* output_path){
        this->interfaceName = interfaceName;
        this->serverIP = serverIP;
        this->port = port;
        this->option_type = option_type;
        this->apn_value1_char = apn_value1;
        this->apn_value2_char = apn_value2;
        this->apn_value3_char = apn_value3;
        this->request_path = request_path;
        this->output_path = output_path;

    }


    int operator()(){

        // printf("v11\n");
        memset(ip, 0, sizeof(ip));
        strcpy(ip, serverIP.c_str());
        error = getaddrinfo(ip, NULL, NULL, &result);
        if(error < 0){
            perror("getaddrinfo error");
        }
        sa = result->ai_addr;
        
        if ((m_sock = socket(AF_INET6, SOCK_STREAM, 0)) < 0) {
            perror("socket create failed");
            ret = -1;
        }
        // set ip

        /* Estimate the length */
        currentlen = inet6_opt_init(NULL, 0);
        if (currentlen == -1)
            return (-1);
        // printf("Hop by Hop length_init: %d\n", currentlen);

        currentlen = inet6_opt_append(NULL, 0, currentlen, option_type, 12, 4, NULL);
        if (currentlen == -1)
            return (-1);
        // printf("Hop by Hop length_append: %d\n", currentlen);

        currentlen = inet6_opt_finish(NULL, 0, currentlen);
        if (currentlen == -1)
            return (-1);
        // printf("Hop by Hop length_finish: %d\n", currentlen);

        extlen = currentlen;
        extbuf = malloc(extlen);

        if (extbuf == NULL) {
            perror("malloc");
            return (-1);
        }
        currentlen = inet6_opt_init(extbuf, extlen);
        if (currentlen == -1)
            return (-1);
        // printf("currentlen_init:%d\n", currentlen);
        // printf("extlen:%d\n", extlen);
        // 此处databuf已经与extbuf产生联系
        currentlen = inet6_opt_append(extbuf, extlen, currentlen, option_type, 12, 4, &databuf);
        if (currentlen == -1)
            return (-1);
        // printf("currentlen_append:%d\n", currentlen);

        //此处开始需要重复设置，才能更新
        /* Insert apn_value for 8-octet field */

        apn_value1 = std::strtol(apn_value1_char, nullptr, 0);
        apn_value2 = std::strtol(apn_value2_char, nullptr, 0);
        apn_value3 = std::strtol(apn_value3_char, nullptr, 0);
        // std::cout << "apn_char_1" << apn_value1_char << std::endl;
        // std::cout << "apn_char_2" << apn_value2_char << std::endl;
        // std::cout << "apn_char_3" << apn_value3_char << std::endl;
        // std::cout << "Hex value 1: " << std::hex << apn_value1 << std::endl;
        // std::cout << "Hex value 2: " << std::hex << apn_value2 << std::endl;
        // std::cout << "Hex value 3: " << std::hex << apn_value3 << std::endl;

        offset = 0;
        apn_value1 = bswap_32(apn_value1);
        apn_value2 = bswap_32(apn_value2);
        apn_value3 = bswap_32(apn_value3);
        offset = inet6_opt_set_val(databuf, offset, &apn_value1, sizeof(apn_value1));
        offset = inet6_opt_set_val(databuf, offset, &apn_value2, sizeof(apn_value2));
        offset = inet6_opt_set_val(databuf, offset, &apn_value3, sizeof(apn_value3));
        currentlen = inet6_opt_finish(extbuf, extlen, currentlen);
        // printf("currentlen_finish: %d\n", currentlen);
        if (currentlen == -1)
            return (-1);
        /* extbuf and extlen are now completely formatted */

        // set network interface
        setsockopt(m_sock, SOL_SOCKET, SO_BINDTODEVICE, interfaceName.c_str(), interfaceName.size());
        setsockopt(m_sock, IPPROTO_IPV6, IPV6_HOPOPTS, extbuf, currentlen);
        inet_ntop(AF_INET6, &(((struct sockaddr_in6*)sa)->sin6_addr), ip, maxlen);
        // printf("socket created ipv6\n");
        
        // set socket struct
        bzero(&svraddr_6, sizeof(svraddr_6));
        svraddr_6.sin6_family = AF_INET6;
        svraddr_6.sin6_port = htons(port);
        if (inet_pton(AF_INET6, ip, &svraddr_6.sin6_addr) < 0) {
            perror(ip);
            ret = -1;
        }
        svraddr_len = sizeof(svraddr_6);
        svraddr = &svraddr_6;
        freeaddrinfo(result);
        if (ret != 0)
        {
            fprintf(stderr, "Cannot Connect the server!n");
            return -1;
        }
        // set socket struct

        // socket connect
        error = connect(m_sock, (struct sockaddr*)svraddr, svraddr_len);
        if (error == -1)
        {
            perror("connect");
            return -1;
        }
        // printf("connect success!\n");
        // socket connect

        myrequest = "GET " + request_path + " HTTP/1.1\r\n"
                    "Host: [" + serverIP + "]\r\n"
                    "Connection: close\r\n"
                    "\r\n";
        
        if (send(m_sock, myrequest.c_str(), myrequest.length(), 0) < 0) {
            cerr << "Failed to send the request." << endl;
            return 1;
        }

        ofstream outputFile(output_path, ios::binary);
        if (!outputFile) {
            cerr << "Failed to create output file." << endl;
            return 1;
        }

        
        while ((bytesRead = recv(m_sock, buffer, sizeof(buffer), 0)) > 0) {
            if (!headerEnded) {
                string response(buffer, bytesRead);
                size_t headerEndPos = response.find("\r\n\r\n");
                if (headerEndPos != string::npos) {
                    // 响应头结束，写入返回体部分到文件
                    headerEnded = true;
                    bytesRead -= static_cast<ssize_t>(headerEndPos) + 4;
                    outputFile.write(buffer + headerEndPos + 4, bytesRead);
                    // 解析响应头状态码
                    string header = response.substr(0, headerEndPos);
                    istringstream iss(header);
                    string line;
                    while (getline(iss, line)) {
                        if (line.substr(0, 5) == "HTTP/") {
                            istringstream statusLine(line);
                            string httpVersion;
                            string statusMessage;
                            statusLine >> httpVersion >> statusCode >> statusMessage;
                            break;
                        }
                    }
                }
            } else {
                // 写入返回体部分到文件
                outputFile.write(buffer, bytesRead);
            }
        }

        outputFile.close();
        // cout << "response ok" << endl;
        // cout << "status:" << statusCode << endl;

        // close connect
        close(m_sock);
        // close connect
        
        return statusCode;

    }
};
