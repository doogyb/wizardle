package main

type Quote struct {
	Book    string `json:"book"`
	Chapter string `json:"chapter"`
	Speaker string `json:"speaker"`
	Content string `json:"content"`
}
