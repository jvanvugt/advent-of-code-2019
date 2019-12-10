#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <vector>

using Vector2 = std::pair<int, int>;


Vector2 operator-(const Vector2& a, const Vector2& b)
{
    return {a.first - b.first, a.second - b.second};
}


Vector2 operator+(const Vector2& a, const Vector2& b)
{
    return {a.first + b.first, a.second + b.second};
}


Vector2 operator/(const Vector2& a, int d)
{
    return {a.first / d, a.second / d};
}

std::ostream& operator<<(std::ostream& out, const Vector2& a)
{
    return out << "(" << a.first << ", " << a.second << ")";
}

template <typename T>
std::ostream& operator<<(std::ostream& out, const std::vector<T>& a)
{
    out << "[";
    for (size_t i = 0; i < a.size(); i++)
    {
        out << a[i];
        if (i < a.size() - 1)
        {
            out << ", ";
        }
    }
    return out << "]";
}


Vector2 normalize(const Vector2& direction)
{
    if (direction.first == 0 && direction.second == 0)
    {
        return direction;
    }
    auto d = std::gcd(direction.first, direction.second);
    return direction / d;
}

std::pair<size_t, Vector2> part_a(std::vector<Vector2>& asteroids)
{
    size_t most = 0;
    Vector2 loc;
    for (const auto& asteroid : asteroids)
    {
        std::set<Vector2> directions;
        for (const auto& other : asteroids)
        {
            if (&asteroid != &other)
            {
                auto dir = normalize(asteroid - other);
                directions.emplace(dir);
            }
        }
        if (directions.size() > most)
        {
            most = directions.size();
            loc = asteroid;
        }
        most = std::max(most, directions.size());
    }
    return {most, loc};
}


double angle_from_top(const Vector2& v)
{
    return std::fmod(std::atan2(static_cast<double>(-v.second), static_cast<double>(v.first)) + 1.5 * M_PI, 2 * M_PI);
}


int manhattan(const Vector2& a, const Vector2& b)
{
    return std::abs(a.first - b.first) + std::abs(a.second - b.second);
}


int part_b(std::vector<Vector2>& asteroids)
{
    auto res = part_a(asteroids);
    auto location = res.second;
    std::map<Vector2, std::vector<Vector2>> asts_per_dir;
    for (const auto& other : asteroids)
    {
        if (location.first != other.first || location.second != other.second)
        {
            auto relpos = other - location;
            auto dir = normalize(relpos);
            asts_per_dir[dir].emplace_back(relpos);
        }
    }
    std::vector<Vector2> keys(asts_per_dir.size());
    std::transform(asts_per_dir.begin(), asts_per_dir.end(), keys.begin(),
                   [](std::pair<Vector2, std::vector<Vector2>> el) { return el.first; });
    // Sort keys clockwise by angle from top
    std::sort(keys.begin(), keys.end(),
              [](const Vector2& a, const Vector2& b) { return angle_from_top(a) > angle_from_top(b); });
    // Start up
    if (keys.back().first == 0 && keys.back().second == -1)
    {
        keys.insert(keys.begin(), keys.back());
        keys.pop_back();
    }

    // Sort asteroids per direction by distance from location (reverse)
    for (const auto& key : keys)
    {
        std::sort(asts_per_dir[key].begin(), asts_per_dir[key].end(), [&location](const Vector2& a, const Vector2& b) {
            return manhattan(a, location) > manhattan(b, location);
        });
    }
    int i = 0;
    while (true)
    {
        for (const auto& key : keys)
        {
            if (asts_per_dir[key].size() > 0)
            {
                auto asteroid = asts_per_dir[key].back();
                asts_per_dir[key].pop_back();
                if (++i == 200)
                {
                    asteroid = asteroid + location;
                    return asteroid.first * 100 + asteroid.second;
                }
            }
        }
    }
}

int main()
{
    std::ifstream in("input10.txt");
    std::vector<Vector2> asteroids;
    std::string line;
    for (int y = 0; in.good(); y++)
    {
        in >> line;
        for (int x = 0; x < line.size(); x++)
        {
            if (line[x] == '#')
            {
                asteroids.emplace_back(x, y);
            }
        }
    }
    std::cout << part_b(asteroids) << std::endl;
    return 0;
}
