package main

import (
	"fmt"
	"log"
	"time"

	"net/http"

	"github.com/gorilla/feeds"
)

func main() {

	http.HandleFunc("/blog", dummyBlog)

	http.ListenAndServe(":8020", nil)

	// rss, err := feed.ToRss()
	// if err != nil {
	// 	log.Fatal(err)
	// }

	// json, err := feed.ToJSON()
	// if err != nil {
	// 	log.Fatal(err)
	// }

}

func dummyBlog(w http.ResponseWriter, req *http.Request) {
	now := time.Now()
	feed := &feeds.Feed{
		Title:       "Dummy example blog",
		Link:        &feeds.Link{Href: "http://example.com/blog"},
		Description: "discussion about examples, stuff and more",
		Author:      &feeds.Author{Name: "John Doe", Email: "mail@example.com"},
		Created:     now,
	}

	feed.Items = []*feeds.Item{
		&feeds.Item{
			Title:       "Testing something with Golang",
			Link:        &feeds.Link{Href: "https://example.com/testing-something/"},
			Description: "Testing a cool Golang program to develop a Errbot plugin",
			Author:      &feeds.Author{Name: "Any Body", Email: "any.body@example.com"},
			Created:     now,
		},
		&feeds.Item{
			Title:       "The banana-apple problem",
			Link:        &feeds.Link{Href: "https://example.com/banana-apple-problem/"},
			Description: "More thoughts on problems with apples and bananas.",
			Created:     now,
		},
		&feeds.Item{
			Title:       "Fun with flags",
			Link:        &feeds.Link{Href: "https://example.com/fun-with-flags/"},
			Description: "How to use interfaces <em>effectively</em>",
			Created:     now,
		},
	}

	atom, err := feed.ToAtom()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Fprintf(w, atom)
	fmt.Println("Site was accessed!")
}
