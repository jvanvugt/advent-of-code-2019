#include <fstream>
#include <iostream>
#include <numeric>
#include <regex>
#include <set>
#include <vector>

struct Vector3
{
    int x;
    int y;
    int z;

    Vector3 operator+(const Vector3& other) const
    {
        return {x + other.x, y + other.y, z + other.z};
    }

    int operator[](size_t i) const
    {
        switch (i)
        {
            case 0: return x;
            case 1: return y;
            case 2: return z;
        }
    }
};

std::ostream& operator<<(std::ostream& out, const Vector3& v)
{
    return out << "Vector3(" << v.x << ", " << v.y << ", " << v.z << ")";
}


struct Moon
{
    Vector3 position;
    Vector3 velocity;

    Moon(Vector3 position_) : position(position_), velocity({})
    {
    }
};

std::ostream& operator<<(std::ostream& out, const Moon& moon)
{
    return out << "Moon(position=" << moon.position << ", velocity=" << moon.velocity << ")";
}


int sum_abs(Vector3 v)
{
    return std::abs(v.x) + std::abs(v.y) + std::abs(v.z);
}


void simulate(std::vector<Moon>& moons, size_t steps)
{
    for (size_t i = 0; i < steps; i++)
    {
        for (auto& moon : moons)
        {
            for (auto& other : moons)
            {
                if (moon.position.x > other.position.x)
                {
                    moon.velocity.x--;
                    other.velocity.x++;
                }
                if (moon.position.y > other.position.y)
                {
                    moon.velocity.y--;
                    other.velocity.y++;
                }
                if (moon.position.z > other.position.z)
                {
                    moon.velocity.z--;
                    other.velocity.z++;
                }
            }
        }

        for (auto& moon : moons)
        {
            moon.position = moon.position + moon.velocity;
        }
    }
}

size_t part_a(std::vector<Moon>& moons)
{
    simulate(moons, 1000);
    int result = 0;
    for (const Moon& moon : moons)
    {
        result += sum_abs(moon.position) * sum_abs(moon.velocity);
    }
    return result;
}


template <size_t i>
std::vector<int> get_coords(std::vector<Moon>& moons)
{
    std::vector<int> coords(moons.size());
    for (auto& moon : moons)
    {
        coords.push_back(moon.position[i]);
        coords.push_back(moon.velocity[i]);
    }
    return coords;
}


size_t part_b(std::vector<Moon>& moons)
{
    std::vector<int> original_x = get_coords<0>(moons);
    std::vector<int> original_y = get_coords<1>(moons);
    std::vector<int> original_z = get_coords<2>(moons);

    size_t x_repeat = 0, y_repeat = 0, z_repeat = 0;
    for (size_t i = 1; i < 1000000; i++)
    {
        simulate(moons, 1);
        if (x_repeat == 0 && original_x == get_coords<0>(moons))
        {
            x_repeat = i;
        }
        if (y_repeat == 0 && original_y == get_coords<1>(moons))
        {
            y_repeat = i;
        }
        if (z_repeat == 0 && original_z == get_coords<2>(moons))
        {
            z_repeat = i;
        }
        if (x_repeat != 0 && y_repeat != 0 && z_repeat != 0)
        {
            break;
        }
    }


    return std::lcm(std::lcm(x_repeat, y_repeat), z_repeat);
}


int main()
{
    std::ifstream in("input12.txt");
    std::string line;
    std::vector<Moon> moons;
    std::regex number("(-?\\d+)");
    while (in.good())
    {
        std::getline(in, line);
        auto numbers = std::sregex_iterator(line.begin(), line.end(), number);
        if (numbers == std::sregex_iterator())
        {
            std::cout << "Did not match regex" << std::endl;
            return 1;
        }
        int x = std::stoi((*numbers++).str());
        int y = std::stoi((*numbers++).str());
        int z = std::stoi((*numbers++).str());
        moons.emplace_back(Vector3{x, y, z});
    }
    std::cout << part_b(moons) << std::endl;
    return 0;
}