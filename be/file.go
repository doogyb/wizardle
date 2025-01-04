package main

import (
	"fmt"
	"io"
	"log"
	"os"

	"encoding/json"
)

func loadQuotes() []Quote {

	var quotes []Quote

	entries, err := os.ReadDir("../ds/data/quotes")
	if err != nil {
		log.Fatal(err)
	}

	for _, e := range entries {
		var book []Quote
		jsonFile, err := os.Open(fmt.Sprintf("../ds/data/quotes/%s", e.Name()))

		if err != nil {
			fmt.Println(err)
		}

		defer jsonFile.Close()
		byteValue, _ := io.ReadAll(jsonFile)

		json.Unmarshal(byteValue, &book)
		quotes = append(quotes, book...)
	}

	return quotes
}
