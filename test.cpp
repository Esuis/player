#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <ifaddrs.h>

bool isGlobalAddress(const struct in6_addr& addr) {
    // 检查 IPv6 地址是否为全局地址
    return (addr.s6_addr[0] & 0xF0) == 0x20;
}

int main() {
    const int port = 80; // 替换为目标端口号

    // 获取本机固定 IPv6 地址
    struct ifaddrs *ifaddr, *ifa;
    if (getifaddrs(&ifaddr) == -1) {
        std::cerr << "Failed to get network interface addresses" << std::endl;
        return 1;
    }

    struct in6_addr localIpv6Address{};
    for (ifa = ifaddr; ifa != nullptr; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == nullptr || ifa->ifa_addr->sa_family != AF_INET6)
            continue;
        struct sockaddr_in6 *sa = reinterpret_cast<struct sockaddr_in6 *>(ifa->ifa_addr);
        if (isGlobalAddress(sa->sin6_addr)) {
            memcpy(&localIpv6Address, &(sa->sin6_addr), sizeof(struct in6_addr));
            break;
        }
    }
    freeifaddrs(ifaddr);

    if (IN6_IS_ADDR_UNSPECIFIED(&localIpv6Address)) {
        std::cerr << "Failed to find a global IPv6 address" << std::endl;
        return 1;
    }

    // 创建 IPv6 socket
    int sockfd = socket(AF_INET6, SOCK_STREAM, 0);
    if (sockfd == -1) {
        std::cerr << "Failed to create socket" << std::endl;
        return 1;
    }

    // 设置目标地址
    struct sockaddr_in6 serverAddr{};
    serverAddr.sin6_family = AF_INET6;
    serverAddr.sin6_port = htons(port);
    serverAddr.sin6_addr = localIpv6Address;

    // 绑定本地地址
    if (bind(sockfd, reinterpret_cast<const sockaddr*>(&serverAddr), sizeof(serverAddr)) == -1) {
        std::cerr << "Failed to bind to local address" << std::endl;
        close(sockfd);
        return 1;
    }

    // 连接到目标地址
    if (connect(sockfd, reinterpret_cast<const sockaddr*>(&serverAddr), sizeof(serverAddr)) == -1) {
        std::cerr << "Failed to connect" << std::endl;
        close(sockfd);
        return 1;
    }

    // 连接成功，可以进行后续操作

    // 关闭 socket
    close(sockfd);

    return 0;
}
