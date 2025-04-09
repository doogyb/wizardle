package main

import (
	"io"
	"os"
	"log"

	"encoding/json"
)

func loadQuotes() []Quote {

	var quotes []Quote

	jsonFile, err := os.Open("../ds/data/quotes/filtered.json")
	defer jsonFile.Close()

	if err != nil {
		log.Fatal(err)
		return quotes
	}

	byteValue, _ := io.ReadAll(jsonFile)

	json.Unmarshal(byteValue, &quotes)
	return quotes
}
