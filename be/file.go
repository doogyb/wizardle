package main

import (
	"fmt"
	"io"
	"os"

	"encoding/json"
)

func loadQuotes() []Quote {

	var quotes []Quote

	jsonFile, err := os.Open("../ds/data/quotes.json")

	if err != nil {
		fmt.Println(err)
	}

	defer jsonFile.Close()

	byteValue, _ := io.ReadAll(jsonFile)

	json.Unmarshal(byteValue, &quotes)
	return quotes
}
