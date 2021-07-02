/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/ISocket.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <strings.h>

#include <cstdint>
#include <stdexcept>
#include <string>

class TcpSocket : public ISocket
{
private:
  int socket_fd_;
  struct sockaddr_in server_address_;
  std::string ip_address_;
  uint16_t port_;
  uint16_t timeout_ms_;

public:
  TcpSocket(std::string ip_address, uint16_t port, uint16_t timeout_ms);
  ~TcpSocket() = default;
  void open() override;
  void close() override;
  void connect() override;
  void reconnect() override;
  void read(Buffer& buffer) override;
  void write(const Buffer& buffer) override;
};
