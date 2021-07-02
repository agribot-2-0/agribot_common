/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/TcpSocket.h>

TcpSocket::TcpSocket(std::string ip_address, uint16_t port, uint16_t timeout_ms)
  : ip_address_{ ip_address }, port_{ port }, timeout_ms_{ timeout_ms }
{
  server_address_.sin_addr.s_addr = inet_addr(ip_address_.c_str());
  server_address_.sin_family = AF_INET;
  server_address_.sin_port = htons(port_);
}

void TcpSocket::open()
{
  socket_fd_ = socket(AF_INET, SOCK_STREAM, 0);

  if (socket_fd_ < 0)
  {
    throw std::runtime_error("Failed to create socket");
  }

  if (timeout_ms_ > 0)
  {
    struct timeval tv;
    tv.tv_sec = timeout_ms_ / 1000;
    tv.tv_usec = (timeout_ms_ - 1000 * tv.tv_sec) * 1000;
    setsockopt(socket_fd_, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv));
  }
}

void TcpSocket::close()
{
  ::close(socket_fd_);
}

void TcpSocket::connect()
{
  if (::connect(socket_fd_, (struct sockaddr*)&server_address_, sizeof(server_address_)) != 0)
  {
    throw std::runtime_error("Failed to connect to socket at " + ip_address_ + ":" + std::to_string(port_));
  }
}

void TcpSocket::reconnect()
{
  close();
  open();
  connect();
}

void TcpSocket::read(Buffer& buffer)
{
  ssize_t read_length;
  read_length = recv(socket_fd_, &buffer.buffer_[0], buffer.buffer_.size(), 0);

  if (read_length < 0)
  {
    buffer.clear();
    throw std::runtime_error("[TcpSocket] recv error (read_length < 0)");
  }
  else
  {
    buffer.read_length_ = read_length;
  }
}

void TcpSocket::write(const Buffer& buffer)
{
  // TODO(all) - implement in the future
  static_cast<void>(buffer);
}
