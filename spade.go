package main

import "flag"

//import "fmt"
import log "github.com/Sirupsen/logrus"
import "github.com/andybug/spade/database"

const version string = "0.1.0"

func handle_flags() map[string]string {
	var data_dir = flag.String("data", "/data", "description goes here")
	flag.Parse()

	// log each of the flags
	log.WithFields(log.Fields{
		"data": *data_dir,
	}).Info("arguments parsed")

	// add the flags to config map
	config := map[string]string{
		"data": *data_dir,
	}

	return config
}

func init() {
	log.SetLevel(log.DebugLevel)
}

func main() {
	log.WithFields(log.Fields{
		"version": version,
	}).Info("starting spade")

	config := handle_flags()
	database.LoadDatabase(config["data"])
}
