package database

import "encoding/csv"
import "io"
import "path/filepath"
import log "github.com/Sirupsen/logrus"
import "os"

type Sport struct {
	name string
	path string
	seasons []Season
	teams map[string]Team
}

type Team struct {
	name string
	id uint
}

func (s *Sport) ReadSport() {
	log.WithFields(log.Fields{
		"sport": s.name,
		"path": s.path,
	}).Info("database: reading sport")

	s.readTeams()
}

func (s *Sport) readTeams() {
	path := filepath.Join(s.path, "teams.csv")
	log.WithFields(log.Fields{
		"sport": s.name,
		"path": path,
	}).Info("database: reading teams")

	io_reader, err := os.Open(path)
	if err != nil {
		log.WithFields(log.Fields{
			"sport": s.name,
			"path": path,
			"error": err,
		}).Fatal("database: error reading teams")
	}

	s.teams = make(map[string]Team)
	var num_teams uint = 0
	reader := csv.NewReader(io_reader)
	reader.Read() // drop heading line
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}

		if err != nil {
			log.WithFields(log.Fields{
				"sport": s.name,
				"path": path,
				"error": err,
			}).Fatal("database: error parsing teams file")
		}

		s.teams[record[0]] = Team{
			name: record[1],
			id: num_teams,
		}

		num_teams++
	}

	log.WithFields(log.Fields{
		"sport": s.name,
		"path": path,
		"teams": num_teams,
	}).Info("database: done reading teams")
}
