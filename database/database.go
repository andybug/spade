package database

//import "fmt"
import "path/filepath"
import log "github.com/Sirupsen/logrus"
import "io/ioutil"

func LoadDatabase(path string) error {
	log.WithFields(log.Fields{
		"path": path,
	}).Info("database: loading database")

	files, err := ioutil.ReadDir(path)
	if err != nil {
		log.WithFields(log.Fields{
			"error": err,
		}).Fatal("database: error reading database")
	}

	for _, file := range files {
		if !file.IsDir() {
			log.WithFields(log.Fields{
				"file": filepath.Join(path, file.Name()),
			}).Debug("database: ignoring non-directory")
		}

		s := Sport{
			name: file.Name(),
			path: filepath.Join(path, file.Name()),
		}
		s.ReadSport()
	}
	return nil
}
