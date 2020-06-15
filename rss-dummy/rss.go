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
			Title:       "Limiting Concurrency in Go",
			Link:        &feeds.Link{Href: "http://jmoiron.net/blog/limiting-concurrency-in-go/"},
			Description: "A discussion on controlled parallelism in golang",
			Author:      &feeds.Author{Name: "Jason Moiron", Email: "jmoiron@jmoiron.net"},
			Created:     now,
		},
		&feeds.Item{
			Title:       "Logic-less Template Redux",
			Link:        &feeds.Link{Href: "http://jmoiron.net/blog/logicless-template-redux/"},
			Description: "More thoughts on logicless templates",
			Created:     now,
		},
		&feeds.Item{
			Title:       "Idiomatic Code Reuse in Go",
			Link:        &feeds.Link{Href: "http://jmoiron.net/blog/idiomatic-code-reuse-in-go/"},
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
