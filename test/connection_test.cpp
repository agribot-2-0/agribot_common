/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <gtest/gtest.h>

#include <agribot_common/connection/parsing_strategy/LsbFirstParsingStrategy.h>
#include <agribot_common/connection/parsing_strategy/MsbFirstParsingStrategy.h>

#include <algorithm>
#include <vector>

/*******************************************
 *        Helper functions
 ******************************************/
std::vector<uint8_t> prepareLsbUint16Buffer(uint16_t value)
{
  return std::vector<uint8_t>{ static_cast<uint8_t>(value & 0xFF), static_cast<uint8_t>((value & 0xFF00) >> 8) };
}

std::vector<uint8_t> prepareLsbUint32Buffer(uint32_t value)
{
  return std::vector<uint8_t>{ static_cast<uint8_t>(value & 0xFF), static_cast<uint8_t>((value & 0xFF00) >> 8),
                               static_cast<uint8_t>((value & 0xFF0000) >> 16),
                               static_cast<uint8_t>((value & 0xFF000000) >> 24) };
}

std::vector<uint8_t> prepareLsbUint64Buffer(uint64_t value)
{
  return std::vector<uint8_t>{ static_cast<uint8_t>(value & 0xFF),
                               static_cast<uint8_t>((value & 0xFF00) >> 8),
                               static_cast<uint8_t>((value & 0xFF0000) >> 16),
                               static_cast<uint8_t>((value & 0xFF000000) >> 24),
                               static_cast<uint8_t>((value & 0xFF00000000) >> 32),
                               static_cast<uint8_t>((value & 0xFF0000000000) >> 40),
                               static_cast<uint8_t>((value & 0xFF000000000000) >> 48),
                               static_cast<uint8_t>((value & 0xFF00000000000000) >> 56) };
}

std::vector<uint8_t> prepareLsbStringBuffer(std::string value)
{
  std::vector<uint8_t> buffer;

  for (const auto& c : value)
  {
    buffer.push_back(c);
  }

  return buffer;
}

std::vector<uint8_t> prepareMsbUint16Buffer(uint16_t value)
{
  auto buffer = prepareLsbUint16Buffer(value);
  std::reverse(buffer.begin(), buffer.end());
  return buffer;
}

std::vector<uint8_t> prepareMsbUint32Buffer(uint32_t value)
{
  auto buffer = prepareLsbUint32Buffer(value);
  std::reverse(buffer.begin(), buffer.end());
  return buffer;
}

std::vector<uint8_t> prepareMsbUint64Buffer(uint64_t value)
{
  auto buffer = prepareLsbUint64Buffer(value);
  std::reverse(buffer.begin(), buffer.end());
  return buffer;
}

std::vector<uint8_t> prepareMsbStringBuffer(std::string value)
{
  auto buffer = prepareLsbStringBuffer(value);
  std::reverse(buffer.begin(), buffer.end());
  return buffer;
}

/*******************************************
 *        LsbFirstParsingStrategy
 ******************************************/
TEST(LsbFirstParsingStrategyTest, ParseUint8)
{
  // Prepare data
  uint8_t value = 176;
  auto buffer = std::vector<uint8_t>{ value };

  // Check assertion
  LsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint8(buffer.begin()));
}

TEST(LsbFirstParsingStrategyTest, ParseUint16)
{
  // Prepare data
  uint16_t value = 2137;
  auto buffer = prepareLsbUint16Buffer(value);

  // Check assertion
  LsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint16(buffer.begin()));
}

TEST(LsbFirstParsingStrategyTest, ParseUint32)
{
  // Prepare data
  uint32_t value = 912387;
  auto buffer = prepareLsbUint32Buffer(value);

  // Check assertion
  LsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint32(buffer.begin()));
}

TEST(LsbFirstParsingStrategyTest, ParseUint64)
{
  // Prepare data
  uint64_t value = 324294967296;
  auto buffer = prepareLsbUint64Buffer(value);

  // Check assertion
  LsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint64(buffer.begin()));
}

