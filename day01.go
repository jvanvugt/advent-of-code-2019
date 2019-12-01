package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func calculateFuel(mass int) int {
	return mass/3 - 2
}

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func a(masses []int) int {
	total := 0
	for _, mass := range masses {
		total += calculateFuel(mass)
	}
	return total
}

func b(masses []int) int {
	total := 0
	for _, mass := range masses {
		fuel := calculateFuel(mass)
		newFuel := fuel
		for true {
			newFuel = max(calculateFuel(newFuel), 0)
			if newFuel == 0 {
				break
			}
			fuel += newFuel
		}
		total += fuel
	}
	return total
}

func main() {
	text, err := ioutil.ReadFile("input01.txt")
	check(err)
	lines := strings.Split(string(text), "\n")

	masses := make([]int, len(lines))
	for i, v := range lines {
		masses[i], err = strconv.Atoi(v)
		check(err)
	}
	fmt.Println(b(masses))
}
