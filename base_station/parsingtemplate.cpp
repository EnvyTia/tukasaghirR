#include <fstream>
#include <iostream>
#include <vector>
#include <nlohmann/json.hpp>  // external json parser

using json = nlohmann::json;

// parsing file output HNNS
std::vector<std::vector<int>> LoadRbAllocation(const std::string& filename)
{
    std::ifstream file(filename);
    json j;
    file >> j;
    return j["rb_allocation"].get<std::vector<std::vector<int>>>();
}