TEST(LsbFirstParsingStrategyTest, ParseFloat)
{
  // Prepare data
  float value = 4328.432;
  uint32_t byte_value;
  std::memcpy(&byte_value, &value, sizeof(float));
  auto buffer = prepareLsbUint32Buffer(byte_value);

  // Check assertion
  LsbFirstParsingStrategy strategy;
  ASSERT_FLOAT_EQ(value, strategy.getFloat(buffer.begin()));
}

TEST(LsbFirstParsingStrategyTest, ParseDouble)
{
  // Prepare data
  double value = 456.324243543543;
  uint64_t byte_value;
  std::memcpy(&byte_value, &value, sizeof(double));
  auto buffer = prepareLsbUint64Buffer(byte_value);

  // Check assertion
  LsbFirstParsingStrategy strategy;
  ASSERT_DOUBLE_EQ(value, strategy.getDouble(buffer.begin()));
}

TEST(LsbFirstParsingStrategyTest, ParseString)
{
  // Prepare data
  std::string value{ "pattern456!@#" };
  auto buffer = prepareLsbStringBuffer(value);

  // Check assertion
  LsbFirstParsingStrategy strategy;
  ASSERT_STREQ(value.c_str(), strategy.getString(buffer.begin(), buffer.end()).c_str());
}

/*******************************************
 *        MsbFirstParsingStrategy
 ******************************************/
TEST(MsbFirstParsingStrategyTest, ParseUint8)
{
  // Prepare data
  uint8_t value = 176;
  auto buffer = std::vector<uint8_t>{ value };

  // Check assertion
  MsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint8(buffer.begin()));
}

TEST(MsbFirstParsingStrategyTest, ParseUint16)
{
  // Prepare data
  uint16_t value = 2137;
  auto buffer = prepareMsbUint16Buffer(value);

  // Check assertion
  MsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint16(buffer.begin()));
}

TEST(MsbFirstParsingStrategyTest, ParseUint32)
{
  // Prepare data
  uint32_t value = 912387;
  auto buffer = prepareMsbUint32Buffer(value);

  // Check assertion
  MsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint32(buffer.begin()));
}

TEST(MsbFirstParsingStrategyTest, ParseUint64)
{
  // Prepare data
  uint64_t value = 324294967296;
  auto buffer = prepareMsbUint64Buffer(value);

  // Check assertion
  MsbFirstParsingStrategy strategy;
  ASSERT_EQ(value, strategy.getUint64(buffer.begin()));
}

TEST(MsbFirstParsingStrategyTest, ParseFloat)
{
  // Prepare data
  float value = 4328.432;
  uint32_t byte_value;
  std::memcpy(&byte_value, &value, sizeof(float));
  auto buffer = prepareMsbUint32Buffer(byte_value);

  // Check assertion
  MsbFirstParsingStrategy strategy;
  ASSERT_FLOAT_EQ(value, strategy.getFloat(buffer.begin()));
}

TEST(MsbFirstParsingStrategyTest, ParseDouble)
{
  // Prepare data
  double value = 456.324243543543;
  uint64_t byte_value;
  std::memcpy(&byte_value, &value, sizeof(double));
  auto buffer = prepareMsbUint64Buffer(byte_value);

  // Check assertion
  MsbFirstParsingStrategy strategy;
  ASSERT_DOUBLE_EQ(value, strategy.getDouble(buffer.begin()));
}

TEST(MsbFirstParsingStrategyTest, ParseString)
{
  // Prepare data
  std::string value{ "pattern456!@#" };
  auto buffer = prepareMsbStringBuffer(value);

  // Check assertion
  MsbFirstParsingStrategy strategy;
  ASSERT_STREQ(value.c_str(), strategy.getString(buffer.begin(), buffer.end()).c_str());
}

int main(int argc, char** argv)
{
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
