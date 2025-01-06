package main

import (
	"fmt"

	"math/rand"

	"github.com/gin-gonic/gin"
)

var quotes []Quote

func getRandomQuote(c *gin.Context) {
	c.IndentedJSON(200, quotes[rand.Intn(len(quotes))])
}

func main() {

	quotes = loadQuotes()
	fmt.Println(quotes)

	router := gin.Default()
	router.GET("/random-quote", getRandomQuote)

	router.Run()

}
