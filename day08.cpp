#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>

#define WIDTH 25
#define HEIGHT 6

size_t part_a(const std::vector<int>& nums)
{
    size_t num_layers = nums.size() / WIDTH / HEIGHT;
    std::vector<std::vector<size_t>> num_counts_per_layer;
    num_counts_per_layer.resize(num_layers);
    for (auto& counts : num_counts_per_layer)
    {
        counts.resize(10);
    }
    for (size_t i = 0; i < nums.size(); i++)
    {
        size_t layer = i / (WIDTH * HEIGHT);
        num_counts_per_layer[layer][nums[i]] += 1;
    }
    auto layer_most_zeros = *std::min_element(num_counts_per_layer.begin(), num_counts_per_layer.end(),
                                              [](std::vector<size_t> a, std::vector<size_t> b) { return a[0] < b[0]; });
    return layer_most_zeros[1] * layer_most_zeros[2];
}

void part_b(const std::vector<int>& nums)
{
    size_t image[HEIGHT][WIDTH];
    for (size_t h = 0; h < HEIGHT; h++)
    {
        for (size_t w = 0; w < WIDTH; w++)
        {
            image[h][w] = 2;
        }
    }

    for (size_t i = 0; i < nums.size(); i++)
    {
        size_t layer = i / (WIDTH * HEIGHT);
        size_t h = (i - layer * WIDTH * HEIGHT) / WIDTH;
        size_t w = (i - layer * WIDTH * HEIGHT) % WIDTH;
        if (image[h][w] == 2 && nums[i] != 2)
        {
            image[h][w] = nums[i];
        }
    }

    for (size_t h = 0; h < HEIGHT; h++)
    {
        for (size_t w = 0; w < WIDTH; w++)
        {
            char r = image[h][w] == 2 ? ' ' : (image[h][w] == 1 ? '#' : '.');
            std::cout << r;
        }
        std::cout << std::endl;
    }
}

int main()
{
    std::ifstream in("input08.txt");
    std::string line;
    in >> line;
    std::vector<int> nums;
    for (size_t i = 0; i < line.size(); i++)
    {
        nums.push_back(static_cast<int>(line[i] - 48));
    }
    std::cout << part_a(nums) << std::endl;
    part_b(nums);
    return 0;
}